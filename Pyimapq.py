import os
import email
import imaplib
import time
import json
import base64


class PyImapQ(object):
    def __init__(self, user, password, server='imap.gmail.com'):
        self._user = user
        self._password = password
        self._server = server
        self._mail = None
        self._connect_imap()
        assert self.connected

    def _connect_imap(self):
        for _ in range(5):
            try:
                mail = imaplib.IMAP4_SSL(self._server)
                (retcode, capabilities) = mail.login(self._user, self._password)
                self._mail = mail
                return
            except:
                pass
            time.sleep(2)
        print(f'erorr connecting to {self._server}')
        self._mail = None

    @property
    def connected(self):
        return self._mail is not None

    def get_unread_emails(self, filter_subject, mark_as_read=True, inbox='inbox'):
        ans = []
        self._mail.select(inbox)
        (retcode, messages) = self._mail.search(None, '(UNSEEN)')
        if retcode == 'OK':
            for num in messages[0].split():
                typ, data = self._mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = email.message_from_bytes(response_part[1])
                        if filter_subject(original['Subject']):
                            ans.append(original)
                            if mark_as_read:
                                typ, data = self._mail.store(num, '+FLAGS', '\\Seen')
                            else:
                                typ, data = self._mail.store(num, '-FLAGS', '\\Seen')
                        else:
                            if not mark_as_read:
                                typ, data = self._mail.store(num, '-FLAGS', '\\Seen')
        return ans

    def send_mail(self, to, subject='', body='', attachment=None):
        import smtplib
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart()

        msg['From'] = self._user
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment is not None:
            att = open(attachment, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((att).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment)}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self._user, self._password)
        text = msg.as_string()
        server.sendmail(self._user, to, text)
        server.quit()

    @staticmethod
    def encode_body(obj):
        return base64.encodestring(json.dumps(obj))

    @staticmethod
    def get_body(msg):
        for part in msg.walk():
            ans = ''
            try:
                ans += part.get_payload(decode=True)
            except:
                pass
        return ans

    @staticmethod
    def decode_body(msg):
        for part in msg.walk():
            try:
                return json.loads(base64.decodestring(part.get_payload(decode=True)))
            except:
                pass
        return None
