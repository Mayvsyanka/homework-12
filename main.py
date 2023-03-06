from collections import UserDict
from datetime import datetime
import re
import json


class Error(Exception):
    pass


class Field:

    def __init__(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):

    @staticmethod
    def checking(num):
        num = re.sub(r"[\-\(\)\+\ a-zA-Zа-яА-я]", "", num)
        try:
            if len(num) == 12 or len(num) == 10 or len(num) == 9:
                pass
            else:
                num = False
                raise Error
        except Error:
            print("Wrong number. Try again")

        if num:
            return num
        else:
            return ""

    def __init__(self, value) -> None:
        self._value = Phone.checking(value)

    @Field.value.setter
    def value(self, value):
        self._value = Phone.checking(value)


class Birthday(Field):
    pass


class Record:

    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        self.phones.append(phone)
        self.birthday = birthday
        self.phone = phone

    def add_contact(self, phone):
        self.phones.append(phone)

    def change_contact(self, old, new):
        old = Phone(old)
        new = Phone(new)

        for phone in self.phones:
            if phone == old:
                self.phones.remove(old)
                self.phones.append(new)

    def remove_contact(self, phone):
        phone = Phone(phone)
        for value in self.phones:
            if value == phone:
                a = self.phones.pop(value)

    def days_to_birthday(self):
        self.b_day = datetime.strptime(
            str(self.birthday.value), "%Y.%m.%d")
        self.current_birthday = datetime(
            year=2023, month=self.b_day.month, day=self.b_day.day)
        self.today = datetime.now()
        self.current_today = self.today.date()
        self.current_birthday_date = self.current_birthday.date()
        self.different = self.current_birthday_date - self.current_today
        t = str(self.different).split(" ")
        if int(t[0]) < 0:
            self.current = datetime(
                year=2024, month=self.b_day.month, day=self.b_day.day).date()
            self.different = self.current - self.current_today
        hello = str(self.different).split(" ")
        return (f"Days to birthday: {hello[0]}")

    def __repr__(self):
        return f"{self.phone}, {self.birthday}"


class AdressBook(UserDict, Record):

    def add_record(self, rec):
        self.data[rec.name.value] = rec
        return self.data

    def generator(self):
        for name, information in self.data.items():
            yield (f"{name} {information}")

    def iterator(self, n):
        n = n
        iterate = self.generator()
        try:
            if n > len(self.data):
                raise Error
        except:
            print(
                (f"Too large value\nTry again"))
        while n > 0:
            try:
                print(next(iterate))
                n -= 1
            except StopIteration:
                return ""
        return ("Ready")

    def find(self, search):
        for key, value in self.data.items():
            if search in key or search in str(value):
                return (f"Match for \"{search}\" found: {key}: {value}")
            else:
                return (f"No match found")

    def write_contacts_to_file(self, filename="phone_book.json"):
        with open(filename, "w") as fh:
            res = []
            for name, info in self.data.items():
                res.append({"Name": name.title(), "Info": str(info)})
            json.dump(res, fh, indent=4, ensure_ascii=False)
            return (f"Information has been saved successfully to {filename}")


def read_contacts_from_file(filename="phone_book.json"):
    with open(filename, "r") as file:
        unpacked = json.load(file)
        return (unpacked)
