from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate_format(self):
        return len(str(self.value)) == 10 and str(self.value).isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if isinstance(phone, Phone) and phone.validate_format():
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone number format.")

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone number not found in the record.")

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        else:
            raise ValueError("Phone number not found in the record.")

    def find_phone(self, phone):
        if phone in self.phones:
            return str(phone)
        else:
            raise ValueError("Phone number not found in the record.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value.lower()] = record
        else:
            raise ValueError("Invalid record format.")

    def delete(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            del self.data[name_lower]
        else:
            raise ValueError("Record not found in the address book.")

    def find(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            return self.data[name_lower]
        else:
            raise ValueError("Record not found in the address book.")

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter username."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"An error occurred: {e}"

    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts.add_record(Record(name))
    contacts.find(name).add_phone(Phone(phone))
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts.find(name).edit_phone(Phone(phone), Phone(args[1]))
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    return contacts.find(name)

def show_all(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join([f"{record}" for record in contacts.data.values()])

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, contacts))
            elif command == "change":
                print(change_contact(args, contacts))
            elif command == "phone":
                print(show_phone(args, contacts))
            elif command == "all":
                print(show_all(contacts))
            else:
                print("Invalid command.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    main()

