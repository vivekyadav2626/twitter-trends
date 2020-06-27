from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    return d[key]


@register.filter
def timedeltainmins(d, key):
    output = ""
    minutes = (d[key].seconds//60) % 60
    if minutes:
        output += str(minutes)
    hours = d[key].seconds//3600
    if hours:
        if hours == 1:
            hrstring = " hour "
        else:
            hrstring = " hours "

        if minutes == 1:
            mnstring = " minute ago"
        else:
            mnstring = " minutes ago"
        output = str(hours) + hrstring + str(minutes) + mnstring
    else:
        if minutes == 1:
            mnstring = " minute ago"
        else:
            mnstring = " minutes ago"
        output += mnstring
    return output


@register.filter
def countcleanup(count):
    magnitude = 0
    if not count:
        return ""
    while abs(count) >= 1000:
        magnitude += 1
        count /= 1000.0
    return '%.2f%s' % (count, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
