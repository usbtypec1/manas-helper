from dataclasses import dataclass
from datetime import datetime

from models.rating import Rating

__all__ = ('Application', 'ApplicationRow')


@dataclass(frozen=True, slots=True)
class Application:
    department_id: int
    applied_at: datetime
    applicant_id: str
    exams_score: float
    additional_score: float
    ratings: list[Rating]


@dataclass(frozen=True, slots=True)
class ApplicationRow:
    department_id: int
    applied_at: datetime
    applicant_id: str
    exams_score: float
    additional_score: float
    rating: int
