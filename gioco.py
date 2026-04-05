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
    print(carta.seme, carta.valore)

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
        self.pile_selezionata = None
        self.colonna_originale = None
        self.scarti = []
        
    def trova_posizione(self, carta):
        for i, colonna in enumerate(self.colonne):
            if carta in colonna:
                indice_carta = colonna.index(carta)
                return i, indice_carta
            
        if carta in self.scarti:
            return 7, self.scarti.index(carta)
            
        return None, None
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        
        if 50 < x < 150 and 50 < y < 150:
            if self.mazzo_pesca:
                carta = self.mazzo_pesca.pop()
                carta.scoperta = True
                carta.texture = carta.front_texture
                carta.center_x = 200
                carta.center_y = 100
                self.scarti.append(carta)
                carta.remove_from_sprite_lists()
                self.lista_carte.append(carta)
            return
    
        for carta in reversed(self.lista_carte):
            if carta.collides_with_point((x, y)) and carta.scoperta:
                col, idx = self.trova_posizione(carta)
                if col is None:
                    continue
            
                self.colonna_originale = col

                if col == 7:
                    if idx != len(self.scarti) - 1:
                        return
                    self.pile_selezionata = [self.scarti[idx]]
                else:
                    sequenza = self.colonne[col][idx:]
                    if self.sequenza_valida(sequenza):
                        self.pile_selezionata = sequenza
                    else:
                        return
            
                self.offset_x = self.pile_selezionata[0].center_x - x
                self.offset_y = self.pile_selezionata[0].center_y - y

                for c in self.pile_selezionata:
                    c.remove_from_sprite_lists()
                    self.lista_carte.append(c)
            
                return
            
    def on_mouse_motion(self, x, y, dx, dy):
        if self.pile_selezionata:
            for i, carta in enumerate(self.pile_selezionata):
                carta.center_x = x + self.offset_x
                carta.center_y = (y + self.offset_y) - i * self.spazio_y_carte
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if not self.pile_selezionata:
            return
        
        col_dest = None
        for i in range(7):
            col_x = self.start_x_colonne + i * self.spazio_x_colonne
            if abs(x - col_x) < self.spazio_x_colonne // 2:
                col_dest = i
                break

        if col_dest is None:
            col_dest = self.colonna_originale

        carta_base =  self.pile_selezionata[0]
        col_orig = self.colonna_originale
        
        if not self.mossa_valida(carta_base, self.colonne[col_dest]):
            if col_orig ==7:
                self.scarti.extend(self.pile_selezionata)
                for carta in self.scarti:
                    carta.center_x = 200
                    carta.center_y = 100
            else:
                self.colonne[col_orig].extend(self.pile_selezionata)
                for i, carta in enumerate(self.colonne[col_orig]):
                    carta.center_x = self.start_x_colonne + col_orig * self.spazio_x_colonne
                    carta.center_y = self.start_y_colonne - i * self.spazio_y_carte

            self.pile_selezionata = None
            self.colonna_originale = None
            return

        if col_orig == 7:
            self.scarti = self.scarti[:-len(self.pile_selezionata)]
        else:
            self.colonne[col_orig] = self.colonne[col_orig][:-len(self.pile_selezionata)]
                
        self.colonne[col_dest].extend(self.pile_selezionata)
               
        for i, carta in enumerate(self.colonne[col_dest]):
            carta.center_x = self.start_x_colonne + col_dest * self.spazio_x_colonne
            carta.center_y = self.start_y_colonne - i * self.spazio_y_carte
        
        if col_orig != 7 and len(self.colonne[col_orig]) > 0:
            ultima = self.colonne[col_orig][-1]
            if not ultima.scoperta:
                ultima.scoperta = True
                ultima.texture = ultima.front_texture
                    
        self.pile_selezionata = None
        self.colonna_originale = None
        
    def colore(self, carta):
        if carta.seme in ["heart", "diamond"]:
            return "rosso"
        return "nero"
    
    def mossa_valida(self, carta, colonna_dest):
        if not colonna_dest:
            return carta.valore == 13
        
        top = colonna_dest[-1]
        
        return (
            self.colore(carta) != self.colore(top) and
            carta.valore == top.valore - 1
        )    
    def sequenza_valida(self, sequenza):
        for i in range(len(sequenza)-1):
            c1 = sequenza[i]
            c2 = sequenza[i+1]
            if self.colore(c1) == self.colore(c2) or c1.valore != c2.valore + 1:
                return False
        return True

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
