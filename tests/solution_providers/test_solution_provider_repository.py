from typing import List

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

    def get_solutions(self, exception: Exception) -> List[Solution]:
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
    def documentation_links(self) -> List[str]:
        return ["https://foo.bar"]


def test_it_has_no_provider_by_default():
    repository = SolutionProviderRepository()

    assert 0 == len(repository._solution_providers)


def test_providers_can_be_passed_to_constructor():
    repository = SolutionProviderRepository()

    assert 0 == len(repository._solution_providers)


def test_it_can_find_solutions():
    repository = SolutionProviderRepository()

    repository.register_solution_provider(ExceptionSolutionProvider)

    solutions = repository.get_solutions_for_exception(ExceptionProvidingException())

    assert 2 == len(solutions)
    solution1 = solutions[0]
    solution2 = solutions[1]
    assert "A simple solution" == solution1.solution_title
    assert "An exception solution" == solution2.solution_title
    assert "A simple solution description" == solution1.solution_description
    assert "An exception solution description" == solution2.solution_description
    assert ["https://example.com"] == solution1.documentation_links
    assert 0 == len(solution2.documentation_links)

    solutions = repository.get_solutions_for_exception(ExceptionWhichIsSolution())

    assert 1 == len(solutions)
    solution1 = solutions[0]
    assert "A solution" == solution1.solution_title
    assert "A solution description" == solution1.solution_description
    assert ["https://foo.bar"] == solution1.documentation_links
