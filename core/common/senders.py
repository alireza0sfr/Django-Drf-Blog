from django.core.mail import send_mass_mail
from django.conf import settings
from mail_templated import EmailMessage

from common.threading import Threading


class Sender:

    from_email = settings.EMAIL_FROM

    @staticmethod
    def send_email(template, details, toEmail):
        message = EmailMessage(template, details, Sender.from_email, to=[toEmail])

        Threading(message.send).start()
        return {'detail': 'email sent!'}

    @staticmethod
    def send_mass_mail():
        message1 = (
            "Subject here",
            "Here is the message",
            "from@example.com",
            ["first@example.com", "other@example.com"],
        )

        message2 = (
            "Another Subject",
            "Here is another message",
            "from@example.com",
            ["second@test.com"],
        )
        send_mass_mail((message1, message2), fail_silently=False)
        return {'detail': 'emails sent!'}
