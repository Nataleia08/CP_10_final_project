
import re
from class_list import Name, Phone, Record, AddressBook, User, Birthday


def main_address_book():
    user_1 = User()
    command_list = ["hello", "add", "change",
                    "phone", "show all", "close", "exit", "good bye", "birthday", "on page", "search", "save", "load"]
    command_list_with_name = ["add", "change", "phone", "birthday"]
    command_list_exit = ["close", "exit", "good bye"]
    address_book = user_1.command_load()
    print("Address book:")
    address_book.show_all()
    while True:
        command_name = Name()
        command_birthday = Birthday()
        find_command = False
# ----------------------------Розпізнавання введенної команди-----------------------
        command_string = input("Enter command:").lower()
        if command_string == ".":
            break
        for k in command_list:
            if k in command_string:
                input_com = k
                attribute_sring = command_string.replace(input_com, "").strip()
                find_command = True
                break
        if not find_command:
            print("Command undefined! Try again!")
            continue
        input_list = attribute_sring.split(" ")
# ------------------------------Пошук імені -----------------------------------------------
    if command_list_with_name.count(input_com) != 0:
        for i in input_list:
            if i.isalpha():
                name = i
                command_name.value = i
                input_list.remove(i)
                break
# ------------------------------Пошук телефону------------------------------------------------
    if (input_com == "add") or (input_com == "change"):
        command_phone = []
        phone_id = 0
        s = re.findall(
            r"[+380]?[(]?[0-9]{2}[)]?[0-9]{3}[-]?[0-9]{1,2}[-]?[0-9]{2,3}\b", " ".join(input_list))
        if s != None:
            for i in s:
                i_phone = Phone()
                i_phone.value = i
                command_phone.append(i_phone)
                input_list = (" ".join(input_list).replace(i, "")).split(" ")
# ------------------------------Пошук дати народження---------------------------------------------
        date_birthday = None
        for i in input_list:
            if (re.search(r"[0-9]{4}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{2}\b", i) != None):
                date_birthday = re.search(
                    r"[0-9]{4}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{2}\b", i).string
                break
            if (re.search(r"[0-9]{2}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{4}\b", i) != None):
                date_birthday = re.search(
                    r"[0-9]{2}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{4}\b", i).string
                break
        command_birthday.value = date_birthday
# ----------------------------Виконання команди--------------------------------------
    if input_com == "hello":
        user_1.command_hello()
    elif command_list_exit.count(input_com) != 0:
        user_1.command_save(address_book)
        user_1.command_exit()
    elif input_com == "add":
        try:
            if (not name) or (len(command_phone) == 0):
                print("Give me name and phone please!")
                continue
            new_record = Record(command_name, command_phone, command_birthday)
            address_book.add_record(new_record)
        except:
            print("Give me name and phone please!")
    elif input_com == "change":
        try:
            if (not name) or (len(command_phone) == 0):
                print("Give me name and phone please!")
                continue
            command_record = address_book.search_record(name)
            command_name = command_record.name
            if command_birthday.value == None:
                command_birthday = command_record.date
            new_record = Record(command_name, command_phone, command_birthday)
            address_book.change_record(new_record)
        except:
            print("Give me name and phone please!")
    elif input_com == "phone":
        try:
            address_book.search_phone(name)
        except:
            print("Enter user name!")
    elif input_com == "show all":
        try:
            address_book.show_all()
        except:
            print("No data!")
    elif input_com == "birthday":
        try:
            command_record = address_book.search_record(name)
            print("by", command_record.days_to_birthday().days, "days")
        except Exception as e:
            print("Error!", e.args)
    elif input_com == "on page":
        try:
            records_on_pages = int(input("Input count records on pages:"))
            n_p_b = 1
            for p_b in address_book.iterator(records_on_pages):
                print("Pages:", n_p_b, p_b)
                n_p_b += 1
        except:
            print("No data!")
    elif input_com == "save":
        try:
            user_1.command_save(address_book)
            print("Data saved successfully!")
        except:
            print("Error! ", e.args)
    elif input_com == "load":
        try:
            address_book = user_1.command_load()
            print("Address book:")
            address_book.show_all()
        except Exception as e:
            print("Error! ", e.args)
    elif input_com == "search":
        try:
            address_book.command_search(attribute_sring)
        except Exception as e:
            print("Error! ", e.args)
    else:
        print("Command undefined! Try again!")

    user_1.command_save(address_book)


