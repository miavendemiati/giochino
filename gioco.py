import arcade
import random
import os

LARGHEZZA = 1024
ALTEZZA = 768
TITOLO = "Solitario - TEST"


class Carta(arcade.Sprite):
    def __init__(self, seme, valore, front_filename):
        super().__init__(front_filename, scale=0.25)

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
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for carta in reversed(self.lista_carte):
                if carta.collides_with_point((x, y)) and carta.scoperta:
                    self.carta_selezionata = carta
                    
                    self.offset_x = carta.center_x - x
                    self.offset_y = carta.center_y - y
                    
                    carta.remove_from_sprite_lists()
                    self.lista_carte.append(carta)
                    
                    break
                
    def on_mouse_motion(self, x, y, dx, dy):
        if self.carta_selezionata:
            self.carta_selezionata.center_x = x + self.offset_x
            self.carta_selezionata.center_y = y + self.offset_y
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.carta_selezionata = None               
                
    def setup(self):
        mazzo = crea_mazzo()

        x = 100
        y = 500

        for carta in mazzo[:52]:
            carta.center_x = x
            carta.center_y = y
            carta.scoperta = True
            carta.texture = carta.front_texture
            self.lista_carte.append(carta)
            x += 80

    def on_draw(self):
        self.clear()
        self.lista_carte.draw()


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
