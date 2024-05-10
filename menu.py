from ursina import *
from client import Client

class MainMenu(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )
        # Create menu elements
        self.title = Text("Chicken fight",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.blue, parent = self)
        self.play_button = Button(text="Play", scale=(0.2,0.07), origin=(0,0), y=0, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.change_map_button = Button(text="Choose Map", scale=(0.2,0.07), origin=(0,0), y=-0.1, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.quit_button = Button(text="Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)

        self.change_map_notification = Text("Selected map unavalible", origin=(0,0), x=0, y=.4, size=0.05, font="Assets/Fonts/FlyingBird.ttf", color=color.red, parent=self)
        self.change_map_notification.alpha = 0
        # Set button callbacks
        self.play_button.on_click = self.Play
        self.change_map_button.on_click = self.ChangeMap
        self.quit_button.on_click = self.Quit

        self.animate_menu()
        self.manager = manager

    def animate_menu(self):
        # Hide menu elements
        self.title.alpha = 0
        self.play_button.alpha = 0
        self.change_map_button.alpha = 0
        self.quit_button.alpha = 0

        self.title.x += 0.5
        self.play_button.x -= 0.5
        self.change_map_button.y -= 0.5
        self.quit_button.x += 0.5

        # Animate menu in
        self.title.fade_in(duration=1, curve=curve.out_quad)
        self.title.animate_position((0,0.3), duration=1, curve=curve.out_quad)

        self.play_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.play_button.animate_position((0,0), duration=1, delay=1, curve=curve.out_quad)

        self.change_map_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.change_map_button.animate_position((0,-0.1), duration=1, delay=1, curve=curve.out_quad)

        self.quit_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.quit_button.animate_position((0,-0.2), duration=1, delay=1, curve=curve.out_quad)

    def Play(self):
        # Start the game
        self.manager.run_client()

    def ChangeMap(self):
        self.manager.show_map_selection()

    def Quit(self):
        self.manager.quit()
    
    def alert_map_unavalible(self, map):
        self.change_map_notification.text = f"Selected map unavalible, switch to {map}"
        self.change_map_notification.fade_in(duration=1, curve=curve.out_quad)
        self.change_map_notification.fade_out(duration=1, delay=2, curve=curve.out_quad)

class DeathScreen(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )

        
        self.title = Text("You died",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.red, parent = self)
        
        self.play_again_button = Button(text = "Play Again", scale=(0.2,0.07), origin=(0,0), y=0, color='#0099db', font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.quit_button = Button(text = "Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color='#0099db', font = "Assets/Fonts/FlyingBird.ttf", parent = self)

        self.play_again_button.on_click = manager.respawn
        self.quit_button.on_click = self.Quit
        
        self.animate_menu()

        self.manager = manager

    def animate_menu(self):
        # Hide death screen elements
        self.title.alpha = 0
        self.play_again_button.alpha = 0
        self.quit_button.alpha = 0

        self.title.fade_in(duration=2, curve=curve.out_quad)
        self.play_again_button.fade_in(duration=2, delay=1, curve=curve.out_quad)
        self.quit_button.fade_in(duration=2, delay=2, curve=curve.out_quad)
    
    def PlayAgain(self):
        self.manager.show_main_menu()
    
    def Quit(self):
        self.manager.quit()

class MapMenu(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )
        # Create buttons
        self.map1 = Button(text="Map 1", scale=(0.25,0.13), origin=(0,0), y=.2, color=color.red,
                           font = "Assets/Fonts/FlyingBird.ttf", parent = self, icon="Assets/Textures/map1_preview.png")
        
        self.map2 = Button(text="Map 2", scale=(0.25,0.13), origin=(0,0), y=0, color=color.red,
                           font = "Assets/Fonts/FlyingBird.ttf", parent=self, icon="Assets/Textures/map2_preview.png")
        
        self.map3 = Button(text="Map 3", scale=(0.25,0.13), origin=(0,0), y=-.2, color=color.red,
                           font = "Assets/Fonts/FlyingBird.ttf", parent=self, icon="Assets/Textures/map3_preview.png")
        
        self.back_button = Button(text="Back", scale=(0.2,0.07), origin=(0,0), y=-.4, color=color.red,
                                  font = "Assets/Fonts/FlyingBird.ttf", parent=self)
        
        # Create map selected visual
        self.selection = Entity(model="cube", scale=(0.25,0.07), x=.3, color=color.green, parent=self)

        # Text for alerting user of selected map
        self.selected_text = Text("Selected Map: ", origin=(0,0), x=-.3, y=.4, size=0.05, font="Assets/Fonts/FlyingBird.ttf", color=color.blue, parent=self)

        # Set default selected map
        self.selection.y = self.map1.y
        self.selected_map = 'map1'

        # Set button callbacks
        self.map1.on_click = self.PlayMap1
        self.map2.on_click = self.PlayMap2
        self.map3.on_click = self.PlayMap3
        self.back_button.on_click = self.Back

        self.manager = manager

        
    def animate_menu(self):
        # Hide map selection elements
        self.map1.x += 1
        self.map2.x -= 1
        self.map3.x += 1
        self.back_button.y -= 0.5

        self.map1.animate_position((0,0.2), duration=1, curve=curve.out_quad)
        self.map2.animate_position((0,0), duration=1, delay=.5, curve=curve.out_quad)
        self.map3.animate_position((0,-0.2), duration=1, delay=1, curve=curve.out_quad)
        self.back_button.animate_position((0,-0.4), duration=1, delay=1.5, curve=curve.out_quad)

    def Back(self):
        self.manager.show_main_menu()

    def PlayMap1(self):
        self.selection.y = self.map1.y
        self.selected_map = 'map1'
        self.manager.client.set_map('map1')
        self.selected_text.text = f"Selected Map: {self.selected_map}"
    
    def PlayMap2(self):
        self.selection.y = self.map2.y
        self.selected_map = 'map2'
        self.manager.client.set_map('map2')
        self.selected_text.text = f"Selected Map: {self.selected_map}"

    def PlayMap3(self):
        self.selection.y = self.map3.y
        self.selected_map = 'map3'
        self.manager.client.set_map('map3')
        self.selected_text.text = f"Selected Map: {self.selected_map}"

class MenuManager:
    def __init__(self):
        # Create the menus
        self.menu = MainMenu(self)
        self.death_screen = DeathScreen(self)
        self.map_selection = MapMenu(self)

        # Hide the menus, only show the main menu
        self.death_screen.enabled = False
        self.map_selection.enabled = False

        # Set the current menu to the main menu
        self.current_menu = self.menu

        # Create the game client
        self.client = Client(menu_manager=self)

        self.animation = CameraAnimator(camera)

    def run_client(self):
        self.client.create_connection()
        response = self.client.handshake()
        if response is True:
            # Connection successful
            self.client.start_game()
            self.current_menu.enabled = False
            self.animation.enabled = False
        elif response is False:
            # Connection failed
            self.quit()
        else:
            # Connection denied due to unavailable map
            self.menu.alert_map_unavalible(response)

    
    def respawn(self):
        self.animation.enabled = False
        self.current_menu.enabled = False
        self.client.respawn_player()
        
    def show_main_menu(self):
        self.change_menu(self.menu)
        self.menu.animate_menu()

    def show_death_screen(self):
        self.change_menu(self.death_screen)
        self.death_screen.animate_menu()
        self.animation.enabled = True

    def show_map_selection(self):
        self.change_menu(self.map_selection)
        self.map_selection.animate_menu()

    def change_menu(self, menu):
        self.current_menu.enabled = False
        self.current_menu = menu
        self.current_menu.enabled = True

    def quit(self):
        self.client.in_menu = False
        self.client.quit()

class ServerListMenu(Entity):
    # Scrollable list of servers with option to create and join a selected server
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )

        self.manager = manager

        self.title = Text("Server List", origin=(0,0), x=0, y=.3, size=0.065, font="Assets/Fonts/FlyingBird.ttf", color=color.blue, parent=self)
        self.server_list = ButtonList(parent=self, y=0)

        self.create_server_button = Button(text="Create Server", scale=(0.2,0.07), origin=(0,0), y=-.3, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)
        self.back_button = Button(text="Back", scale=(0.2,0.07), origin=(0,0), y=-.4, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)

        self.create_server_button.on_click = self.CreateServer
        self.back_button.on_click = self.Back


class CameraAnimator(Entity):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.camera.rotation = (0,0,0)
        self.camera.rotation_speed = 100
        self.angle = 0

    def animate_camera(self):
        speed = 20
        radius = 20
        # Increment angle
        self.angle += time.dt * speed
        self.angle %= 360  # Keep the angle within [0, 360)
        
        pivot = Vec3(0, 0, 0)
        # Calculate new positions
        new_x = pivot.x + radius * math.cos(math.radians(self.angle))
        new_z = pivot.z + radius * math.sin(math.radians(self.angle))

        # Lerp the camera's position
        camera.x = lerp(camera.x, new_x, 0.1)  # Smoothing factor can be adjusted
        camera.z = lerp(camera.z, new_z, 0.1)

        # Optionally adjust the camera to always look at the pivot or another target
        camera.look_at(pivot, up=(0,1,0))

    def update(self):
        self.animate_camera()



if __name__ == "__main__":
    app = Ursina()

    # # Load the menus
    # menu = MainMenu()
    # death_screen = DeathScreen()
    # map_selection = MapSelection()

    # map_selection.enabled = False
    # death_screen.enabled = False
    
    # current_menu = menu

    
    # # death_screen = DeathScreen()
    menu_manager = MenuManager()
    menu_manager.show_main_menu()

    app.run()