while True:
    command_name = Name()
    command_birthday = Birthday()
    find_command = False
# ----------------------------Розпізнавання введенної команди-----------------------
    command_string = input("Enter command:").lower()
    if command_string == ".":
        break
    for k in command_list:
        if k in command_string:
            input_com = k
            attribute_sring = command_string.replace(input_com, "").strip()
            find_command = True
            break
    if not find_command:
        print("Command undefined! Try again!")
        continue
    input_list = attribute_sring.split(" ")
# ------------------------------Пошук імені -----------------------------------------------
    if command_list_with_name.count(input_com) != 0:
        for i in input_list:
            if i.isalpha():
                name = i
                command_name.value = i
                input_list.remove(i)
                break
# ------------------------------Пошук телефону------------------------------------------------
    if (input_com == "add") or (input_com == "change"):
        command_phone = []
        phone_id = 0
        s = re.findall(
            r"[+380]?[(]?[0-9]{2}[)]?[0-9]{3}[-]?[0-9]{1,2}[-]?[0-9]{2,3}\b", " ".join(input_list))
        if s != None:
            for i in s:
                i_phone = Phone()
                i_phone.value = i
                command_phone.append(i_phone)
                input_list = (" ".join(input_list).replace(i, "")).split(" ")
# ------------------------------Пошук дати народження---------------------------------------------
        date_birthday = None
        for i in input_list:
            if (re.search(r"[0-9]{4}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{2}\b", i) != None):
                date_birthday = re.search(
                    r"[0-9]{4}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{2}\b", i).string
                break
            if (re.search(r"[0-9]{2}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{4}\b", i) != None):
                date_birthday = re.search(
                    r"[0-9]{2}[-]?[/]?[.]?[0-9]{2}[-]?[/]?[.]?[0-9]{4}\b", i).string
                break
        command_birthday.value = date_birthday
# ----------------------------Виконання команди--------------------------------------
    if input_com == "hello":
        user_1.command_hello()
    elif command_list_exit.count(input_com) != 0:
        user_1.command_save(address_book)
        user_1.command_exit()
    elif input_com == "add":
        try:
            if (not name) or (len(command_phone) == 0):
                print("Give me name and phone please!")
                continue
            new_record = Record(command_name, command_phone, command_birthday)
            address_book.add_record(new_record)
        except:
            print("Give me name and phone please!")
    elif input_com == "change":
        try:
            if (not name) or (len(command_phone) == 0):
                print("Give me name and phone please!")
                continue
            command_record = address_book.search_record(name)
            command_name = command_record.name
            if command_birthday.value == None:
                command_birthday = command_record.date
            new_record = Record(command_name, command_phone, command_birthday)
            address_book.change_record(new_record)
        except:
            print("Give me name and phone please!")
    elif input_com == "phone":
        try:
            address_book.search_phone(name)
        except:
            print("Enter user name!")
    elif input_com == "show all":
        try:
            address_book.show_all()
        except:
            print("No data!")
    elif input_com == "birthday":
        try:
            command_record = address_book.search_record(name)
            print("by", command_record.days_to_birthday().days, "days")
        except Exception as e:
            print("Error!", e.args)
    elif input_com == "on page":
        try:
            records_on_pages = int(input("Input count records on pages:"))
            n_p_b = 1
            for p_b in address_book.iterator(records_on_pages):
                print("Pages:", n_p_b, p_b)
                n_p_b += 1
        except:
            print("No data!")
    elif input_com == "save":
        try:
            user_1.command_save(address_book)
            print("Data saved successfully!")
        except:
            print("Error! ", e.args)
    elif input_com == "load":
        try:
            address_book = user_1.command_load()
            print("Address book:")
            address_book.show_all()
        except Exception as e:
            print("Error! ", e.args)
    elif input_com == "search":
        try:
            address_book.command_search(attribute_sring)
        except Exception as e:
            print("Error! ", e.args)
    else:
        print("Command undefined! Try again!")

user_1.command_save(address_book)
