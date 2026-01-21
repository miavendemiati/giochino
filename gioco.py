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
    
def main():
        Game(larghezza, altezza, titolo)
        arcade.run()
        
if __name__ == "__main__":
        main()
        
        