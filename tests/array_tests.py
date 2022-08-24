from easytest.expectation import expect


def test_array_contains_element_basic():
    expect([1, 2, 3]).contains(2)
