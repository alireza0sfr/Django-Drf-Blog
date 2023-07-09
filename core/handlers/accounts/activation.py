from rest_framework.response import Response

from handlers.accounts.token import generate_tokens_for_user
from common.senders import Sender

class Activation:
    def activate_with_email(self, user):
      token = generate_tokens_for_user(user)

      return Response(Sender.send_email(template='email/activation', details={'token': token.get('access_token')}, toEmail=user.email))