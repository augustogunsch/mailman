#!/bin/python3.9
import os, tempfile, subprocess, re, sys
from datetime import datetime, timedelta

os.chdir(os.path.dirname(__file__))

EDITOR = os.environ.get('EDITOR', 'vim')

os.makedirs('scheduled', exist_ok=True)

tomorrow = datetime.utcnow() + timedelta(days=1)
tomorrow = tomorrow.replace(microsecond=0, second=0, minute=int(tomorrow.minute/15))
initial_msg = f'To: \nSubject: \nScheduled to (UTC): {tomorrow.isoformat()}\n---- Body ----'

with tempfile.NamedTemporaryFile() as file:
    file.write(bytes(initial_msg, encoding='utf-8'))
    file.flush()

    subprocess.call([EDITOR, file.name])

    file.seek(0)
    msg = file.read().decode()


to = re.findall(r'To: (.*)\n', msg)[0]
subject = re.findall(r'Subject: (.*)\n', msg)[0]

if not to or not subject:
    print('ERROR: recipient or subject empty')
    exit(1)

filename = f'scheduled/{to}:{subject}.mail'

if os.path.exists(filename):
    print('ERROR: an email for this recipient with the same subject is already scheduled')
    exit(1)

with open(filename, 'w') as file:
    file.write(msg)
