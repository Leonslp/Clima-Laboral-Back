from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({"message": "API funcionando correctamente"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include('api.urls')),         
    path('uploader/', include('uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
