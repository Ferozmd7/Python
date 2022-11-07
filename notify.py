import smtplib, ssl ,csv


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
message = MIMEMultipart()

port = 587  # For starttls
body = "This message is regarding latest 3rd party jars available"
smtp_server = "smtp.office365.com"
sender_email = "mohammad.feroz@mobileum.com"
receiver_email = "mahesh.akuthota@mobileum.com"
password = "phdhwvpkdjhvjwfg"
subject = """\
Subject: Hi mahesh, """


message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

message.attach(MIMEText(body, "plain"))
filename = "output.txt"  # In same directory as script
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

message.attach(part)
text = message.as_string()
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

