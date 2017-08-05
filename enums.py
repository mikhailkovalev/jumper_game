from clashers import StaticClasher


class PlatformTypesEnum:

    STATIC = 1

    verbose_names = {
        STATIC: 'static',
    }

    clashers = {
        STATIC: StaticClasher(),
    }

    @classmethod
    def get_name(cls, type):
        return cls.verbose_names.get(type, 'invalid type')
