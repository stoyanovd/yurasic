from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = Library()


@stringfilter
def spacify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(re.sub('\s', '&' + 'nbsp;', esc(value)))


spacify.needs_autoescape = True
register.filter(spacify)


@stringfilter
def chordify(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    # chords = [chr(ord('A') + c) for c in range(8)]
    # chords += map(lambda x: x + 'm', chords)
    # s = esc(value)
    # for c in chords:
    #     s = re.sub('\b' + c + '\b', '<span class="chord">' + c + "</span>", s)
    #     s = re.sub('\b' + c + '\b', '<span class="chord">' + c + "</span>", s)
    # return mark_safe(s)
    return mark_safe(re.sub(r'\b(?P<chord>[A-H]m?)\b', r'<span class="chord">\g<chord></span>', esc(value)))



chordify.needs_autoescape = True
register.filter(chordify)
