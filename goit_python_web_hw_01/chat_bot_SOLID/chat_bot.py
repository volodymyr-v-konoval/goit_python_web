from pprint import pprint
import pickle

from classes import AddressBook, Record
from decorators import input_error
from save import save_data, load_data


def parse_input(income: str) -> tuple:
    """I struct the input to use it in the modul's functions!"""
    command = income.split(' ')[0]
    args = income.split(' ')[1:]
    return command, args


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """I add new contacts to the phone-book."""
    name, phone, *_ = args
    record = book.find(name)
    message = 'Contact updated.'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added.'
    if phone:
        record.add_phone(phone)
    return message

  
@input_error    
def change_contact(args: list, book: AddressBook) -> str:
    """I change a contact in the phone-book."""
    name, new_phone, old_phone, *_ = args
    record = book.find(name)
    record.remove_phone(old_phone)
    record.add_phone(new_phone)
    message = 'Contact changed.'
    return message


@input_error
def show_phone(args: list, book: AddressBook) -> Record:
    """I show the phone number of a chosen man."""
    name, *_ = args
    return book.find(name)
    

def show_all(book: AddressBook) -> AddressBook:
    """I return the phone-book to print it."""
    return book


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    '''
    The function adds birthday to the contact.
    '''
    name, birthday, *_ = args
    record = book.find(name)
    message = 'Contact updated.'
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added.'
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    '''
    The function returns one's birthday as a formated string.
    '''
    name, *_ = args
    record = book.find(name)
    return f"{record.name}'s birthday is {record.birthday}."



@input_error
def birthdays(book: AddressBook) -> list:
    '''
    The function returns a list with a birthdays.
    '''
    return book.get_upcoming_birthdays()


def main() -> None:
    """I rule the show!"""
    book = load_data()
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
        command, args = parse_input(user_input)

        if command in ['close', 'exit']:
            save_data(book)
            print('Good bye!')
            break

        elif command == 'hello':
            print('How can I help you?')

        elif command == 'add':
            print(add_contact(args, book))

        elif command == 'change':
            print(change_contact(args, book))

        elif command == 'phone':
            print(show_phone(args, book))

        elif command == 'all':
            print(show_all(book))

        elif command == 'add-birthday':
            print(add_birthday(args, book))

        elif command == 'show-birthday':
            print(show_birthday(args, book))

        elif command == 'birthdays':
            pprint(birthdays(book))

        else:
            print('Invalid command.')

            
if __name__ == '__main__':
    main()
