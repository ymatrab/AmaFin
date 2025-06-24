from django import template

register = template.Library()

@register.filter
def after_dash(value):
    """Returns the part after the dash."""
    value=str(value)
    if value and ' - ' in value:
        return value.split(' - ')[-1]
    return value

@register.filter
def accounting_format(value):
    try:
        value = float(value)
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")
    except (ValueError, TypeError):
        return value
    


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

