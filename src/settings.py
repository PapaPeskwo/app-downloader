import os
import json

SETTINGS_FILE = 'settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def set_standard_download_location():
    settings = load_settings()
    print("Current standard download location:", settings.get('standard_download_location', 'Not set'))
    new_location = input("Enter the new standard download location (or leave blank to cancel):\n").strip()
    if new_location:
        if os.path.exists(new_location) and os.path.isdir(new_location):
            settings['standard_download_location'] = new_location
            save_settings(settings)
            print("Standard download location has been updated.")
        else:
            print("Invalid directory. Please enter a valid directory.")

def get_download_location():
    settings = load_settings()
    return settings.get('standard_download_location', '')

def settings_menu():
    print("1. Set standard download location")
    print("2. Go back to the main menu")
    choice = int(input("\nChoose an option (1-2): "))

    if choice == 1:
        set_standard_download_location()
    elif choice == 2:
        return
    else:
        print("Invalid choice. Please try again.")