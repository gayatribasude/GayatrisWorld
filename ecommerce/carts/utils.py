from access_tokens import tokens
from django.core.mail import send_mail
from django.http import Http404


def send_review_mail(self):
    token = tokens.generate(scope=(), key="some value", salt="None")
    message = render_to_string('email_to.html', {'token': token})
    msg = EmailMessage('Subject here',
                       'Here is the message.',
                       'from@example.com',
                       ['to@example.com'],
                       headers=Headers,
                       cc=[cc @ example.com]
                       )
    msg.content_subtype = "html"
    msg.send()

def validate_token(function):
    def wrap(request, *args, **kwargs):
        token = kwargs.get('token')
        case_id = kwargs.get('case_id')
        validate = tokens.validate(token, scope=(), key=case_id, salt=settings.TOKEN_SALT, max_age=None)
        if validate:
            return function(request, *args, **kwargs)
        else:
            raise Http404
        return wrap
