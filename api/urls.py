from django.urls import path
from .views import UploadExcelView 

from uploader.views import ListExcelFilesView, DownloadAllFilesView

urlpatterns = [
    path('upload-excel/', UploadExcelView.as_view(), name='upload_excel'),
    path('list-excel-files/', ListExcelFilesView.as_view(), name='list_excel_files'),
    path('download-all-excel/', DownloadAllFilesView.as_view(), name='download_all_excel'),
]
