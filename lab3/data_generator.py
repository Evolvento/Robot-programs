import random
import string
from datetime import datetime


class DataGenerator:
    
    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def generate_random_subject():
        subjects = [
            "Важное уведомление",
            "Еженедельный отчет",
            "Обновление системы",
            "Новости проекта",
            "Тестовое сообщение"
        ]
        return f"{random.choice(subjects)} #{DataGenerator.generate_random_string(5)}"
    
    @staticmethod
    def generate_html_content():
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        color = random.choice(colors)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .header {{
                    background-color: {color};
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px;
                }}
                .content {{
                    padding: 20px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px;
                    font-size: 0.9em;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Тестовое письмо</h1>
            </div>
            <div class="content">
                <p>Здравствуйте!</p>
                <p>Это <strong>тестовое письмо</strong>, сгенерированное автоматически.</p>
                <p>Дата отправки: <em>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
                <p>Случайный идентификатор: <code>{DataGenerator.generate_random_string(8)}</code></p>
                <ul>
                    <li>Пункт 1: {DataGenerator.generate_random_string(15)}</li>
                    <li>Пункт 2: {DataGenerator.generate_random_string(15)}</li>
                    <li>Пункт 3: {DataGenerator.generate_random_string(15)}</li>
                </ul>
            </div>
            <div class="footer">
                <p>Это письмо создано автоматически. Пожалуйста, не отвечайте на него.</p>
            </div>
        </body>
        </html>
        """
        return html_content