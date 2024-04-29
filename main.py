from ursina import *
from client import Client
from menu import *
from direct.filter.CommonFilters import CommonFilters
if __name__ == '__main__':
    app = Ursina()

    filters = CommonFilters(app.win, app.cam)
    filters.set_cartoon_ink(1)

    # Create a window
    window.title = "Chicken Fight"
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False

    
    # filters.setCartoonInk(separation=2)

    # Load the menus
    menu_manager = MenuManager()
    menu_manager.show_main_menu()


    app.run()