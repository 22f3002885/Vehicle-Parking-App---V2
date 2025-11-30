import smtplib
from email.mime.text import MIMEText

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'admin@parkease.com'

def send_email(to_email, subject, body):
    """Send plain text email"""
    msg = MIMEText(body, 'plain')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_email_with_lots(to_email, subject, body, lots):
    """Send plain text email with parking lot details"""
    lot_details = "\n".join(
        [f"Lot Name: {lot.name}, Address: {lot.address}, Price per Hour: ₹{lot.price_per_hour}" for lot in lots]
    )
    full_body = f"{body}\n\nAvailable Parking Lots:\n{lot_details}"
    send_email(to_email, subject, full_body)

def send_html_email(to_email, subject, html_body):
    """Send HTML formatted email"""
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"HTML email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send HTML email: {e}")
