from django.db.models import Func


class AtTimeZone(Func):
    function = 'AT TIME ZONE'
    template = "%(expressions)s %(function)s '%(timezone)s'"
