from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('service/', views.service, name='service'),
    path('actualite/', views.page_actualite, name='page_actualite'),
    path('actualite/<int:pk>/', views.detail_actualite, name='detail_actualite'),
    path('concours/', views.liste_concours, name='liste_concours'),
    path('profile/', views.update_profile, name='profile'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)