import re

HEADER = r"""
  _________ __                                      
 /   _____//  |_  _________________    ____   ____  
 \_____  \\   __\/  _ \_  __  \__  \  / ___\_/ __ \ 
 /        \|  | (  <_> )  | \// __  \/ /_/  >  ___/ 
/_______  /|__|  \____/|__|  (____  /\___  / \___  >
        \/                        \/ /____/      \/ 
by Python 20
<****************************************************>
"""

def regexp_check(*args):
    pattern = r"^(add|remove) [a-zA-Z]+ \d+$"
    user_string = " ".join(args)

    return True if re.match(pattern, user_string) is not None else False


def classic_check(command, item, amount):
    if command != "add" and command != "remove":
        return False

    if not item.isalpha():
        return False

    if not amount.isdigit():
        return False

    return True


# command: add/remove
# item: contains letters only
# amount: contains digits only
#
# $command $item $amount
def parse_input(sequence, check_callback):
    tokens = sequence.split(" ") # ["$command", "$item", "$amount"]
    if len(tokens) != 3:
        return None

    result = check_callback(*tokens)
    if not result:
        return None

    return tokens

def add(storage, item, amount):
    storage_item = storage.get(item)
    if storage_item is None:
        storage[item] = amount
    else:
        storage[item] += amount


def remove(storage, item, amount):
    storage_item = storage.get(item)
    if storage_item is None:
        print("Nothing to remove")
    else:
        if storage[item] >= amount:
            storage[item] -= amount
        else:
            storage.pop(item)


def main():
    print(HEADER)

    storage = {}

    while True:
        sequence = input(">>> ")

        if sequence == "exit":
            print("Bye-bye")
            break

        parsing_result = parse_input(sequence, regexp_check)
        if parsing_result is None:
            print("Wrong command format")
            continue

        command, item, amount = parsing_result

        commands = {
            "add": add,
            "remove": remove
        }

        commands[command](storage, item, int(amount))

        print("Storage state:")
        for key, value in storage.items():
            print(f"|{key:<10}|{value:*^10}|")
        print(f'|{"":*>21}|')

        # globals()[command](storage, item, amount)


if __name__ == "__main__":
    main()
