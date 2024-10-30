from django import template

register = template.Library()


# To make pagination work
@register.simple_tag
def filtered_url(**kwargs):
    """This tag returns a querystring for paginating on the filtered items"""
    url = ''
    for key, value in kwargs.items():
        if value:
            url += f'&{key}={value}'
    return url
