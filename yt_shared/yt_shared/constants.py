import enum


@enum.unique
class ChoiceEnum(enum.Enum):
    @classmethod
    def choices(cls) -> tuple[str, ...]:
        return tuple(x.value for x in cls)


class TaskStatus(str, ChoiceEnum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    FAILED = 'FAILED'
    DONE = 'DONE'


class TaskSource(str, ChoiceEnum):
    API = 'API'
    BOT = 'BOT'
