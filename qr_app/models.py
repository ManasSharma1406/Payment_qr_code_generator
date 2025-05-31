from django.db import models
from django.utils import timezone

# Create your models here.

class QRCodeHistory(models.Model):
    upi_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    message = models.CharField(max_length=255, default='Payment')
    phonepe_qr = models.ImageField(upload_to='qr_codes/')
    gpay_qr = models.ImageField(upload_to='qr_codes/')
    paytm_qr = models.ImageField(upload_to='qr_codes/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"QR Code for {self.upi_id} - {self.created_at}"
