from dataclasses import dataclass
from datetime import datetime

__all__ = ('Rating',)


@dataclass(frozen=True, slots=True)
class Rating:
    value: int
    recorded_at: datetime
