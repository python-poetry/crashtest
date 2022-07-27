from __future__ import annotations

from crashtest.contracts.base_solution import BaseSolution
from crashtest.contracts.has_solutions_for_exception import HasSolutionsForException
from crashtest.contracts.provides_solution import ProvidesSolution
from crashtest.contracts.solution import Solution
from crashtest.solution_providers.solution_provider_repository import (
    SolutionProviderRepository,
)


class ExceptionSolutionProvider(HasSolutionsForException):
    def can_solve(self, exception: Exception) -> bool:
        return isinstance(exception, ExceptionProvidingException)

    def get_solutions(self, exception: Exception) -> list[Solution]:
        return [
            BaseSolution("An exception solution", "An exception solution description")
        ]


class ExceptionProvidingException(Exception, ProvidesSolution):
    @property
    def solution(self) -> Solution:
        solution = BaseSolution("A simple solution", "A simple solution description")
        solution.documentation_links.append("https://example.com")

        return solution


class ExceptionWhichIsSolution(Exception, Solution):
    @property
    def solution_title(self) -> str:
        return "A solution"

    @property
    def solution_description(self) -> str:
        return "A solution description"

    @property
    def documentation_links(self) -> list[str]:
        return ["https://foo.bar"]


def test_it_has_no_provider_by_default() -> None:
    repository = SolutionProviderRepository()

    assert len(repository._solution_providers) == 0


def test_providers_can_be_passed_to_constructor() -> None:
    repository = SolutionProviderRepository()

    assert len(repository._solution_providers) == 0


def test_it_can_find_solutions() -> None:
    repository = SolutionProviderRepository()

    repository.register_solution_provider(ExceptionSolutionProvider)

    solutions = repository.get_solutions_for_exception(ExceptionProvidingException())

    assert len(solutions) == 2
    solution1 = solutions[0]
    solution2 = solutions[1]
    assert solution1.solution_title == "A simple solution"
    assert solution2.solution_title == "An exception solution"
    assert solution1.solution_description == "A simple solution description"
    assert solution2.solution_description == "An exception solution description"
    assert solution1.documentation_links == ["https://example.com"]
    assert len(solution2.documentation_links) == 0

    solutions = repository.get_solutions_for_exception(ExceptionWhichIsSolution())

    assert len(solutions) == 1
    solution1 = solutions[0]
    assert solution1.solution_title == "A solution"
    assert solution1.solution_description == "A solution description"
    assert solution1.documentation_links == ["https://foo.bar"]
