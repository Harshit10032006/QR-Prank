from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_view, name='upload'),
    path('', views.gallery_view, name='gallery'),
    path('scan/<uuid:pk>/', views.scan_view, name='scan'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)