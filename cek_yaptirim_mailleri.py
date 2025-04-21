import imaplib
import email
from email.header import decode_header
import pandas as pd

# Giriş bilgileri
username = "uluslararasiyaptirim@gmail.com"
password = "aekj iuyt wkgg jtue"  # Gerçek app password'ü

# Gmail'e bağlan
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)

# Gelen kutusunu seç
imap.select("inbox")

# Tüm mailleri al
status, messages = imap.search(None, 'ALL')
mail_ids = messages[0].split()

data = []

# SON 10 MAIL
for i in mail_ids[-10:]:
    res, msg = imap.fetch(i, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
            date = msg["Date"]
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            data.append([date, subject, body])

# CSV'ye kaydet
df = pd.DataFrame(data, columns=["date", "subject", "body"])
df.to_csv("yaptirim_mailleri.csv", index=False, encoding="utf-8")

# Oturumu kapat
imap.logout()

print("✅ Mail verileri 'yaptirim_mailleri.csv' dosyasına kaydedildi.")
