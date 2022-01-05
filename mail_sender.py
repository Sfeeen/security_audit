# Created by Sven Onderbeke at 01/03/2021
import smtplib
from email.mime.text import MIMEText

def send_mail(subject, body, recipients, html=True):
    if type(recipients) != type([]):
        recipients = [recipients]

    smtp_ssl_host = ''  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    username = ""
    password = ""
    sender = ""

    if html:
        msg = MIMEText(body, "html")
    else:
        msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()
