from django import template
from django.forms import CheckboxInput, Select

register = template.Library()


@register.filter
def add_class(field, css):
    widget = field.field.widget
    if isinstance(widget, CheckboxInput):
        css_class = "form-check-input"
    elif isinstance(widget, Select):
        css_class = "form-select"
    else:
        css_class = css
    return field.as_widget(attrs={**widget.attrs, "class": css_class})


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)
