from collections import UserList
from dataclasses import dataclass


class MagicList(UserList):
    def __init__(self, cls_type: callable = None, *args, **kwargs):

        # Make sure that cls_type is callable (only if given).
        if cls_type is not None and not callable(cls_type):
            raise TypeError(f"'{cls_type}' is not callable")

        # Saves a list in self.data
        super().__init__(*args, **kwargs)

        self.default_class = cls_type

    def __setitem__(self, index, value):
        # If the index is the first uninitialized index, it needs to be created
        if index == len(self.data):
            self.append(value)
        else:
            super().__setitem__(index, value)

    def __getitem__(self, index):
        # If the index is the first uninitialized index
        # and a default constructor was defined,
        # initialize it with the default constructor
        if index == len(self.data) and self.default_class is not None:
            self.append(self.default_class())

        return super().__getitem__(index)


if __name__ == '__main__':
    a = MagicList()
    a[0] = 5

    @dataclass
    class Person:
        age: int = 1

    a = MagicList(cls_type=Person)
    a[0].age = 5

    a = MagicList(cls_type=dict)
    a[0]['test'] = 5
