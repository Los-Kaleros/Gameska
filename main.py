import arcade
import arcade.gui

#konštanty
SCREEN_WIDTH = 1000 #sirka okna
SCREEN_HEIGHT = 800 #vyska okna
SCREEN_TITLE = "Honey Run" #nazov okna

CHARACTER_SCALING = 1.25 #scaling postavicky opriti velkosti fotky z ktore je
TILE_SCALING = 2.00 #scaling kociek pouzitych v hre -//-
SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING #velkost jednej kocky v pixeloch
COIN_SCALING = TILE_SCALING

#rychlosti zadane v pixeloch za frame (sekundu)
PLAYER_MOVEMENT_SPEED = 6.00 #rychlost pohybu postavicky
GRAVITY = 1.5 #sila gravitacie pouzita v hre 
PLAYER_JUMP_SPEED = 35 #rychlost skoku postavicky
PLAYER_MOVEMENT_SPEED_ZAPOR = -7

#pozicia postavicky pri starte
PLAYER_START_X = 64
PLAYER_START_Y = 225

#nazvy vrstiev z nasej Tile mapy
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYEN_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_ENEMIES = "Enemies"



#klasa kde sa nastavuje menu okno
class MenuView(arcade.View):
    
    def on_show(self): #funkcia ktora sa spusti pri zobrazeni okna
        
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) #nastavi farbu pozadia na tmavom modry

    def on_draw(self): #funkcia ktora vykresli nami zadane veci uvedene nizsie
        
        self.clear() #vycisti okno pred tym ako nan nieco nakresli
        
        arcade.draw_text("Honey Run", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.GREEN, font_size=70, anchor_x="center",font_name="Kenney Mini Square", bold = True)   #nakresli text Lidl Mario s nastavenymi parametrami
        
        arcade.draw_text("(Klikni pre pokracovanie)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
                         arcade.color.GREEN, font_size=25, anchor_x="center",font_name="Kenney Mini Square")   #nakresli text (Klikni pre pokračovanie) s nastavenymi parametrami

    def on_mouse_press(self, _x, _y, _button, _modifiers): #funkcia ktora sa spusti pri kliknuti na myš
        
        instruction = InstructionView() #zvolime ze okno InstructionView bude pod premennou instruction
        self.window.show_view(instruction) #zobrazime okno InstructionView
        self.window.set_window(instruction) 

