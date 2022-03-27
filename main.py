import arcade


#Rozmery + Nazov okna
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Lidl Mario"

CHARACTER_SCALING = 0.30
TILE_SCALING = 0.50

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

    
class MainHra(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None

        self.scene = None
        self.player_sprite = None 
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.physics_engine = None

        self.camera = None

        self.jump_sound = arcade.load_sound("./zvuky/zvuk_skok.mp3")
        
        
    
    def setup(self):
        
        map_name = "./mapa/map_2.tmj"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)


        self.scene.add_sprite_list("Player")
        

        image_source = "./obrazky/Franta.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant = GRAVITY, walls=self.scene["Platforms"]
        )

        self.camera = arcade.Camera(self.width, self.height)

        
    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.camera.use()
        
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0


    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width /2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height /2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
    
    
    def on_update(self, delta_time):
        self.physics_engine.update()

        self.center_camera_to_player()

    
    
    
    
    
def main():
    window = MainHra()
    window.setup()
    arcade.run()

# Spustenie jadra hry
if __name__ == "__main__":
    main()
    