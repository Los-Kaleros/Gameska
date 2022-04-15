import arcade


#konštanty
SCREEN_WIDTH = 1000 #sirka okna
SCREEN_HEIGHT = 800 #vyska okna
SCREEN_TITLE = "Lidl Mario" #nazov okna

CHARACTER_SCALING = 0.50 #scaling postavicky opriti velkosti fotky z ktore je
TILE_SCALING = 2.00 #scaling kociek pouzitych v hre -//-
SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING #velkost jednej kocky v pixeloch

#rychlosti zadane v pixeloch za frame (sekundu)
PLAYER_MOVEMENT_SPEED = 7 #rychlost pohybu postavicky
GRAVITY = 1.5 #sila gravitacie pouzita v hre 
PLAYER_JUMP_SPEED = 30 #rychlost skoku postavicky

#pozicia postavicky
PLAYER_START_X = 64
PLAYER_START_Y = 225

#nazvy vrstiev z nasej Tile mapy
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYEN_NAME_DONT_TOUCH = "Don't Touch"



#klasa kde sa nastavuje menu okno
class MenuView(arcade.View):
    
    def on_show(self): #funkcia ktora sa spusti pri zobrazeni okna
        
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) #nastavi farbu pozadia na tmavom modry

    def on_draw(self): #funkcia ktora vykresli nami zadane veci uvedene nizsie
        
        self.clear() #vycisti okno pred tym ako nan nieco nakresli
        
        arcade.draw_text("Lidl Mario", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")   #nakresli text Lidl Mario s nastavenymi parametrami
        
        arcade.draw_text("(Klikni pre pokračovanie)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
                         arcade.color.BLACK, font_size=15, anchor_x="center")   #nakresli text (Klikni pre pokračovanie) s nastavenymi parametrami

    def on_mouse_press(self, _x, _y, _button, _modifiers): #funkcia ktora sa spusti pri kliknuti na myš
        
        instruction = InstructionView() #zvolime ze okno InstructionView bude pod premennou instruction
        self.window.show_view(instruction) #zobrazime okno InstructionView

#klasa kde sa nastavuje instruktazne okno   
class InstructionView(arcade.View): 

    def on_show(self): #funkcia ktora sa spusti pri zobrazeni okna
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) #nastavi farbu pozadia na tmavom modry

    def on_draw(self): #funkcia ktora vykresli nami zadane veci uvedene nizsie
        self.clear() #vycisti okno pred tym ako nan nieco nakresli
        arcade.draw_text("Inštrukcie:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center") #nakresli text Inštrukcie s nastavenymi parametrami
        arcade.draw_text("Ovládanie: W, A, D", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5,
                         arcade.color.BLACK, font_size=15, anchor_x="center") #nakresli text Ovládanie s nastavenymi parametrami
        arcade.draw_text("(Klikni pre spustenie hry)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
                         arcade.color.BLACK, font_size=15, anchor_x="center") #nakresli text (Klikni pre spustenie hry) s nastavenymi parametrami
        
    def on_mouse_press(self, _x, _y, button, _modifiers): #funkcia ktora sa spusti pri kliknuti na myš
        game_view = MyGame() #zvolime ze okno MyGame bude pod premennou game_view
        game_view.setup() #spustime funkciu setup() v MyGame
        self.window.show_view(game_view) #zobrazime okno MyGame

#klasa kde sa nastavuje jadro hry
class MyGame(arcade.Window):

    def __init__(self):  #definicia co sa deje ako prve pri spusteni
        #vyvola rodicovsku klasu a nastavi okno
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE) 
        
        self.tile_map = None 
        
        self.scene = None
        
        self.player_sprite = None 
        
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        #nacitanie enginu 
        self.physics_engine = None
        #nacitanie kamery
        self.camera = None
        #nacitanie zvuku ktory sa pouzije pri skoku
        self.jump_sound = arcade.load_sound("./zvuky/jump1.wav")
        #nacitanie zvuku ktory sa pouzije pri prehre
        self.game_over_sound = arcade.load_sound("./zvuky/game_over.wav")
        #nastevnie kde sa konci mapa aby sme vedeli kde je koniec
        self.end_of_map = 0
        #level
        self.level = 1
        
        
    
    def setup(self): #definicia co sa deje ako druhe pri spusteni ()
        
        map_name = f"./mapa/map5_level_{self.level}.tmj" #vyber zdroju mapy
        #specificke nastavenia pre nase mapy
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            
            

        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options) #nacitanie mapy
        self.scene = arcade.Scene.from_tilemap(self.tile_map) #vytvorenie sceny z mapy


        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND) #vytvorenie listu pre nasu postavicku 
        

        image_source = "./obrazky/Franta.png" #zdroj obrazku postavicky
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING) #vykreslenie postavicky podla zadaných parametrov
        self.player_sprite.center_x = 64 #nastavenie pozicie postavicky na stred mapy
        self.player_sprite.center_y = 128 #nastavenie pozicie postavicky na stred mapy
        self.scene.add_sprite("Player", self.player_sprite) #pridanie postavicky do sceny

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        if self.tile_map.background_color: #ak je zadane pozadie mapy tak ho nastavime
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant = GRAVITY, 
            walls=self.scene[LAYER_NAME_PLATFORMS],
            
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
    
    
    def on_update(self, delta_time): #definicia co sa vykonava pri aktualizacii hry (aktualizacia pohybu postavicky, kamera, kontrola kolizii, ci hrac nespadol z mapy, atd)
        self.physics_engine.update()
        
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            arcade.play_sound(self.game_over_sound)

        #co sa stane ak hrac skonci na konci mapy
        if self.player_sprite.center_x >= self.end_of_map:	 
            #nacita sa dalsia mapa
            self.level += 1
            #opetovne sa spusti definicia setup aby sa dalsia mapa mohla nacitat
            self.setup()

        
        self.center_camera_to_player() #aktualizacia kamery tak aby bola vzdy centrovana na hraca

    
    
    
    
    
def main(): #definicia hlavneho programu(spustenie definicii okna, nacitanie mapy, nacitanie postavicky, nacitanie zvukov, spustenie samotnej hry)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Lidl Mario-MENU")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    


if __name__ == "__main__": #vyvolanie main definicie vdaka ktorej spustime celu hru
    main()
    