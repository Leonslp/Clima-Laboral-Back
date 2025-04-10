import os
import datetime
import tempfile
import zipfile
from io import BytesIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse

from api.firebase_config import bucket  # ✅ Importar el bucket correctamente

class UploadExcelView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        user_id = request.POST.get('username', 'sin_nombre')

        if not file:
            return Response({'error': 'No se envió ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ruta destino en Firebase Storage
            fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            ruta_archivo = f"archivos_excel/{user_id}/respuestas_{fecha}.xlsx"

            # Subida a Firebase Storage
            blob = bucket.blob(ruta_archivo)
            blob.upload_from_file(
                file,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            # Hacer público (opcional)
            blob.make_public()

            return Response({'message': 'Archivo subido con éxito', 'url': blob.public_url}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error exacto al subir archivo:", str(e))  # ✅ Log para depuración
            return Response({'error': f'Error al subir archivo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListExcelFilesView(APIView):
    def get(self, request):
        try:
            blobs = bucket.list_blobs(prefix="archivos_excel/")
            file_urls = []

            for blob in blobs:
                url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(hours=1))
                file_urls.append({
                    "name": blob.name,
                    "url": url
                })

            return Response(file_urls, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error al listar archivos:", str(e))
            return Response({'error': f'Error al listar archivos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadAllFilesView(APIView):
    def get(self, request):
        try:
            blobs = bucket.list_blobs(prefix="archivos_excel/")

            with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
                with zipfile.ZipFile(tmp_zip.name, 'w') as zipf:
                    for blob in blobs:
                        if blob.name.endswith('.xlsx'):
                            file_data = blob.download_as_bytes()
                            zipf.writestr(blob.name, file_data)

                tmp_zip.flush()
                response = FileResponse(open(tmp_zip.name, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="archivos_excel.zip"'
                return response

        except Exception as e:
            print("Error al generar ZIP:", str(e))
            return Response({'error': f'No se pudo generar el ZIP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
