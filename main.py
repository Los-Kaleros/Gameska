import arcade



SCREEN_WIDTH = 1000 #sirka okna
SCREEN_HEIGHT = 800 #vyska okna
SCREEN_TITLE = "Lidl Mario" #nazov okna

CHARACTER_SCALING = 0.50 #scaling postavicky opriti velkosti fotky z ktore je
TILE_SCALING = 2.00 #scaling kociek pouzitych v hre -//-

PLAYER_MOVEMENT_SPEED = 8 #rychlost pohybu postavicky
GRAVITY = 1 #sila gravitacie pouzita v hre 
PLAYER_JUMP_SPEED = 20 #rychlost skoku postavicky

    
class MainHra(arcade.Window):

    def __init__(self):  #definicia co sa deje ako prve pri spusteni
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE) #vytvorenie okna s nastavenymi parametrami
        #nacitanie mapy
        self.tile_map = None
        #nacitanie sceny, postavicky a pozadia(v zaklade je pozadie modre ak neni inak zadane)
        self.scene = None
        self.player_sprite = None 
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        #nacitanie enginu 
        self.physics_engine = None
        #nacitanie kamery
        self.camera = None
        #nacitanie zvukov
        self.jump_sound = arcade.load_sound("./zvuky/jump1.wav")
        self.game_over_sound = arcade.load_sound("./zvuky/game_over.wav")
        
        
    
    def setup(self): #definicia co sa deje ako druhe pri spusteni ()
        
        map_name = "./mapa/map5.tmj" #vyber zdroju mapy
        #jednotlive vrstvy mapy nacitane z mapy
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            

        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options) #nacitanie mapy
        self.scene = arcade.Scene.from_tilemap(self.tile_map) #vytvorenie sceny z mapy


        self.scene.add_sprite_list("Player") #vytvorenie listu pre nasu postavicku 
        

        image_source = "./obrazky/Franta.png" #zdroj obrazku postavicky
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING) #vykreslenie postavicky podla zadaných parametrov
        self.player_sprite.center_x = 64 #nastavenie pozicie postavicky na stred mapy
        self.player_sprite.center_y = 128 #nastavenie pozicie postavicky na stred mapy
        self.scene.add_sprite("Player", self.player_sprite) #pridanie postavicky do sceny

        if self.tile_map.background_color: #ak je zadane pozadie mapy tak ho nastavime
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant = GRAVITY, walls=self.scene["Platforms"]
        ) #vytvorenie enginu pre fyziku

        self.camera = arcade.Camera(self.width, self.height) #vytvorenie kamery

        
    def on_draw(self): #definicia ktora vykresluje sceny, kameru atd
        self.clear()
        self.scene.draw()
        self.camera.use()
        
        

    def on_key_press(self, key, modifiers): #definicia co sa vykonava pri stlaceni klaves
        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers): #definicia co sa vykonava pri uvolneni klaves
        if key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0


    def center_camera_to_player(self): #definicia v ktorej sa kamera nastavi na poziciu postavicky
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width /2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height /2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)
    
    
    def on_update(self, delta_time): #definicia co sa vykonava pri aktualizacii hry (aktualizacia pohybu postavicky, kamera, kontrola kolizii)
        self.physics_engine.update()

        self.center_camera_to_player()

    
    
    
    
    
def main(): #definicia hlavneho programu(spustenie definicii okna, nacitanie mapy, nacitanie postavicky, nacitanie zvukov, spustenie samotnej hry)
    window = MainHra()
    window.setup()
    arcade.run()


if __name__ == "__main__": #vyvolanie main definicie vdaka ktorej spustime celu hru
    main()
    