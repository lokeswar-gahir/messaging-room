from django import template
from main.utils import animal_from_uuid

register = template.Library()

@register.filter
def get_animal_from_uuid(uuid_value):
    # h = hashlib.sha256(str(uuid_value).encode()).hexdigest()
    # return ANIMALS[int(h, 16) % len(ANIMALS)]
    return animal_from_uuid(uuid_value)