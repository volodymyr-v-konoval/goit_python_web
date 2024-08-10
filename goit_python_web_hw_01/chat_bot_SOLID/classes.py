from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime, date, timedelta
import re

class Field(ABC):
    '''
    It's the parrent class for fields with strings.
    '''
    @abstractmethod
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def validate(self):
        pass

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    '''
    It's a special class for a person's name in the phonebook.
    '''
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value:
            raise ValueError('Name cannot be empty.')


class Phone(Field):
    '''
    It's a special class, with validation,
    for phone numbers in the phonebook.
    '''

    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not (len(self.value) == 10 and self.value.isdigit()):
            raise ValueError('Phone number must be 10 digits')

class Record:
    '''
    It's a class to prepare and edit data in the phonebook.
    '''
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        '''
        The function adds the Phone object to the phonebook.
        '''
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        '''
        The function removes the phone object, with value
        equal to the phone argument, from the phonebook.
        '''
        for phone_object in self.phones:
            if phone_object.value == phone:
                self.phones.remove(phone_object)

    def edit_phone(self, old: str, new: str) -> None:
        '''
        The function replaces one phone object in the phonebook,
        to another, using other functions of the class.
        '''
        self.remove_phone(old)
        self.add_phone(new)

    def add_birthday(self, birthday:str) -> None:
        '''
        Adds a one's birthday.
        '''
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    '''
    It's a special custom dictionary to use it as a phonebook.
    '''

    def add_record(self, data: Record) -> None:
        '''
        Adds a apecial Record object as a note 
        in the phonebook dictionary.
        '''
        self.data[data.name.value] = data

    def find(self, name: str) -> Record | None:
        '''
        If founds key, equal to the name argunent, 
        returns the Record object, which is 
        the value in the phonebook dictionary. 
        Otherwise returns None.
        '''
        if name in self.data.keys():
            return self[name]
        return None
    
    def delete(self, name: str) -> None:
        '''
        The function removes the note from the phonebook
        with the key equal to the name argument.
        '''
        if name in self.data.keys:
            self.data.pop(name)

    def get_upcoming_birthdays(self, days=7) -> list:
        '''The function collects the birthdays for the next
        seven days, and returns them as a list.
        '''
        upcoming_birthdays = []
        today = date.today()
        self.days = days

        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday
        
        def date_to_string(date: datetime) -> str:
            return date.strftime("%Y.%m.%d")

        for user in self.data.keys():
            birthday_this_year = self[user].birthday.birthday_dt.replace(year=today.year).date()
            if birthday_this_year < today:
                birthday_this_year = self[user].birthday.birthday_dt.replace(year=today.year + 1)
            if 0 <= (birthday_this_year - today).days <= self.days:
                birthday_this_year = adjust_for_weekend(birthday_this_year)
                
                congratulation_date_str = date_to_string(birthday_this_year)
                upcoming_birthdays.append(f"{self[user].name.value}'s congratulation date is {congratulation_date_str}.")
        
        return upcoming_birthdays

    def __str__(self):
        dict_to_string = ''
        for rec in self.values():
            dict_to_string += (f"Contact name: {rec.name.value}, phones: {'; '.join(p.value for p in rec.phones)}\n")       
        return dict_to_string.strip()

class Birthday(Field):
    '''
    The special class to validate, save and operate birthday dates.
    '''
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        try:
            shablon = r'[0-3]\d.[0-1]\d.\d{4}'
            birthday_str = (re.search(shablon, self.value)).group(0)
            birthday_dt = datetime.strptime(birthday_str, '%d.%m.%Y')
            self.birthday_dt = birthday_dt
            self.value = birthday_str
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        except AttributeError:
            raise AttributeError('Invalid date format. Use DD.MM.YYYY')
 
if __name__ == '__main__':

    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)