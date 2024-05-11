from ursina import *
from client import Client
from menu_client import MenuClient

class MainMenu(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )
        # Create menu elements
        self.title = Text("Chicken fight",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.blue, parent = self)
        self.play_button = Button(text="Play", scale=(0.2,0.07), origin=(0,0), y=0, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.servers_button = Button(text="Servers", scale=(0.2,0.07), origin=(0,0), y=-.1, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        # self.change_map_button = Button(text="Choose Map", scale=(0.2,0.07), origin=(0,0), y=-0.1, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)
        self.quit_button = Button(text="Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color=color.red,font = "Assets/Fonts/FlyingBird.ttf", parent = self)

        self.change_map_notification = Text("Selected map unavalible", origin=(0,0), x=0, y=.4, size=0.05, font="Assets/Fonts/FlyingBird.ttf", color=color.red, parent=self)
        self.change_map_notification.alpha = 0
        # Set button callbacks
        self.play_button.on_click = manager.run_client
        self.servers_button.on_click = manager.show_server_list
        # self.change_map_button.on_click = self.ChangeMap
        self.quit_button.on_click = manager.quit

        # Hide menu elements
        self.title.alpha = 0
        self.play_button.alpha = 0
        self.servers_button.alpha = 0
        self.quit_button.alpha = 0

        self.title.x = 0.5
        self.play_button.x = -0.5
        self.servers_button.x = 0.5
        self.quit_button.x = -0.5

        # self.animate_menu()
        self.manager = manager

    def animate_menu(self):

        # Animate menu in
        self.title.fade_in(duration=1, curve=curve.out_quad)
        self.title.animate_position((0,0.3), duration=1, curve=curve.out_quad)

        self.play_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.play_button.animate_position((0,0), duration=1, delay=1, curve=curve.out_quad)

        self.servers_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.servers_button.animate_position((0,-0.1), duration=1, delay=1, curve=curve.out_quad)
        # self.change_map_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        # self.change_map_button.animate_position((0,-0.1), duration=1, delay=1, curve=curve.out_quad)

        self.quit_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.quit_button.animate_position((0,-0.2), duration=1, delay=1, curve=curve.out_quad)

    def Play(self):
        # Start the game
        self.manager.run_client()

    def Quit(self):
        self.manager.quit()
    
    def alert_map_unavalible(self, map):
        self.change_map_notification.text = f"Selected map unavalible, Server uses {map}"
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
        
        # self.animate_menu()
        self.manager = manager

        # Hide death screen elements
        self.title.alpha = 0
        self.play_again_button.alpha = 0
        self.quit_button.alpha = 0

    def animate_menu(self):
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

        # Set button callbacks
        self.map1.on_click = self.PlayMap1
        self.map2.on_click = self.PlayMap2
        self.map3.on_click = self.PlayMap3
        self.back_button.on_click = self.Back

        self.manager = manager

        # Hide map selection elements
        self.map1.x += 1
        self.map2.x -= 1
        self.map3.x += 1
        self.back_button.y -= 0.5
        
    def animate_menu(self):
        self.map1.animate_position((0,0.2), duration=1, curve=curve.out_quad)
        self.map2.animate_position((0,0), duration=1, delay=.5, curve=curve.out_quad)
        self.map3.animate_position((0,-0.2), duration=1, delay=1, curve=curve.out_quad)
        self.back_button.animate_position((0,-0.4), duration=1, delay=1.5, curve=curve.out_quad)

    def Back(self):
        self.manager.show_create_server()

    def PlayMap1(self):
        self.selection.y = self.map1.y
        self.manager.selected_map = 'map1'
        self.manager.client.set_map('map1')
        self.selected_text.text = f"Selected Map: {self.manager.selected_map}"
    
    def PlayMap2(self):
        self.selection.y = self.map2.y
        self.manager.selected_map = 'map2'
        self.manager.client.set_map('map2')
        self.selected_text.text = f"Selected Map: {self.manager.selected_map}"

    def PlayMap3(self):
        self.selection.y = self.map3.y
        self.manager.selected_map = 'map3'
        self.manager.client.set_map('map3')
        self.selected_text.text = f"Selected Map: {self.manager.selected_map}"

class MenuManager:
    def __init__(self):
        self.lobbies = []
        self.selected_map = 'map1'
        self.selected_server = None
        # Create the menus
        self.menu = MainMenu(self)
        self.death_screen = DeathScreen(self)
        self.map_selection = MapMenu(self)
        self.server_list = ServerListMenu(self)
        self.create_server = CreateServerMenu(self)
        

        # Hide the menus, only show the main menu
        self.death_screen.enabled = False
        self.map_selection.enabled = False
        self.server_list.enabled = False
        self.menu.enabled = False
        self.create_server.enabled = False

        # Set the current menu to the main menu
        self.current_menu = self.menu

        self.menuClient = MenuClient(self)

        # Create the game client
        self.client = Client(menu_manager=self)

        self.animation = CameraAnimator(camera)

    def run_client(self):
        # Start the game client
        print(f"Connecting to server at {self.client.ip}:{self.client.port}")
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
    
    def show_server_list(self):
        self.server_list.update_server_list(self.lobbies)
        self.change_menu(self.server_list)
        self.server_list.animate_menu()

    def show_create_server(self):
        self.change_menu(self.create_server)
        self.create_server.animate_menu()

    def change_menu(self, menu):
        self.current_menu.enabled = False
        self.current_menu = menu
        self.current_menu.enabled = True

    def quit(self):
        self.menuClient.inMenu = False
        self.client.quit()

class ServerListMenu(Entity):
    # Scrollable list of servers with option to create and join a selected server
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )

        self.manager = manager
        
        # self.selected_server = None
        self.servers_dict = {}

        self.title = Text("Server List", origin=(0,0), x=0, y=.3, size=0.065, font="Assets/Fonts/FlyingBird.ttf", color=color.blue, parent=self)
        # p = Button(model='quad', parent=self, scale=(.4, .8), collider='box')
        # self.servers_dict[f'example_server    |    Players:-2000'] = Func(print, 'bob')
        self.server_list = ButtonList(parent=self, button_dict=self.servers_dict, button_height=1.3, width = 0.7, y=.1)
        # self.server_list.add_script(Scrollable(max=0.2, min = -0.1, scroll_speed=.01))

        self.join_server_button = Button(text="Join Server", scale=(0.2,0.07), origin=(0,0), y=-.1, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)

        self.create_server_button = Button(text="Create Server", scale=(0.2,0.07), origin=(0,0), y=-.2, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)
        self.back_button = Button(text="Back", scale=(0.2,0.07), origin=(0,0), y=-.3, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)

        self.create_server_button.on_click = manager.show_create_server
        self.back_button.on_click = manager.show_main_menu
        self.join_server_button.on_click = self.join_server
        
        # Hide server list elements
        self.title.alpha = 0
        self.server_list.alpha = 0
        self.create_server_button.alpha = 0
        self.back_button.alpha = 0

    def animate_menu(self):
        self.title.fade_in(duration=1, curve=curve.out_quad)
        self.server_list.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.create_server_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.back_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
    
    def select_server(self, server):
        self.manager.selected_server = server
        self.manager.client.set_map(server['map'])
        self.manager.client.port = server['port']
        print(f"Selected server: {server['lobby_id']} - {server['map']} - {server['players']} players")

    def join_server(self):
        if self.manager.selected_server is not None:
            self.manager.menuClient.join_lobby(self.manager.selected_server['lobby_id'])
            while self.manager.menuClient.inMenu:
                pass
            print("Started Client")
            self.manager.run_client()
    
    def update_server_list(self, servers):
        print(f"Updating server list: {servers}")
        self.manager.menuClient.get_lobby_list()
        for server in servers:
            # self.servers[f'{server["lobby_id"]}    |    Players:{server["players"]}'] = Func(self.manager.menuClient.join_lobby, server["lobby_id"])
            self.servers_dict[f'{server["lobby_id"]}   |   Players:{server["players"]}   |   Map:{server["map"]}'] = Func(self.select_server, server)
        destroy(self.server_list)
        self.server_list = ButtonList(parent=self, button_dict=self.servers_dict, button_height=1.3, width = 0.7, y=.1)



class CreateServerMenu(Entity):
    def __init__(self, manager):
        super().__init__(
            parent = camera.ui
        )

        self.manager = manager

        self.title = Text("Create Server", origin=(0,0), x=0, y=.3, size=0.065, font="Assets/Fonts/FlyingBird.ttf", color=color.blue, parent=self)
        self.server_name_input = InputField(placeholder="Server Name", scale=(0.3,0.07), origin=(0,0), y=0.2, color=color.black, font="Assets/Fonts/FlyingBird.ttf", parent=self)
        self.create_button = Button(text="Create", scale=(0.2,0.07), origin=(0,0), y=-.15, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)
        self.map_selection_button = Button(text="Map",scale=(0.2,0.07), origin=(0,0), y=-.25, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)
        self.back_button = Button(text="Back", scale=(0.2,0.07), origin=(0,0), y=-.35, color=color.red, font="Assets/Fonts/FlyingBird.ttf", parent=self)

        # Hide server list elements
        self.title.alpha = 0
        self.server_name_input.alpha = 0
        self.create_button.alpha = 0
        self.back_button.alpha = 0
        self.map_selection_button.alpha = 0

    def animate_menu(self):
        self.title.fade_in(duration=1, curve=curve.out_quad)
        self.server_name_input.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.create_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.back_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.map_selection_button.fade_in(duration=1, delay=1, curve=curve.out_quad)

        self.create_button.on_click = self.CreateServer
        self.back_button.on_click = self.Back
        self.map_selection_button.on_click = self.manager.show_map_selection

    def CreateServer(self):
        self.manager.menuClient.create_lobby(self.manager.selected_map, self.server_name_input.text)
    
    def Back(self):
        self.manager.show_server_list()

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
    menu_manager.show_create_server()

    app.run()