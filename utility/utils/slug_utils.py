from django.utils.crypto import get_random_string
from django.utils.text import slugify


def generate_unique_slug(slug_content, instance,length=5):
    slug = slugify(slug_content)
    KClass = instance.__class__
    while KClass.objects.filter(slug=slug).exists():
        slug = slug + "-" + get_random_string(length=length)
    return slug


def generate_unique_username(content, model_name,length=5):
    username = slugify(content)
    while model_name.objects.filter(username=username).exists():
        username = username + get_random_string(length=length if len(username)>=4 else 4)
    return username

