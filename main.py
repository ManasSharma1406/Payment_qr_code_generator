import qrcode

#Taking The UPI ID As Input
UPI_ID = input("Enter Your Payment UPI ID :- ")

#Generating The QR Code
# upi: upi://pay?pa=upi_id&pn=upi_id&am=amount&tn=MESSAGE

#Creating The QR Code
phonepe_url = f"upi://pay?pa={UPI_ID}&pn={UPI_ID}&am=100&tn=Payment"
Googlepay_url = f"upi://pay?pa={UPI_ID}&pn={UPI_ID}&am=100&tn=Payment"
paytm_url = f"upi://pay?pa={UPI_ID}&pn={UPI_ID}&am=100&tn=Payment"

#Creating The QR Code for each payment app

phonepe_qr = qrcode.make(phonepe_url)
gpay_qr = qrcode.make(Googlepay_url)
paytm_qr = qrcode.make(paytm_url)

#Saving The QR Code
phonepe_qr.save("phonepe_qr.png")
gpay_qr.save("gpay_qr.png")
paytm_qr.save("paytm_qr.png")

#Displaying The QR Code
print("QR Code Generated Successfully")
print("Phonepe QR Code Saved As phonepe_qr.png")
print("Google Pay QR Code Saved As gpay_qr.png")
print("Paytm QR Code Saved As paytm_qr.png")

phonepe_qr.show()
gpay_qr.show()
paytm_qr.show()




