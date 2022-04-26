#!/bin/python3.9
import config, re, smtplib, os
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

os.chdir(os.path.dirname(__file__))

smtp = smtplib.SMTP(config.HOSTNAME, port=config.PORT)

smtp.ehlo()
smtp.starttls()
smtp.ehlo()

smtp.login(config.LOGIN, config.PASSWORD)

for mail in Path('scheduled').glob('*.mail'):
    with mail.open('r') as file:
        msg = file.read()

        scheduled = re.findall(r'Scheduled to \(UTC\): (.*)\n', msg)[0]
        scheduled = datetime.fromisoformat(scheduled)

        if scheduled <= datetime.utcnow():
            to_address = re.findall(r'To: (.*)\n', msg)[0]
            subject = re.findall(r'Subject: (.*)\n', msg)[0]

            body = ''
            reading_body = False
            for line in msg.splitlines():
                if reading_body:
                    body += f'{line}\n'
                elif line == '---- Body ----':
                    reading_body = True

            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = config.EMAIL
            msg['To'] = to_address

            smtp.send_message(msg)
            os.makedirs('sent', exist_ok=True)
            mail.rename(Path('sent') / mail.name)

smtp.quit()
