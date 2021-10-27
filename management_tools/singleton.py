from abc import ABC


class Singleton(ABC):
    singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.singleton_instance is None:
            cls.singleton_instance = super().__new__(cls, *args, **kwargs)

        return cls.singleton_instance
