from sqlalchemy.ext.hybrid import hybrid_property

_missing = object()


class cached_hybrid_property(hybrid_property):
    def __get__(self, instance, owner):
        if instance is None:
            return self.expr(owner)
        else:
            name = self.fget.__name__
            value = instance.__dict__.get(name, _missing)
            if value is _missing:
                value = self.fget(instance)
                instance.__dict__[name] = value
            return value
