from django.urls import path
from .views import ListExcelFilesView, DownloadAllFilesView


urlpatterns = [
    path('list-excel-files/', ListExcelFilesView.as_view(), name='list_excel_files'),
    path('download-all-excel/', DownloadAllFilesView.as_view(), name='download_all_excel'),
]
