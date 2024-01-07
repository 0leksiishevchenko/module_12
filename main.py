import functools
from inspect import signature
from bookclass import AddressBook, Record, Phone, Birthday, Name


def input_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Input error: {str(e)}"
    return wrapper

@input_error 
def add_contact(name, phone):
    
    if name in address_book.data:
        raise ValueError(f"Contact {name} already exists")
    
    birthday = None    
    is_birthday = input('Would you like to record a birthday for this contact? (y/n): ')
    if is_birthday.casefold() == 'y':
        birthday = input("Enter birthday (DD-MM-YYYY): ")
    
    record = Record(name, birthday)
    record.add_phone(phone)
    address_book.add_record(record)
    
    return f"Contact {name} added with phone {phone}" 

@input_error
def change_contact(name):
    if name not in address_book.data:
        raise KeyError(f"Contact {name} not found")
    
    ch_contact = address_book.find(name)
    is_change = input('What exactly do you want to change?\n Plese type:\n "N" - name\n "P" - phone\n "B" - birthday : ')
    
    if is_change.casefold() == 'n':
        new_name = input('Enter new name : ')
        ch_contact[0].edit_name(new_name)
        
    
    if is_change.casefold() == 'p':
        old_phone = ch_contact[0].phones[0].value
        if len(ch_contact[0].phones) > 1:
            old_phone_idx = input(f"contact contains {len(ch_contact[0].phones)} numbers, select the number to change(1/2)) : ")
            old_phone_idx += 1
            old_phone = ch_contact[0].phones[old_phone_idx].value
        
        new_phone = input('Enter new number : ')
        ch_contact[0].edit_phone(old_phone, new_phone)

    if is_change.casefold() == 'b':
        new_birthday = input('Enter new birthday date : ')
        ch_contact[0].edit_birthday(new_birthday)
    
    return f" Contact {name} edited"

@input_error
def delete_contact(name):
    address_book.delete(name)
    return f"conatact {name} removed"

@input_error
def get_phone(query):
    
    contact_list = address_book.find(query)
    res = '\n'.join(
    [f"Name: {record.name}, Phones: {'; '.join(contact.value for contact in record.phones)}, Birthday: {record.birthday}" for record in contact_list])
    
    return res 

@input_error
def show_all():
    
    contacts_list = "\n".join(
        [f"Name: {record.name}, Phones: {'; '.join(contact.value for contact in record.phones)}, Birthday: {record.birthday}" for record in address_book.data.values()])
    
    return contacts_list

@input_error
def hello():
    return "How can I help you?"

@input_error
def good_bye():
    address_book.save_to_file(filename)
    return "Good bye!"

@input_error
def get_handler(command):
    handlers = {
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "delete": delete_contact,
        "phone": get_phone,
        "show all": show_all,
    }

    _, *args = command.split(" ")
    for key, handler in handlers.items():
        if key in command.lower():
            expected_args = len(signature(handler).parameters)
            if len(args) != expected_args:
                
                return handler()

            return handler(*args)
                                    
    return "Invalid command. Please try again."


def main():
    global filename, address_book
    filename = "address_book.pkl"
    address_book = AddressBook() 

    try:
        address_book.read_from_file(filename)
    except FileNotFoundError: 
        print("new book created")
    
    while True:
        command = input("Enter a command: ").lower()
        
        if command in ["good bye", "close", "exit"]:
            print(get_handler(command))
            break
            
        print(get_handler(command))

if __name__ == "__main__":
    main()