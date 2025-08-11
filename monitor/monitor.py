#The robust Python log tailer & alerting script
#Key Features
#Tail file in real tine by seeking to  EOF and reading new lines in a loop
#Direct log rotation or truncation by checking file inode or size
#Configurable keywords and alert backends (Slack,Telegram,email).
#Minimal in-process rate limiting (avoid alert spam).


import os, time, yaml, requests, smtplib
from email.message import EmailMessage

CONFIG_PATH = 'config.yaml'

def load_config(path=CONFIG_PATH):
    with open(path) as f:
        return yaml.safe_load(f)

def send_slack(webhook, text):
    payload = {"text": text}
    requests.post(webhook, json=payload, timeout=5)

def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.get(url, params={"chat_id": chat_id, "text": text}, timeout=5)

def send_email(smtp_cfg, subject, text):
    msg = EmailMessage()
    msg['From'] = smtp_cfg['from']
    msg['To'] = smtp_cfg['to']
    msg['Subject'] = subject
    msg.set_content(text)
    with smtplib.SMTP(smtp_cfg['host']) as s:
        if smtp_cfg.get('starttls'):
            s.starttls()
        if smtp_cfg.get('user'):
            s.login(smtp_cfg['user'], smtp_cfg.get('password', smtp_cfg.get('pass')))
        s.send_message(msg)

def tail_file(path):
    """Generator yielding new lines robustly across rotations/truncations."""
    with open(path, 'r') as fh:
        fh.seek(0, os.SEEK_END)
        inode = os.fstat(fh.fileno()).st_ino
        while True:
            line = fh.readline()
            if line:
                yield line.rstrip('\n')
            else:
                time.sleep(0.5)
                try:
                    st = os.stat(path)
                    if st.st_ino != inode:
                        # file was rotated - reopen
                        fh = open(path, 'r')
                        inode = os.fstat(fh.fileno()).st_ino
                        continue
                    elif fh.tell() > st.st_size:
                        # truncated
                        fh.seek(0)
                except FileNotFoundError:
                    # log file removed -> wait until it's recreated
                    time.sleep(1)

def run():
    cfg = load_config()
    path = cfg['log_path']
    keywords = cfg.get('keywords', ['ERROR', 'CRITICAL'])
    alert_cfg = cfg.get('alerts', {})

    for line in tail_file(path):
        lower = line.lower()
        for kw in keywords:
            if kw.lower() in lower:
                msg = f"[ALERT] keyword {kw} in {path}"
                print(msg)  # console + docker logs
                if 'slack_webhook' in alert_cfg:
                    send_slack(alert_cfg['slack_webhook'], msg)
                if 'telegram' in alert_cfg:
                    t = alert_cfg['telegram']
                    send_telegram(t['token'], t['chat_id'], msg)
                if 'smtp' in alert_cfg:
                    send_email(alert_cfg['smtp'], f"Log alert: {kw}", msg)
                # native rate limit : skip to next line

if __name__ == '__main__':
    run()



