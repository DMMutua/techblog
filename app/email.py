from flask_mail import Message
from app import mail


def send_email(subject, sender, recepients,
               text_body, html_body):
    """An Email Sending Wrapper Function"""
    msg = Message(subject, sender=sender,
                  recepients=recepients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)