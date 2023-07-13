from dataclasses import dataclass

__all__ = ('Department', 'DepartmentIDAndName')


@dataclass(frozen=True, slots=True)
class DepartmentIDAndName:
    id: int
    name: str


@dataclass(frozen=True, slots=True)
class Department(DepartmentIDAndName):
    quota: int
