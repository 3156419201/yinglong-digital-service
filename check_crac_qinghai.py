import smtplib

# Function to send an email

def send_email(recipient_email):
    sender_email = 'your_email@example.com'
    message = 'Subject: Test Email\n\nThis is a test email.'

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, 'your_password')
        server.sendmail(sender_email, recipient_email, message)

if __name__ == '__main__':
    recipient = 'recipient@example.com'
    send_email(recipient)
