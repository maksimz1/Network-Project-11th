from ursina import *
from client import Client

class MainMenu(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )
        # Create menu elements
        self.title = Text("Chicken fight",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.light_gray, parent = self)
        self.play_button = Button(text="Play", scale=(0.2,0.07), origin=(0,0), y=0, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.change_map_button = Button(text="Choose Map", scale=(0.2,0.07), origin=(0,0), y=-0.1, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.quit_button = Button(text="Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)

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

class DeathScreen(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )

        
        self.title = Text("You died",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.light_gray, parent = self)
        
        self.play_again_button = Button(text = "Play Again", scale=(0.2,0.07), origin=(0,0), y=0, color='#0099db', font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.quit_button = Button(text = "Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color='#0099db', font = "Assets/Fonts/FlyingBird.ttf", parent = self)

        self.play_again_button.on_click = self.PlayAgain
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
        self.manager.client.unload_map()
        self.manager.client.load_map('map1')
    
    def PlayMap2(self):
        self.selection.y = self.map2.y
        self.selected_map = 'map2'
        self.manager.client.unload_map()
        self.manager.client.load_map('map2')

    def PlayMap3(self):
        self.selection.y = self.map3.y
        self.selected_map = 'map3'
        self.manager.client.unload_map()
        self.manager.client.load_map('map3')

class MenuManager:
    def __init__(self):
        self.menu = MainMenu(self)
        self.death_screen = DeathScreen(self)
        self.map_selection = MapMenu(self)

        self.menu.enabled = False
        self.death_screen.enabled = False
        self.map_selection.enabled = False

        self.current_menu = self.menu
        self.client = Client()

        self.animation = CameraAnimator(camera)

    def run_client(self):
        self.current_menu.enabled = False
        self.client.start_game()
    
    def show_main_menu(self):
        self.change_menu(self.menu)
        self.menu.animate_menu()

    def show_death_screen(self):
        self.change_menu(self.death_screen)
        self.death_screen.animate_menu()

    def show_map_selection(self):
        self.change_menu(self.map_selection)
        self.map_selection.animate_menu()

    def change_menu(self, menu):
        self.current_menu.enabled = False
        self.current_menu = menu
        self.current_menu.enabled = True

    def quit(self):
        self.client.in_menu = False
        application.quit()

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
        camera.look_at(pivot, up=Vec3(0,1,0))

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