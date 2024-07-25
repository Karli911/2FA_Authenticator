import qrcode

def generate_qr_code(secret, user_email):
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(user_email, issuer_name="2faC")
    qr = qrcode.make(provisioning_uri)

    # Save QR code to a temporary file
    temp_qr_path = 'temp_qr_code.png'
    qr.save(temp_qr_path)

    return temp_qr_path, provisioning_uri