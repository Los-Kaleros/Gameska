import arcade



#Rozmery + Nazov okna
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Lidl Mario"

TILE_SCALING = 0.5

    
class MainHra(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.scene = None
        self.player_sprite = None 
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    
    def setup(self):
        self.scene = arcade.Scene()
        
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite("./obrazky/zem.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        coordinate_list = [[512, 96],[256, 96], [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("./obrazky/box1.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
        
    def on_draw(self):
        self.clear()
        self.scene.draw()
    
    
    
    
def main():
    window = MainHra()
    window.setup()
    arcade.run()

# Spustenie jadra hry
if __name__ == "__main__":
    main()