from repositories import DepartmentRepository
from services.manas import get_departments

__all__ = ('init_departments',)


def init_departments(
        department_repository: DepartmentRepository,
) -> None:
    departments = get_departments()

    excluded_departments = {
        'Живопись (Изобразительное искусство)',
        'Графика (Изобразительное искусство)',
        'Театральное искусство',
        'Музыкальное искусство',
        'Физическая культура',
        'Подготовка тренеров',
    }

    for department in departments:

        if department.name in excluded_departments:
            continue

        department_repository.create(department.id, department.name)
