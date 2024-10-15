import os

def check_for_back(input_value):
    if input_value.strip().lower() == '0':
        print("Returning to the main menu.")
        return True
    return False

def select_or_create_folder():
    temp_folder_name = ""  # Переменная для временного хранения названия папки

    while True:
        print("\n--- Select or Create Car Brand Folder ---")
        print("1. Create a new folder")
        print("2. Use an existing folder")
        print("0. Back")
        choice = input("Enter your choice (or type '0' to return to the main menu): ").strip()

        # Проверка на команду возврата
        if check_for_back(choice):
            return None

        if choice == '1':
            # Процесс создания новой папки
            while True:
                if temp_folder_name:
                    print(f"Current input for new folder name: '{temp_folder_name}' (you can change it or type '0' to go back)")
                else:
                    print("Type '0' at any time to return to the previous menu.")

                folder_name = input("Enter a NEW folder name to store car information: ").strip()

                # Проверка на команду возврата
                if check_for_back(folder_name):
                    return None

                temp_folder_name = folder_name

                if os.path.exists(folder_name):
                    print("Invalid input: Folder already exists. Please choose a different name.")
                else:
                    os.makedirs(folder_name)
                    print(f"Folder '{folder_name}' created.")
                    return folder_name

        elif choice == '2':
            folders = [f for f in os.listdir() if os.path.isdir(f)]
            if not folders:
                print("No existing folders available. Please create a new folder.")
                continue

            print("\nAvailable Car Brand Folders:")
            for i, folder in enumerate(folders, start=1):
                print(f"{i}. {folder}")

            folder_choice = input("Enter the number of the folder you want to use (or type 'back' to return to the main menu): ").strip()
            if check_for_back(folder_choice):
                return None

            try:
                folder_choice = int(folder_choice) - 1
                if 0 <= folder_choice < len(folders):
                    return folders[folder_choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '0':
            print("Returning to the previous menu.")
            return None

        else:
            print("Invalid choice. Please enter 1, 2, or 0.")



def rename_folder():
    print("\n--- Rename a Car Brand Folder ---")
    folders = [f for f in os.listdir() if os.path.isdir(f)]
    if not folders:
        print("No existing folders available to rename.")
        return

    print("\nAvailable Car Brand Folders:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("\nEnter the number of the folder you want to rename: ")) - 1
        if 0 <= folder_choice < len(folders):
            old_folder_name = folders[folder_choice]
            new_folder_name = input("Enter the new folder name: ")
            if os.path.exists(new_folder_name):
                print("A folder with this name already exists. Please choose a different name.")
            else:
                os.rename(old_folder_name, new_folder_name)
                print(f"Folder '{old_folder_name}' has been renamed to '{new_folder_name}'.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def check_and_save_car_id():
    while True:
        print("\n--- Enter Car ID ---")
        car_id = input("Enter the Car ID (unique, or type '0' to return to the main menu): ").strip()

        # Проверка на команду возврата
        if check_for_back(car_id):
            return None

        with open("CarsID.txt", "a+") as f:
            f.seek(0)
            existing_ids = f.read().splitlines()
            if car_id in existing_ids:
                print("Invalid input: This Car ID already exists. Please use a unique ID.")
            else:
                f.write(car_id + "\n")
                return car_id

def save_car_info(folder_name, car_id, car_info):
    file_path = os.path.join(folder_name, f"{car_id}.txt")
    with open(file_path, "w") as car_file:
        car_file.write(car_info)
    print(f"\nCar information saved in '{file_path}'\n")

def view_cars():
    print("\n--- View Existing Car Brands ---")
    folders = [f for f in os.listdir() if os.path.isdir(f)]
    if not folders:
        print("No car brands available.")
        return
    
    print("\nAvailable Car Brands:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("\nEnter the number of the brand you want to view: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"\nNo cars available in the '{selected_folder}' brand.")
                return
            
            print(f"\nAvailable Cars in '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            
            file_choice = int(input("\nEnter the number of the car you want to view: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                with open(os.path.join(selected_folder, selected_file), "r") as f:
                    print("\n--- Car Information ---")
                    print(f.read())
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_car():
    print("\n--- Delete Car Information ---")
    folders = [f for f in os.listdir() if os.path.isdir(f)]
    if not folders:
        print("No car brands available.")
        return

    print("\nAvailable Car Brands:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")

    try:
        folder_choice = int(input("\nEnter the number of the brand from which you want to delete a car: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"\nNo cars available in the '{selected_folder}' brand.")
                return

            print(f"\nAvailable Cars in '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")

            file_choice = int(input("\nEnter the number of the car you want to delete: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                os.remove(os.path.join(selected_folder, selected_file))
                print(f"Car information '{selected_file}' has been deleted.")
                
                # Update CarsID.txt to remove the deleted Car ID
                car_id = selected_file.replace(".txt", "")
                with open("CarsID.txt", "r") as f:
                    ids = f.read().splitlines()
                ids = [id for id in ids if id != car_id]
                with open("CarsID.txt", "w") as f:
                    f.write("\n".join(ids))
                
                print(f"Car ID '{car_id}' removed from the list of IDs.")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    print("Welcome to the Car Dealer App")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new car")
        print("2. View existing cars")
        print("3. Delete a car")
        print("4. Rename a car brand folder")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        # Проверка на команду возврата
        if check_for_back(choice):
            continue

        if choice == '1':
            folder_name = select_or_create_folder()
            if not folder_name:
                continue  # Возвращаемся в главное меню, если пользователь ввел 'back'

            car_id = check_and_save_car_id()
            if not car_id:
                continue  # Возвращаемся в главное меню, если пользователь ввел 'back'

            print("\n--- Enter Car Details ---")
            car_model = input("Enter the Car Model (or type '0' to return to the main menu): ").strip()
            if check_for_back(car_model):
                continue

            car_year = input("Enter the Year of Manufacture (or type '0' to return to the main menu): ").strip()
            if check_for_back(car_year):
                continue

            car_price = input("Enter the Price of the Car (or type '0' to return to the main menu): ").strip()
            if check_for_back(car_price):
                continue

            car_color = input("Enter the Car color (or type '0' to return to the main menu): ").strip()
            if check_for_back(car_color):
                continue

            car_info = (
                f"Car ID: {car_id}\n"
                f"Car Model: {car_model}\n"
                f"Year of Manufacture: {car_year}\n"
                f"Price: {car_price}\n"
                f"Color: {car_color}"
            )
            save_car_info(folder_name, car_id, car_info)

        elif choice == '2':
            view_cars()

        elif choice == '3':
            delete_car()

        elif choice == '4':
            rename_folder()

        elif choice == '5':
            print("\nExiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from the menu options.")

if __name__ == "__main__":
    main()
