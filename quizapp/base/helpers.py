import uuid
import smtplib, ssl
import environ

env = environ.Env()
environ.Env.read_env()

def send_forgot_password_mail(user_obj, encode_pk):
    port = env("EMAIL_PORT")
    smtp_server = env("SMTP_SERVER")
    receiver_email = user_obj.email
    token = str(uuid.uuid4())
    USERNAME = env("EMAIL_USERNAME")
    PASSWORD = env("EMAIL_PASSWORD")
    TEXT = f""" Hi, click on the link to reset password 
    http://127.0.0.1:8000/reset/{user_obj.id}/{encode_pk[0]}/"""
    SUBJECT = "Reset your Password"
    message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, receiver_email, message)
    return True

def send_quiz_email(user_obj):
    port = env("EMAIL_PORT")
    smtp_server = env("SMTP_SERVER")
    USERNAME = env("EMAIL_USERNAME")
    PASSWORD = env("EMAIL_PASSWORD")
    TEXT = f""" You have an assigned Quiz for you.  
    Kindly attempt the quiz before time."""
    SUBJECT = "Unattempted Quiz"
    message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
    context = ssl.create_default_context()

    # for obj in user_obj:
    receiver_email = user_obj.email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, receiver_email, message)
    return True

