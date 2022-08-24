from __future__ import annotations

import operator


class FailedExpectationError(AssertionError):
    def __init__(self, message):
        self.message = message


class Expectation:
    def __init__(self, value):
        self.value = value

    def _assert(self, message: str, op: operator, expected) -> Expectation:
        if not op(self.value, expected):
            raise FailedExpectationError(
                f"expected "
                f"""{'"%s"' % self.value if type(self.value) is str else self.value} {message} """
                f"""{'"%s"' % expected if type(expected) is str else expected}"""
            )
        return Expectation(True)

    def equals(self, expected):
        return self._assert("to equal", operator.eq, expected)

    def not_to_equal(self, expected):
        return self._assert("to not equal", operator.ne, expected)

    def contains(self, element):
        return self._assert("to include", operator.contains, element)


def expect(value):
    return Expectation(value=value)


def before_all(func):
    def wrapper():
        func()
    return wrapper
