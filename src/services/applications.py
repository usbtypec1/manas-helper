import statistics
from collections import defaultdict
from collections.abc import Iterable
from typing import TypeVar, Protocol

import models


def group_by_department_name(
        items: Iterable[tuple[str, float]],
) -> defaultdict[str, list[float]]:
    department_name_to_scores = defaultdict(list)
    for department_name, score in items:
        department_name_to_scores[department_name].append(score)
    return department_name_to_scores


def compute_applications_statistics(
        department_name_to_exam_scores: dict[str, Iterable[float]],
) -> list[models.ApplicationStatistics]:
    return [
        models.ApplicationStatistics(
            department_name=department_name,
            average_exams_score=statistics.mean(exam_scores),
            min_exams_score=min(exam_scores),
            max_exams_score=max(exam_scores),
        ) for department_name, exam_scores in
        department_name_to_exam_scores.items()
    ]
