from dataclasses import dataclass

__all__ = ('Department',)


@dataclass(frozen=True, slots=True)
class Department:
    id: int
    name: str
