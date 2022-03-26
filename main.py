import arcade

#Rozmery + Nazov okna
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Lidl Mario"

def draw_pozadie():
    arcade.draw_rectangle_filled(SCREEN_WIDTH /2, SCREEN_HEIGHT * 2/3,
                                 SCREEN_WIDTH -1, SCREEN_HEIGHT * 3/3, arcade.color.LIGHT_BLUE)
    arcade.draw_rectangle_filled(SCREEN_WIDTH /2, SCREEN_HEIGHT * 0/5,
                                 SCREEN_WIDTH -1, SCREEN_HEIGHT * 2/5, arcade.color.DARK_BROWN)
    

#Vykreslovanie kociek
def draw_kocky(x, y):
    
    arcade.draw_rectangle_filled(x, y, 35, 35, arcade.color.YELLOW)
    
#Jadro hry
def main():

    #Otvorenie okna
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    #Start renderovania objektov
    arcade.start_render()

    #Vykreslenie funkcii
    draw_pozadie()
    draw_kocky(120, 138)
    

    #Dokoncenie renderovanie po vykresleni vsetkych funkcii
    arcade.finish_render()

    #Zabezpeci chod okna pokial ho niekto nevypne
    arcade.run()



# Spustenie jadra hry
if __name__ == "__main__":
    main()