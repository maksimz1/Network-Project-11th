from ursina import *

class MainMenu(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui
        )
        self.title = Text("Chicken fight",origin=(0,0), x=0,y=.3,size=0.065,font = "Assets/Fonts/FlyingBird.ttf", color = color.light_gray)
        self.play_button = Button(text="Play", scale=(0.2,0.07), origin=(0,0), y=0, color=color.red,font = "Assets/Fonts/FlyingBird.ttf")
        self.quit_button = Button(text="Quit", scale=(0.2,0.07), origin=(0,0), y=-.2, color=color.red,font = "Assets/Fonts/FlyingBird.ttf")

        

    def animate_menu(self):
        # Hide menu elements
        self.title.alpha = 0
        self.play_button.alpha = 0
        self.quit_button.alpha = 0
        self.title.x += 0.5
        self.play_button.x -= 0.5
        self.quit_button.x += 0.5

        # Animate menu in
        self.title.fade_in(duration=1, curve=curve.out_quad)
        self.title.animate_position((0,0.3), duration=1, curve=curve.out_quad)

        self.play_button.fade_in(duration=1, delay=1, curve=curve.out_quad)
        self.play_button.animate_position((0,0), duration=1, delay=1, curve=curve.out_quad)

        self.quit_button.fade_in(duration=1, delay=1.5, curve=curve.out_quad)
        self.quit_button.animate_position((0,-0.2), duration=1, delay=1.5, curve=curve.out_quad)


if __name__ == "__main__":
    app = Ursina()
    menu = MainMenu()
    menu.animate_menu()
    app.run()