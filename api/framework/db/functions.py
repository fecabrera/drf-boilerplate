from django.db.models import Func


class BinaryFunc(Func):
    template = '%(lhs)s %(function)s %(rhs)s'
    arity = 2

    def as_sql(self, compiler, connection, function=None, template=None, **extra_context):
        assert getattr(self, 'function', None) or function is not None, (
            "%s should either include a `function` attribute, "
            "or pass it as an argument when calling `as_sql()`."
            % self.__class__.__name__
        )

        left_expr, right_expr = self.get_source_expressions()

        lhs, lhs_params = compiler.compile(left_expr)
        rhs, rhs_params = compiler.compile(right_expr)

        template = template or self.template
        function = function or self.function

        data = {'function': function, 'lhs': lhs, 'rhs': rhs}
        params = lhs_params + rhs_params
        return template % data, params


class AtTimeZone(BinaryFunc):
    function = 'AT TIME ZONE'


class Timezone(Func):
    function = 'TIMEZONE'
