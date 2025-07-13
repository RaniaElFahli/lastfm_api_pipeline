from prefect_email import EmailServerCredentials
from dotenv import load_dotenv
import os

load_dotenv()

credentials = EmailServerCredentials(
    username=os.getenv("EMAIL"),
    password=os.getenv("EMAIL_PASSWORD"),
    smtp_server="smtp.gmail.com"
)

credentials.save("email-credentials")

