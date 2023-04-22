from dnd import *

user_character = Character("temp")
userinput = 10

while userinput != 0:
    print("Welcome to the DnD character builder! What would you like to do?\n"
          "1. View character information and stats\n"
          "2. Name character\n"
          "3. Get stats\n"
          "4. Choose class\n"
          "5. Choose race\n"
          "6. Choose backgroud\n"
          "0 Exit\n")
    userinput = int(input("Option: "))
    if userinput < 0 or userinput > 6:
        print("Error: selection must be between 0 and 6 inclusive")
        continue

    elif userinput == 0:
        print("Bye!")
    
    elif userinput == 1:
        if user_character.name == "temp":
            print("You haven't made a character yet!\n")
            continue
        elif user_character.name != "temp" and user_character.clas == "":
            print(
                f"Name  : {user_character.name}\n" 
                f"Level : {user_character.level}\n")
        else:
            print(
                f"Name  : {user_character.name}\n" 
                f"Level : {user_character.level}\n"
                f"Class : {user_character.clas}\n"
                f"Str   : {user_character.stre}\n"
                f"Dex   : {user_character.dex}\n"
                f"Con   : {user_character.con}\n"
                f"Int   : {user_character.int}\n"
                f"Wis   : {user_character.wis}\n"
                f"Cha   : {user_character.cha}\n")
    
    elif userinput == 2:
        if user_character.name == "temp":
            user_character.name = input("What is your character's name: ")
        else:
            while True:
                confirm = input(f"Character is already named {user_character.name}, do you want to rename? (y/n): ")
                if confirm.lower() == "y":
                    user_character.name = input("What is your character's name: ")
                    break
                elif confirm.lower() == "n":
                    break
                else:
                    print("Error: confirmation must be one of y or n")

        print("\n")

    elif userinput == 3:
        print("How do you want to do stats:\n"
                  "1. Rolling - 4d6 and keep the highest 3\n"
                  "2. Use the standard array of [15, 14, 13, 12, 10, 8]\n"
                  "3. Use point buy\n")
        while True:
            statinput = int(input("Option: "))
            if statinput == 1:
                user_character.stats("roll")
                break
            elif statinput == 2:
                user_character.stats("standard array")
                break
            elif statinput == 3:
                user_character.stats("point buy")
                break
            else:
                print("Error: selection must be between 1 and 3 inclusive")

    elif userinput == 4:
        if user_character.clas == "":
            user_character.get_class()
        else:
            while True:
                confirm = input(f"{user_character.name} is already a(n) {user_character.clas}, do you want to redo that? (y/n): ")            
                if confirm.lower() == "y":
                    user_character.get_class()
                    break
                elif confirm.lower() == "n":
                    break
                else:
                    print("Input must be one of (y/n)")
    
    elif userinput == 5:
        print("Not ready yet!\n")

    elif userinput == 6:
        print("Not ready yet!\n")
