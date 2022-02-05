from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def room_status_for_date(context, date_obj, room_obj):
    date_key = date_obj.strftime("%m-%d-%Y")
    room_dict = context["room_schedule"]
    room_key = str(room_obj)

    # TODO: If we have a bunch of rooms this would work better
    # we used the room key as a key of another dictionary under the date
    if len(room_dict[date_key]):
        for room in room_dict[date_key]:
            if room_key == str(room):
                return mark_safe("<td class='room-booked'>*</td>")
    return mark_safe(
        "<td data-cell-date='{}' data-room-key='{}' class='room-vacant'>-</td>".format(
            date_key, room_key
        )
    )
