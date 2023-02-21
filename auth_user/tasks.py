from asyncio import sleep as aiosleep
from time import sleep

from django.core.mail import send_mail

from MainApp.celery import app
from MainApp.settings import EMAIL_HOST_USER


@app.task
def send_email_thread():
    print(f"GO!!!!")
    text_message = "HELLO FROM DJANGO !!! ))))"
    email = "frommydjango@gmail.com"
    send_mail('djangoProjectCBS',
              text_message,
              EMAIL_HOST_USER, [email],
              fail_silently=True,
              )
    return 1010
