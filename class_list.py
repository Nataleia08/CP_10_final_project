import re
import sys
import json
import copy
import shutil
from collections import UserDict
from datetime import datetime, date, timedelta


class Field():
    def __init__(self) -> None:
        pass


class Name(Field):
    def __init__(self) -> None:
        Field.__init__(self)
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if (new_value != None) and (new_value != ""):
            self.__value = new_value
        else:
            print("Enter value!")


class Phone(Field):
    def __init__(self) -> None:
        Field.__init__(self)
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        try:
            result = re.search(
                r"[+380]?[(]?[0-9]{2}[)]?[0-9]{3}[-]?[0-9]{1,2}[-]?[0-9]{2,3}\b", new_value).string
            if result != None:
                self.__value = str(result)
            else:
                print("This is not a phone!")
        except ValueError as e:
            print(e.error)


class Birthday(Field):
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if (type(new_value) == datetime) or (type(new_value) == date):
            self.__value = new_value
        elif type(new_value) == str:
            try:
                if "-" in new_value:
                    d_list = new_value.split("-")
                elif "/" in new_value:
                    d_list = new_value.split("/")
                elif "." in new_value:
                    d_list = new_value.split(".")
                if len(d_list[0]) == 4:
                    self.__value = datetime(
                        year=int(d_list[0]), month=int(d_list[1]), day=int(d_list[2]))
                else:
                    self.__value = datetime(
                        year=int(d_list[-1]), month=int(d_list[-2]), day=int(d_list[-3]))
            except:
                print("This is not a date! Date not save!")


class Record():
    def __init__(self, name: Name, phone, date: Birthday = None) -> None:
        self.name = name
        self.date = date
        self.phone = phone

    def add_phone(self, phone_new):
        self.phone.append(Phone(phone_new))

    def change_phone(self, phone_new):
        self.phone.extend(Phone(phone_new))

    def delete_phone(self, phone_new):
        try:
            self.phone.remove(Phone(phone_new))
        except:
            print("This phone not found!")

    def days_to_birthday(self):
        if self.date == None:
            print("Birthday not entering!")
            return None
        else:
            now_day = datetime.now().date()
            birthday_now = datetime(
                year=2023, month=self.date.value.month, day=self.date.value.day).date()
            days_count = birthday_now - now_day
            if days_count.days > 365:
                days_count = days_count - timedelta(days=365)
            if days_count.days < 0:
                days_count = days_count + timedelta(days=365)
            return days_count


