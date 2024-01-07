from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = self.is_valid(value)

    def is_valid(self, value):
        return value 

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def is_valid(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Please enter a 10-digit number.")
        return value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = self.is_valid(new_value)

class Birthday(Field):

    def is_valid(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Please use DD-MM-YYYY.")
        return value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = self.is_valid(new_value)

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj) 

    def remove_phone(self, phone):
        drop_contact = self.find_phone(phone)
        if drop_contact:
            self.phones.remove(drop_contact)

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError(f"Phone {old_phone} not found in the record.")
            
    def edit_name(self, name):
        self.name = Name(name)
        
    def edit_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        

    def find_phone(self, phone):
        try:
            for contact in self.phones:
                if contact.value == phone:
                    return contact

            raise ValueError(f"Phone {phone} not found in the record.")
        except ValueError:
            pass

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            birthday_date = datetime.strptime(self.birthday.value, "%d-%m-%Y")
            if today > birthday_date:
                next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day)
            else:
                next_birthday = datetime(today.year, birthday_date.month, birthday_date.day)

            return (next_birthday - today).days
        
        return None

    def __str__(self):
        birthday_str = f', birthday: {self.birthday.value}' if self.birthday else ''
        return f"Contact name: {self.name.value}, {birthday_str} phones: {'; '.join(contact.value for contact in self.phones)}"

class AddressBook(UserDict):
    
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, query):
        results = []
        for contact in self.data.values():
            for phone in contact.phones:
                if re.search(query, phone.value, re.IGNORECASE):
                    results.append(contact)
                    
            if re.search(query, contact.name.value, re.IGNORECASE):
                results.append(contact)

        return list(set(results))

    def delete(self, name):
        try:
            if name in self.data:
                del self.data[name]
            else:
                raise KeyError(f"Record with name {name} not found in the address book.")
        except KeyError:
            pass

    def iterator(self, n):
        for i in range(0, len(self.data), n):
            yield list(self.data.values())[i:i + n]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def read_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)