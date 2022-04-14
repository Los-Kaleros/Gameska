import arcade 
from main import *
import arcade.gui
import os

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Lidl Mario-MENU", resizable=True)

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            "main.py"
  
         
    def on_draw(self):
        self.clear()
        
window = MyWindow()
arcade.run()
