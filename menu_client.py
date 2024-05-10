
from ursina import *
'''
This will make target entity move up or down when you hover the entity/its children
while scrolling the scroll wheel.
'''

app = Ursina()
p = Button(model='quad', scale=(.4, .8), collider='box')
for i in range(8):
    Button(parent=p , scale_y=.05, text=f'giopwjoigjwr{i}', origin_y=.5, y=.5-(i*.05))

p.add_script(Scrollable())
app.run()