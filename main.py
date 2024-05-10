from ursina import *
from client import Client
from menu import *
from direct.filter.CommonFilters import CommonFilters
if __name__ == '__main__':
    app = Ursina()

    

    # Create a window
    window.title = "Chicken Fight"
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False

    # Load the menus
    menu_manager = MenuManager()
    menu_manager.show_main_menu()


    app.run()