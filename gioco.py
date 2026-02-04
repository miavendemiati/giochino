import arcade
import random
import math

larghezza = 1024
altezza = 768
titolo = "solitario"



class Game(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = None
        self.lista_background = arcade.SpriteList()
        self.carte = None
        self.mat = None
        self.lista_carte = arcade.SpriteList()
        self.lista_mat = arcade.SpriteList()
        
        self.setup()
        
    def sfondo(self):
        arcade.set_background_color(arcade.color.AMAZON)
    
    def setup(self):
        self.sfondo()
               
    def on_draw(self):
        self.clear()
        self.lista_carte.draw()
        self.lista_mat.draw()
        
    def on_mouse_press(self, x, y, button, key_modifiers):
        pass
    
    def on_mouse_release(self, x: float, y: float, dx: float, dy: float):
        pass
    
class Carta(arcade.Sprite):
    def __init__(self, seme, valore, filename, scala = 0.5):
        super().__init__(filename, scala)
        self.seme = seme
        self.valore = valore
        
        self.front_texture = arcade.load_texture
        self.back_texture = arcade.load_texture("giochino/assets/card_back.png")
        
        self.scoperta = False
        self.texture = self.back_texture
    
    def colore(self):
        if self.seme in ["cuori", "quadri"]:
            return "rosso"
        return "nero"
    
def crea_mazzo():
    semi = ["cuori", "quadri", "fiori", "picche"]
    nomi = {
        1: "asso",
        11: "jack",
        12: "regina",
        13: "re"
    }
        
    mazzo = []
    
    for seme in semi:
        for valore in range(1, 14):
                nome = nomi.get(valore, str(valore))
                filename = f"assets/carte/{nome}_{seme}.png"
                carta = Carta(seme, valore, filename)
                mazzo.append(carta)
    
    random.shuffle(mazzo)
    return mazzo
    
def setup(self):
    self.sfondo()
    self.lista_carte = arcade.SpriteList()
    
    mazzo = crea_mazzo()   
    print(len(mazzo)) 
    
    x = 100
    y = 600
    
    for carta in mazzo:
        carta.center_x = x
        carta.center_y = y
        self.lista_carte.apend(carta)
        x += 0.5
    
    
def main():
        Game(larghezza, altezza, titolo)
        arcade.run()
        
if __name__ == "__main__":
        main()
        
        