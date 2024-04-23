import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(image_path, data, content):
    sender_email = 'iotpoppinger@gmail.com'
    app_password = 'efoz uuea ymsr ceul' 
    recipient_email = 'iotpoppinger@gmail.com'

    temperature = data['temperature']
    humidity = data['humidity']
    pressure = data['pressure']

    timestamp = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f'Smart Home Monitoring Alert {timestamp}'

    if content == 0:
        body = (f"Hello,\n\n"
            f"Motion has been detected in your monitored area. Here are the current environmental readings:\n"
            f"Temperature: {temperature:.2f}°C\n"
            f"Humidity: {humidity:.2f}%\n"
            f"Pressure: {pressure:.2f} hPa\n\n"
            f"Attached is the image captured during the motion event.")
    elif content == 1:
        body = (f"Hello,\n\n"
            f"Here are the current environmental readings:\n"
            f"Temperature: {temperature:.2f}°C\n"
            f"Humidity: {humidity:.2f}%\n"
            f"Pressure: {pressure:.2f} hPa\n\n"
            f"Attached is the image captured during the motion event.")

    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, 'rb') as file:
        img = MIMEImage(file.read(), name=os.path.basename(image_path))
    msg.attach(img)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    server.login(sender_email, app_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

    print("Email sent successfully with the attached image and environmental data")
