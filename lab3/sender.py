import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
from data_generator import DataGenerator


class Sender:

    def __init__(self, config):
        self.config = config
    
    def connect(self):
        try:
            self.smtp_server = smtplib.SMTP(self.config["SMTP_server"], self.config["SMTP_port"])
            self.smtp_server.starttls()  # шифрование
            self.smtp_server.login(self.config["yandex_email"], self.config["yandex_password"])
            print("Успешное подключение к SMTP серверу")
            return True
        except Exception as e:
            print(f"Ошибка подключения к SMTP: {e}")
            return False

    def disconnect(self):
        if self.smtp_server:
            self.smtp_server.quit()
            print("Соединение с SMTP сервером закрыто")   

    def send(self, email_from = "NiZel145@yandex.ru", email_to = "zelent.nikita@mail.ru"):
        msg = MIMEMultipart()
        msg['From'] = "NiZel145@yandex.ru"
        msg['To'] = "zelent.nikita@mail.ru"
        msg['Subject'] = DataGenerator.generate_random_subject()
        msg['Date'] = email.utils.formatdate(localtime=True)

        body = MIMEText(DataGenerator.generate_html_content(), 'html')
        msg.attach(body)
        
        self.smtp_server.send_message(msg)
        print("Письмо отправлено успешно")