class AddressBook(UserDict):
    def __init__(self) -> None:
        UserDict.__init__(self)
        # self.on_pages = 2
        self.number_record = 0
        self.current_page = 1
        self.numbers_record = 0

    def iterator(self, on_pages):
        result = []
        self.numbers_record = len(self.data)
        if (len(self.data) % on_pages) == 0:
            max_page = int(self.numbers_record/on_pages)
        else:
            max_page = int(self.numbers_record//on_pages + 1)
        try:
            for i, (key_name, val) in enumerate(self.data.items()):
                i += 1
                if (i <= self.current_page*on_pages) and (i > (self.current_page-1)*on_pages):
                    k = key_name.title()
                    result.append(k)
                    self.number_record += 1
                    if self.data[key_name].date.value != None:
                        d = str(self.data[key_name].date.value.date())
                        result.append(d)
                    phone_l = self.data[key_name].phone
                    for h in phone_l:
                        result.append(str(h.value))
                        result.append("\n")
                if (self.current_page*on_pages <= self.number_record) or (self.number_record == self.numbers_record):
                    if self.current_page < max_page:
                        self.current_page += 1
                    else:
                        self.current_page = 1
                    yield (" ".join(result))
                    result.clear()
            self.current_page = 1
            self.number_record = 0
        except Exception as e:
            print("Error!", e.args)

    def add_record(self, record: Record):
        """Функція додання запису"""

        key = str(record.name.value)
        if (key == "") or (len(record.phone) == 0):
            print("Give me name and phone please!")
            return None
        try:
            self.data[key] = record
            print("Contact save fine!")
        except Exception as e:
            print("Error!", e.args)

    def change_record(self, record: Record):
        """Функція зміни запису"""

        key = str(record.name.value)
        if (key == "") or (len(record.phone) == 0):
            print("Give me name and phone please!")
            return None
        try:
            self.data[key] = record
            print("Contact update fine!")
        except:
            print("There is no user with this name!")

    def search_phone(self, name: str) -> str:
        """Функція пошуку телефону за ім'ям"""

        if (name == ""):
            print("Give me name please!")
            return None
        try:
            result = []
            for p in self.data[name].phone:
                result.append(str(p.value))
            print(" ".join(result))
        except:
            print("There is no user with this name!")

    def show_all(self) -> str:
        """Функція відображення списку контактів"""
        try:
            result = []
            for key_name in self.data.keys():
                k = key_name.title()
                result.append(k)
                if self.data[key_name].date:
                    if self.data[key_name].date.value != None:
                        d = str(self.data[key_name].date.value.date())
                        result.append(d)
                phone_l = self.data[key_name].phone
                for i in phone_l:
                    result.append(str(i.value))
                result.append("\n")
            print(" ".join(result))
        except Exception as e:
            print("Error!", e.args)

    def search_record(self, name: str) -> Record:
        """Функція пошуку запису за ім'ям користувача"""

        for key_name in self.data.keys():
            if key_name == name:
                return self.data[key_name]

    def packaged_in_dict(self) -> list:
        """Функція перетворення адресної книги на список словників"""

        try:
            result = []
            y = 0
            phone_result = []
            for key_name in self.data.keys():
                result.append({})
                result[y]["name"] = key_name.title()
                if self.data[key_name].date:
                    if self.data[key_name].date.value != None:
                        d = str(self.data[key_name].date.value.date())
                        result[y]["birthday"] = d
                    else:
                        result[y]["birthday"] = "-"
                else:
                    result[y]["birthday"] = "-"
                phone_result.clear()
                for i in self.data[key_name].phone:
                    phone_result.append(str(i.value))
                result[y]["phone"] = copy.copy(phone_result)
                y += 1
            return result
        except Exception as e:
            print("Error!", e.args)

    def unpackaged_in_this_book(self, book: [dict]):
        """Функція перетворення словника на адресну книгу"""

        n = Name()
        p = []
        b = Birthday()
        p_i = Phone()
        for k in book:
            n.value = k["name"].lower()
            p.clear()
            for i in k["phone"]:
                p_i.value = copy.copy(i)
                p.append(copy.copy(p_i))
            if k["birthday"] != "-":
                b.value = copy.copy(k["birthday"])
                self.add_record(Record(n, copy.copy(p), copy.copy(b)))
            else:
                self.add_record(Record(n, copy.copy(p)))

    def command_search(self, text: str):
        """Функція пошуку запису в адресній книзі по введеному тексту"""

        try:
            result = []
            for key_name in self.data.keys():
                if (key_name.find(text) != -1):
                    result.append(key_name.title())
                    if self.data[key_name].date.value != None:
                        d = str(self.data[key_name].date.value.date())
                        result.append(d)
                    for i in self.data[key_name].phone:
                        result.append(str(i.value))
                    result.append("\n")
                else:
                    for i in self.data[key_name].phone:
                        if text in str(i.value):
                            result.append(key_name.title())
                            if self.data[key_name].date.value != None:
                                d = str(self.data[key_name].date.value.date())
                                result.append(d)
                            result.append(str(i.value))
                            result.append("\n")
            if len(result) == 0:
                print("Not found!")
            else:
                print(" ".join(result))
        except Exception as e:
            print("Error!", e.args)


class User():
    def __init__(self):
        pass

    def command_hello(self) -> None:
        """Функція привітання"""
        print("How can I help you?")

    def command_exit(self):
        """Функція виходу"""
        sys.exit("Good bye!")

    def command_save(self, book: AddressBook) -> None:
        """Функція збереження записів адресної книги до файлу"""

        with open("data.json", "w") as fh:
            json.dump(book.packaged_in_dict(), fh)

    def command_load(self) -> AddressBook:
        """Функція завантаження даних із файлу до адресної книги"""

        book = AddressBook()
        try:
            with open("data.json", "r") as fh:
                address_book_dict = json.load(fh)
                if address_book_dict:
                    book.unpackaged_in_this_book(address_book_dict)
            return book
        except:
            return book
