import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore

# Vista para guardar respuestas en Firestore
class UploadExcelView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data  # Respuestas enviadas desde React
            user_id = data.get('username', 'sin_nombre')
            fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Guardar en Firestore
            db = firestore.client()
            doc_ref = db.collection('respuestas').document(f"{user_id}_{fecha}")
            doc_ref.set(dict(data))  # Asegúrate que sea un diccionario serializable

            return Response({'message': 'Respuestas guardadas con éxito'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Error al guardar respuestas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para listar las respuestas guardadas en Firestore
class ListExcelFilesView(APIView):
    def get(self, request):
        try:
            db = firestore.client()
            respuestas = db.collection('respuestas').stream()
            data = []

            for doc in respuestas:
                doc_data = doc.to_dict()
                doc_data['id'] = doc.id
                data.append(doc_data)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al obtener respuestas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para descargar todas las respuestas en un ZIP (si decides generar Excel en backend luego)
class DownloadAllFilesView(APIView):
    def get(self, request):
        return Response({'message': 'Funcionalidad de descarga masiva no disponible por ahora. Se puede implementar con archivos generados en frontend y backend si se desea.'})
