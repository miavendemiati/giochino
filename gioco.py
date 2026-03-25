import arcade
import random
import os

LARGHEZZA = 1024
ALTEZZA = 700
TITOLO = "Solitario"


class Carta(arcade.Sprite):
    def __init__(self, seme, valore, front_filename):
        super().__init__(front_filename, scale=0.5)

        self.seme = seme
        self.valore = valore

        self.front_texture = arcade.load_texture(front_filename)
        self.back_texture = arcade.load_texture(
            "assets/carte/solitaire/individuals/card_back.png"
        )

        self.scoperta = False
        self.texture = self.back_texture

def crea_mazzo():
    semi = ["heart", "diamond", "club", "spade"]
    nomi = {1: "1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11: "11", 12: "12", 13: "13"}

    mazzo = []

    for seme in semi:
        for valore in range(1, 14):
            nome = nomi.get(valore, str(valore))
            filename = f"assets/carte/solitaire/individuals/{valore}_{seme}.png"
            carta = Carta(seme, valore, filename)
            mazzo.append(carta)
    print(filename)

    random.shuffle(mazzo)
    return mazzo


class Game(arcade.Window):
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, TITOLO)
        arcade.set_background_color(arcade.color.AMAZON)
        self.lista_carte = arcade.SpriteList()
        self.carta_selezionata = None
        self.offset_x = 0
        self.offset_y = 0
        self.colonne = []
        self.spazio_x_colonne = 140
        self.start_x_colonne = 100
        self.start_y_colonne = 650
        self.spazio_y_carte = 30
        
    def trova_posizione(self, carta):
        for i, colonna in enumerate(self.colonne):
            if carta in colonna:
                indice_carta = colonna.index(carta)
                return i, indice_carta
            if carta in self.scarti:
                return 7, self.scarti.index(carta)
            
        return None, None
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for carta in reversed(self.lista_carte):
                if carta.collides_with_point((x, y)) and carta.scoperta:
                    self.carta_selezionata = carta
                    
                    col, idx = self.trova_posizione(carta)
                    print(col, idx)
                    self.pile_selezionata = self.colonne[col][idx:]
                    self.colonna_originale = col
                    if col == 7:
                        self.pile_selezionata = self.scarti[idx:]
                    
                    self.offset_x = self.pile_selezionata[0].center_x - x
                    self.offset_y = self.pile_selezionata[0].center_y - y
                    
                    for carta in self.pile_selezionata:          
                        carta.remove_from_sprite_lists()
                        self.lista_carte.append(carta)
                    
            for carta in reversed(self.lista_carte):
                if carta.collides_with_point((x, y)) and carta.scoperta:
                    self.carta_selezionata = carta
                    self.pile_selezionata = [carta]
                    self.offset_x = carta.center_x - x
                    self.offset_y = carta.center_y - y
                    
                    break

            print(len(self.mazzo_pesca))
            if 60 < x < 140 and 60 < y < 140:
                if self.mazzo_pesca:
                    carta = self.mazzo_pesca.pop()

                    carta.scoperta = True
                    carta.texture = carta.front_texture

                    self.scarti.append(carta)
                    
                    carta.remove_from_sprite_lists()
                    self.lista_carte.append(carta)

                    carta.center_x = 200
                    carta.center_y = 100

                    if carta not in self.lista_carte:
                        self.lista_carte.append(carta)
                else:
                    self.mazzo_pesca = self.scarti[::-1]
                    self.scarti = []
                    
                    for carta in self.mazzo_pesca:
                        carta.scoperta =  False
                        carta.texture = carta.back_texture
                        carta.center_x = 100
                        carta.center_y = 100
                            
    def on_mouse_motion(self, x, y, dx, dy):
        if self.pile_selezionata:
            for i, carta in enumerate(self.pile_selezionata):
                carta.center_x = x + self.offset_x
                carta.center_y = (y + self.offset_y) - i * self.spazio_y_carte
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.carta_selezionata = None

        if not self.pile_selezionata:
            return
        
        if col_dest > 6:  # se proviene dagli scarti
            self.scarti = self.scarti[:-len(self.pile_selezionata)]
        else:
            self.colonne[self.colonna_originale] = self.colonne[self.colonna_originale][:-len(self.pile_selezionata)]
        
        col_dest = int((x - self.start_x_colonne + self.spazio_x_colonne // 2) / self.spazio_x_colonne)         
        col_dest = max(0, min(6, col_dest))  # limita tra 0 e 6 colonne
        self.colonne[self.colonna_originale] = self.colonne[self.colonna_originale][:-len(self.pile_selezionata)]
        self.colonne[col_dest].extend(self.pile_selezionata)
        
        for i, carta in enumerate(self.colonne[col_dest][-len(self.pile_selezionata):]):
            carta.center_x = self.start_x_colonne + col_dest * self.spazio_x_colonne
            carta.center_y = self.start_y_colonne - (len(self.colonne[col_dest]) - len(self.pile_selezionata) + i) * self.spazio_y_carte

        colonna = self.colonne[self.colonna_originale]

        if len(colonna) >0:
            ultima = colonna[-1]

            if not ultima.scoperta:
                ultima.scoperta = True
                ultima.texture = ultima.front_texture

        self.colonna_originale = None
        self.pile_selezionata = None

    def setup(self):
        print("inizio setup")
        self.lista_carte = arcade.SpriteList()
        self.colonne = []
        self.scarti = []
        
        mazzo = crea_mazzo()

        for i in range(7):
            colonna = []
            
            for j in range(i + 1):
                carta = mazzo.pop()
                
                carta.center_x = self.start_x_colonne + i * self.spazio_x_colonne
                carta.center_y = self.start_y_colonne - j * self.spazio_y_carte
                
                if j == i:
                    carta.scoperta = True
                    carta.texture = carta.front_texture
                    
                else:
                    carta.scoperta = False
                    carta.texture = carta.back_texture
                
                self.lista_carte.append(carta)
                colonna.append(carta)
                
            self.colonne.append(colonna)
        
        self.mazzo_pesca = mazzo
        
        
        for i, carta in enumerate(self.mazzo_pesca):
            carta.scoperta = False
            carta.texture = carta.back_texture
            carta.center_x = 100
            carta.center_y = 100
            carta.remove_from_sprite_lists()
            self.lista_carte.append(carta)

        x = 100
        y = 500

        # for carta in mazzo[:52]:
        #     carta.center_x = x
        #     carta.center_y = y
        #     carta.scoperta = True
        #     carta.texture = carta.front_texture
        #     self.lista_carte.append(carta)
        #     x += 80

    def on_draw(self):
        self.clear()
        self.lista_carte.draw()
    
    print("fine setup")


def main():
    print("PARTITO")
    game = Game()
    print("CREATO")
    game.setup()
    print("SETUP FATTO")
    arcade.run()


if __name__ == "__main__":  
    main()
