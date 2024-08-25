class TestingRoute:
    def __init__(self, base_url, test_url):
        self.base_url = base_url
        self.test_url = test_url

    def get_absolute_url(self):
        return f'{self.base_url}{self.test_url}'


class BaseLocator:
    base_url = 'http://127.0.0.1:8000/'


class UserCreateLocator:
    test_url = 'auth'


class ItemCreateLocator:
    test_url = 'items/create'


class ItemGetLocator:
    test_url = 'items/'
