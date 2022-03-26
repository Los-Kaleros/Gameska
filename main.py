import arcade

#Rozmery + Nazov okna
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Lidl Mario"

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
    draw_kocky(100, 100)
    

    #Dokoncenie renderovanie po vykresleni vsetkych funkcii
    arcade.finish_render()

    #Zabezpeci chod okna pokial ho niekto nevipne 
    arcade.run()



# Spustenie jadra hry
if __name__ == "__main__":
    main()