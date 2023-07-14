from dataclasses import dataclass
from datetime import datetime

from models.departments import Department
from models.rating import Rating

__all__ = (
    'Application',
    'ApplicationRow',
    'ApplicationStatistics',
    'DepartmentRatings',
    'ApplicationsCountByDepartment',
)


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
    applied_at: datetime
    applicant_id: str
    exams_score: float
    additional_score: float
    rating: int


@dataclass(frozen=True, slots=True)
class DepartmentRatings:
    department: Department
    application_rows: list[ApplicationRow]


@dataclass(frozen=True, slots=True)
class ApplicationStatistics:
    department_name: str
    min_exams_score: float
    max_exams_score: float
    average_exams_score: float


@dataclass(frozen=True, slots=True)
class ApplicationsCountByDepartment:
    department_name: str
    count: int
    quota: int
