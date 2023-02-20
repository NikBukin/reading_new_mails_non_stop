import config
import email
import time
import imaplib
from csv import writer

imap = imaplib.IMAP4_SSL("imap.mail.ru")

# Авторизация
imap.login(config.Y_LOGIN, config.MY_PASSWORD)

imap.select("inbox")

# Поиск новых непрочитанных писем
status, email_ids = imap.search(None, "(UNSEEN)")

# Бесконечный цикл, который проверяет поступление новых писем
# и выводит адрес отправителя с его сообщением
while True:
    status, email_ids = imap.search(None, "(UNSEEN)")

    for email_id in email_ids[0].split():
        status, email_data = imap.fetch(email_id, "(RFC822)")

        email_message = email.message_from_bytes(email_data[0][1])

        sender = email.utils.parseaddr(email_message["From"])[1]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                message = part.get_payload(decode=True).decode(encoding="utf-8", errors='ignore')

        # # Вывод адреса отправителя с его сообщением
        # print("From:", sender)
        # print("Message:", message)

        # Добавление адреса пользователя и его сообщения в csv файл
        list_data = [message, sender]

        with open("users_card.csv", 'a', newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(list_data)
            f_object.close()

    # Проверка проводится каждые 30 секунд чтобы не нагружать систему (в боте использовал 15, так как была
    # необходимость в оперативности)
    time.sleep(30)

imap.close()
imap.logout()

# Полезная инфа с обработкой вложенных файлов на будущее
# https://habr.com/ru/post/688784/
