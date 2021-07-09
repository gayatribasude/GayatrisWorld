import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    klass = instance.__class__
    qs_exists =klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randomstring}".format(slug=slug,randomstring=random_string_generator(size=4))
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip
