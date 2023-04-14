from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem
import platform
import os

from downloaders import list_available_downloads, download_apps_menu, download_all_apps_menu
from settings import set_standard_download_location, settings_menu

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def list_downloads_and_wait():
    list_available_downloads()
    input("\nPress Enter to return to the main menu...")
    clear_screen()

def main():
    main_menu = ConsoleMenu("Main Menu", "")

    list_downloads_item = FunctionItem("List all available downloads", list_downloads_and_wait)
    main_menu.append_item(list_downloads_item)

    download_menu = ConsoleMenu("Download Menu", "")
    download_apps_item = FunctionItem("Download apps", download_apps_menu)
    download_all_apps_item = FunctionItem("Download all apps", download_all_apps_menu)
    download_menu.append_item(download_apps_item)
    download_menu.append_item(download_all_apps_item)

    download_submenu = SubmenuItem("Download applications", download_menu, main_menu)
    main_menu.append_item(download_submenu)

    settings_menu = ConsoleMenu("Settings Menu", "")
    set_standard_location_item = FunctionItem("Set standard download location", set_standard_download_location)
    settings_menu.append_item(set_standard_location_item)

    settings_submenu = SubmenuItem("Settings", settings_menu, main_menu)
    main_menu.append_item(settings_submenu)

    main_menu.show()

if __name__ == "__main__":
    os_name = platform.system()
    if os_name == "Windows":
        main()
    else:
        print("This script does not support your operating system.")
