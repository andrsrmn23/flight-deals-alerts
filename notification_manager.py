from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
import os
load_dotenv()
class NotificationManager:
    def __init__(self):
        self.sid = os.environ.get('TWILIO_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.from_number = os.environ.get('TWILIO_VIRTUAL_NUMBER')
        self.to_number = os.environ.get('TWILIO_VERIFIED_NUMBER')

        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]


    def send_message(self, message):
        client = Client(self.sid, self.auth_token)
        message = client.messages.create(
            from_=self.from_number,
            body=message,
            to=self.to_number,
        )

    def send_emails(self, emails, message):
        with smtplib.SMTP(self.smtp_address, 587) as connection:
            connection.starttls()
            connection.login(self.email, self.email_password)

            for email in emails:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}"
                )
