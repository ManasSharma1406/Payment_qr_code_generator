from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_qr, name='generate'),
    path('history/', views.QRCodeHistoryView.as_view(), name='history'),
] 