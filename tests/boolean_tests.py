from easytest.expectation import expect


def test_success():
    expect(True).equals(True)


def test_not_equal_success():
    expect(True).not_to_equal(False)
