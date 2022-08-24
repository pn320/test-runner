from dataclasses import dataclass
import datetime

from easytest.expectation import before_all, expect 


@dataclass
class User:
    email: str = ''
    last_login: datetime.datetime = datetime.datetime.now()
    password: str = ''

    def update(self, **kwargs):
        for attr, val in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, val)
        return self


@before_all
def create_user():
    pass


def test_user_created_correctly():
    user = User(email="tom@example.com")
    expect(user.email).equals('tom@example.com')
    expect(user.last_login).equals(datetime.datetime(2022, 7, 15, 10, 32, 14))


def test_update_user():
    user = User(email="tom@example.com")
    expect(user.update(email='tommy@example.com').email).equals('tommy@example.com')
