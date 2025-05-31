from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import QRCodeHistory
import qrcode
from django.core.files import File
from io import BytesIO
import os

def generate_qr(request):
    if request.method == 'POST':
        upi_id = request.POST.get('upi_id')
        amount = request.POST.get('amount', '100')
        message = request.POST.get('message', 'Payment')

        # Generate QR codes
        phonepe_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"
        gpay_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"
        paytm_url = f"upi://pay?pa={upi_id}&pn={upi_id}&am={amount}&tn={message}"

        # Create QR code images
        phonepe_qr = qrcode.make(phonepe_url)
        gpay_qr = qrcode.make(gpay_url)
        paytm_qr = qrcode.make(paytm_url)

        # Save QR codes to BytesIO objects
        phonepe_buffer = BytesIO()
        gpay_buffer = BytesIO()
        paytm_buffer = BytesIO()

        phonepe_qr.save(phonepe_buffer, format='PNG')
        gpay_qr.save(gpay_buffer, format='PNG')
        paytm_qr.save(paytm_buffer, format='PNG')

        # Create QRCodeHistory instance
        qr_history = QRCodeHistory(
            upi_id=upi_id,
            amount=amount,
            message=message
        )

        # Save QR code images
        phonepe_buffer.seek(0)
        gpay_buffer.seek(0)
        paytm_buffer.seek(0)

        qr_history.phonepe_qr.save(f'phonepe_{upi_id}.png', File(phonepe_buffer), save=False)
        qr_history.gpay_qr.save(f'gpay_{upi_id}.png', File(gpay_buffer), save=False)
        qr_history.paytm_qr.save(f'paytm_{upi_id}.png', File(paytm_buffer), save=False)
        qr_history.save()

        return redirect('history')

    return render(request, 'qr_app/generate.html')

class QRCodeHistoryView(ListView):
    model = QRCodeHistory
    template_name = 'qr_app/history.html'
    context_object_name = 'qr_codes'
    ordering = ['-created_at']
