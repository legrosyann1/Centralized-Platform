from backend import settings
import logging
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders

class Email():
    addr_from = settings.EMAIL_HOST_USER
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    password = settings.EMAIL_HOST_PASSWORD

    def send(self, addr_to, subject, body, file=None, filename=None):
        
        msg = MIMEMultipart() 
        msg['To'] = addr_to
        msg['From'] = self.addr_from
        msg['Subject'] = subject
        try:
            msg.attach(MIMEText(body,'plain'))
            if file != None:
                adjunto = MIMEBase('multipart','encrypted')
                adjunto.set_payload(file.read()) 
                file.close()
                encoders.encode_base64(adjunto) 
                adjunto.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(adjunto) 
                
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.addr_from, self.password)
            server.sendmail(self.addr_from, addr_to, msg.as_string())
            server.quit()
            return "1"
        except Exception as e:
            print(e)
            return e