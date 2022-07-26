from __future__ import annotations

from .solution import Solution


class HasSolutionsForException:
    def can_solve(self, exception: Exception) -> bool:
        raise NotImplementedError()

    def get_solutions(self, exception: Exception) -> list[Solution]:
        raise NotImplementedError()
