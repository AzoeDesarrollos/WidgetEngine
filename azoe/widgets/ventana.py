from azoe.engine import color, EventHandler
from pygame import Rect, Surface
from . import BaseWidget


class Ventana(BaseWidget):
    focusable = False

    def __init__(self, tamanio):
        super().__init__()
        self.rect = Rect((0, 0), tamanio)
        self.nombre = 'ventana'
        self.image = Surface(self.rect.size)
        self.image.fill(color('sysElmFace'))
        EventHandler.add_widgets(self)
        EventHandler.currentFocus = self
