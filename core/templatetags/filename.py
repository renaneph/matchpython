import os

from django import template
from django.db.models.fields.files import FieldFile

register = template.Library()


@register.filter
def filename(value: FieldFile) -> str:
    """
    Receive the uploaded file and return just the name from file
    Example:
        input: uploads/resume/Match_List_zeUWq8h.pdf
        output: Match_List_zeUWq8h.pdf
    """
    return os.path.basename(value.file.name)
