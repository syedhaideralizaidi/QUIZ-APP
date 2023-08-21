from django.core.mail import send_mail
import uuid
import smtplib, ssl


def send_forgot_password_mail(user_obj, encode_pk):
    port = 465  # ToDo: this should be set in the setting files, and imported from settings
    smtp_server = "smtp.gmail.com"  # ToDo: this should be set in the setting files, and imported from settings
    receiver_email = user_obj.email
    token = str(uuid.uuid4())
    USERNAME = "haider.zaidiy@gmail.com"    # ToDo: this should be set in the setting files, and imported from settings
    PASSWORD = "arlgrijgssodacgi"   # ToDo: this should be set in the setting files, and imported from settings
    TEXT = f""" Hi, click on the link to reset password 
    http://127.0.0.1:8000/reset_pw/{user_obj.id}/{encode_pk[0]}/"""
    SUBJECT = "Reset your Password"
    message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, receiver_email, message)
    return True


def send_quiz_email(user_obj):
    port = 465  # ToDo: this should be set in the setting files, and imported from settings
    smtp_server = "smtp.gmail.com"  # ToDo: this should be set in the setting files, and imported from settings
    USERNAME = "haider.zaidiy@gmail.com"    # ToDo: this should be set in the setting files, and imported from settings
    PASSWORD = "arlgrijgssodacgi"   # ToDo: this should be set in the setting files, and imported from settings
    TEXT = f""" You have an assigned Quiz for you.  
    Kindly attempt the quiz before time."""
    SUBJECT = "Unattempted Quiz"
    message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
    context = ssl.create_default_context()

    receiver_email = user_obj.email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, receiver_email, message)
    return True
