# -*- coding: utf-8 -*-

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


@register.filter(is_safe=True, needs_autoescape=True)
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
    return mark_safe(
        re.sub(r'(?m)(?P<chord>\b[A-H]b?#?m?[0-9]?[0-9]?(sus[0-9])?(?=\s|\b|$))',

               r'<span class="chord chords_collapse">\g<chord></span>', esc(value)))


# chordify.needs_autoescape = False
# register.filter(chordify)

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def add_spans_to_text(value, autoescape=False):
    """
    Converts all newlines in a piece of plain text to HTML line breaks
    (``<br />``).
    """
    lines = value.split('<br />')
    spanned_lines = []
    for s in lines:
        if 'chords_collapse' in s:
            spanned_lines += ["<span class='chords_line_collapse'>" + s + '<br />' + "</span>"]
        else:
            spanned_lines += ["<span class='text_collapse'>" + s + '<br />' + "</span>"]
    value = ''.join(spanned_lines)
    return value


# add_spans_to_text.needs_autoescape = False
# register.filter(add_spans_to_text)


@stringfilter
def color_song_keywords(value, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    keywords = ['Припев', 'Куплет',
                'Интро', 'Вступление', 'Кода', 'Проигрыш',
                'Chorus', 'Intro', 'Coda', 'Outro']
    s = esc(value)
    for k in keywords:
        s = re.sub(r'\b(?P<keyword>' + k + r'\b[.: \n])', r'<span class="song_keyword">\g<keyword></span>', s)

    return mark_safe(s)


color_song_keywords.needs_autoescape = True
register.filter(color_song_keywords)


@stringfilter
def turn_tabs_to_spaces(value, autoescape=None):
    return re.sub(r'\t', r' ', value)


turn_tabs_to_spaces.needs_autoescape = False
register.filter(turn_tabs_to_spaces)