#klasa kde sa nastavuje instruktazne okno   
class InstructionView(arcade.View): 

    def on_show(self): #funkcia ktora sa spusti pri zobrazeni okna
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) #nastavi farbu pozadia na tmavom modry

    def on_draw(self): #funkcia ktora vykresli nami zadane veci uvedene nizsie
        self.clear() #vycisti okno pred tym ako nan nieco nakresli
        arcade.draw_text("Návod:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.GREEN, font_size=50, anchor_x="center",font_name="Kenney Mini Square") #nakresli text Inštrukcie s nastavenymi parametrami
        arcade.draw_text("Ovládanie: W, A, S, D", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.5,
                         arcade.color.GREEN, font_size=35, anchor_x="center",font_name="Kenney Mini Square") #nakresli text Ovládanie s nastavenymi parametrami
        arcade.draw_text("(Klikni pre spustenie hry)", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3,
                         arcade.color.GREEN, font_size=15, anchor_x="center",font_name="Kenney Mini Square") #nakresli text (Klikni pre spustenie hry) s nastavenymi parametrami
    

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
        
        self.background = None

        self.player_sprite = None 
        
        self.coin_hit_list = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
        #nacitanie enginu 
        self.physics_engine = None
        
        #nacitanie kamery
        self.camera = None
        
        self.gui_camera = None

        self.score = 0

        self.points = 1

        #nacitanie zvuku ktory sa pouzije pri zozbierani medu
        self.coin_collect_sound = arcade.load_sound("./zvuky/coin_sound.wav")
        
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
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True, 
            },
            

        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options) #nacitanie mapy
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map) #vytvorenie sceny z mapy
                
        self.gui_camera = arcade.Camera(self.width, self.height)

        self.background = arcade.load_texture("./obrazky/Background.png")


        # Keep track of the score
        self.score = 0

        self.scene.add_sprite_list_after("Player", LAYER_NAME_FOREGROUND) #vytvorenie listu pre nasu postavicku 
        

        image_source = "./obrazky/Medved.png" #zdroj obrazku postavicky
        self.player_sprite = arcade.Sprite(image_source,CHARACTER_SCALING, hit_box_algorithm = None) #vykreslenie postavicky podla zadaných parametrov
        self.player_sprite.center_x = 64 #nastavenie pozicie postavicky na stred mapy
        self.player_sprite.center_y = 128 #nastavenie pozicie postavicky na stred mapy
        self.scene.add_sprite("Player", self.player_sprite) #pridanie postavicky do sceny

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE - 500 #urcenie kde sa nachadza koniec mapy


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, 
            gravity_constant = GRAVITY,
            ladders = self.scene[LAYER_NAME_LADDERS], 
            walls=self.scene[LAYER_NAME_PLATFORMS],
            
        ) #vytvorenie fyzickeho enginu

        self.camera = arcade.Camera(self.width, self.height) #vytvorenie kamery s nastavenim rozmerov

    
    def on_draw(self): #definicia ktora vykresluje sceny, kameru atd
        self.clear() #vycisti okno pred tym ako nan nieco nakresli
        
        
        self.scene.draw() #vykresli scenu
        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()
        
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Medov: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        self.camera.use() #pouzije kameru
        
        #self.player_sprite.draw_hit_box(arcade.color.RED, 3) #vykresli hitbox postavicky
        

    def on_key_press(self, key, modifiers): #definicia co sa vykonava pri stlaceni klaves
        if key == arcade.key.W: #ak sa stlaci W tak:
            if self.physics_engine.is_on_ladder(): #ak je postavicka na rebriku tak:
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED #zmena pozicie postavicky v osi y na velkost PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(): #ak je mozne skocit tak:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED #zmena pozicie postavicky v osi y na velkost PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound) #spusti zvuk skoku
        elif key == arcade.key.S: #ak sa stlaci S tak:
            if self.physics_engine.is_on_ladder(): #ak je postavicka na rebriku tak:
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED #zmena pozicie postavicky v osi y na velkost -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers): #definicia co sa vykonava pri uvolneni klaves
        
        if key == arcade.key.W: #ak sa pusti W tak:
            if self.physics_engine.is_on_ladder(): #ak je postavicka na rebriku tak:
                self.player_sprite.change_y = 0 #zmena pozicie postavicky v osi y na velkost 0 (zastavi sa na rebriku)
        elif key == arcade.key.S: #ak sa pusti S tak:
            if self.physics_engine.is_on_ladder(): #ak je postavicka na rebriku tak:
                self.player_sprite.change_y = 0 #zmena pozicie postavicky v osi y na velkost 0 (zastavi sa na rebriku)
        elif key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0


    def center_camera_to_player(self): #definicia v ktorej sa kamera nastavi na poziciu postavicky
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width /2) #urcenie stredu okna na osi x
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height /2) #urcenie stredu okna na osi y 

        if screen_center_x < 0: 
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y 
        self.camera.move_to(player_centered) #nastavenie kamery na poziciu postavicky
    


    def on_update(self, delta_time): #definicia co sa vykonava pri aktualizacii hry (aktualizacia pohybu postavicky, kamera, kontrola kolizii, ci hrac nespadol z mapy, atd)
        self.physics_engine.update() #aktualizacia fyzickeho enginu
        
        if self.player_sprite.center_y < -100: #ak hrac spadol z mapy tak:
            self.player_sprite.center_x = PLAYER_START_X #nastavenie pozicie postavicky na poziciu zadanej v konfiguracnom subore
            self.player_sprite.center_y = PLAYER_START_Y #nastavenie pozicie postavicky na poziciu zadanej v konfiguracnom subore

            arcade.play_sound(self.game_over_sound) #spusti zvuk prehra
        
        #co sa stane ak hrac skonci na konci mapy
        if self.player_sprite.center_x >= self.end_of_map: #ak sa postavicka nachadza na konci mapy tak:	 
            self.level += 1 #zvysenie levelu o 1
            self.setup() #znovu nastavenie hry
        
        coin_hit_list = arcade.check_for_collision_with_list(
           self.player_sprite, 
           self.scene["Coins"],
           
        )
            
        
        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.coin_collect_sound)
            # Add one to the score
            self.score += 1
        
        
        self.center_camera_to_player() #aktualizacia kamery tak aby bola vzdy centrovana na hraca

    
    
    
    
    
def main(): #definicia hlavneho programu(spustenie definicii okna, nacitanie mapy, nacitanie postavicky, nacitanie zvukov, spustenie samotnej hry)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Lidl Mario-MENU")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    


if __name__ == "__main__": #vyvolanie main definicie vdaka ktorej spustime celu hru
    main()