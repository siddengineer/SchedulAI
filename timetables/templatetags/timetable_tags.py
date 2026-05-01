# from django import template
# register = template.Library()

# @register.filter
# def get_item(dictionary, key):
#     if isinstance(dictionary, dict):
#         return dictionary.get(key)
#     return None

# @register.filter
# def split(value, sep=','):
#     return value.split(sep)



# ============================================================
# timetables/templatetags/timetable_tags.py
#
# ALSO create an empty file:
#   timetables/templatetags/__init__.py
# ============================================================

from django import template

register = template.Library()


@register.filter(name='get_div')
def get_div(slot_map, div_id):
    """slot_map|get_div:div.pk  →  {day: {period_id: slot}}"""
    if not slot_map:
        return {}
    return slot_map.get(div_id, {})


@register.filter(name='get_day')
def get_day(day_map, day):
    """day_map|get_day:day_num  →  {period_id: slot}"""
    if not day_map:
        return {}
    return day_map.get(day, {})


@register.filter(name='get_period')
def get_period(period_map, period_id):
    """period_map|get_period:period.pk  →  slot or None"""
    if not period_map:
        return None
    return period_map.get(period_id)


@register.filter(name='get_item')
def get_item(d, key):
    if not d:
        return None
    return d.get(key)