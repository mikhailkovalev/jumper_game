from clashers import StaticClasher, LiftClasher


class PlatformTypesEnum:

    STATIC = 1
    LIFT = 2

    keys = {
        STATIC,
        LIFT,
    }

    verbose_names = {
        STATIC: 'static',
        LIFT: 'lift',
    }

    clashers = {
        STATIC: StaticClasher(),
        LIFT: LiftClasher(),
    }

    colors = {
        LIFT: (1, 112, 192),
    }

    @classmethod
    def get_name(cls, type):
        return cls.verbose_names.get(type, 'invalid type')
