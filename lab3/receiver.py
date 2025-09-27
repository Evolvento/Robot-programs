import imaplib
import email
from email.header import decode_header
import os
import time


class Receiver:
    
    def __init__(self, config):
        self.config = config
        self.attachments_dir = self.config["folder_for_attachments"]
        
        # cоздаем папку для вложений если не существует
        if not os.path.exists(self.config["folder_for_attachments"]):
            os.makedirs(self.config["folder_for_attachments"])
    
    def connect(self):
        try:
            self.imap_server = imaplib.IMAP4_SSL(self.config["IMAP_server"], self.config["IMAP_port"])
            self.imap_server.login(self.config["yandex_email"], self.config["yandex_password"])
            print("Успешное подключение к IMAP серверу")
            return True
        except Exception as e:
            print(f"Ошибка подключения к IMAP: {e}")
            return False
    
    def disconnect(self):
        if self.imap_server:
            self.imap_server.logout()
            print("Соединение с IMAP сервером закрыто")
    
    def decode_mime_words(self, text):
        if text is None:
            return None
        
        decoded_parts = decode_header(text)
        decoded_text = ''
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_text += part.decode(encoding)
                else:
                    decoded_text += part.decode('utf-8', errors='ignore')
            else:
                decoded_text += part
        
        return decoded_text
    
    def search_emails_by_subject(self, subject):
        if not self.connect():
            return []
        
        self.imap_server.select('INBOX')
            
        search_criteria = f'SUBJECT "{subject}"'
        status, messages = self.imap_server.search(None, search_criteria)
            
        if status != 'OK':
            print("Ошибка поиска писем")
            return []
            
        email_ids = messages[0].split()
            
        return email_ids
    
    def download_attachments(self, email_id):
        if not self.connect():
            return False
        
        self.imap_server.select('INBOX')
        status, msg_data = self.imap_server.fetch(email_id, '(RFC822)')
            
        if status != 'OK':
            return False
            
        msg = email.message_from_bytes(msg_data[0][1])
            
        subject = self.decode_mime_words(msg['Subject'])
        from_ = self.decode_mime_words(msg['From'])
        date = msg['Date']
            
        downloaded_files = []
            
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                    
                if filename:
                    filename = self.decode_mime_words(filename)

                    filepath = os.path.join(self.attachments_dir, filename)
                        
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                        
                    downloaded_files.append(filepath)
            
        return downloaded_files
    
    def process_emails_with_attachments(self):

        subject = self.config["subject"]
        
        email_ids = self.search_emails_by_subject(subject)
        
        if not email_ids:
            print("Письма не найдены")
            return
        
        total_downloaded = 0
        
        for email_id in email_ids:
            downloaded_files = self.download_attachments(email_id)
            if downloaded_files:
                total_downloaded += len(downloaded_files)
            
            time.sleep(1)
        