from azoe.libs.textrect import render_textrect
from pygame import font, Rect, Surface
from azoe.engine import color
from . import BaseWidget


class Label(BaseWidget):
    texto = ''

    def __init__(self, parent, nombre, x, y, texto='', fuente=None):
        super().__init__(parent)
        if fuente is None:
            self.fuente = font.SysFont('Verdana', 14)
        else:
            self.fuente = fuente
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + '.Label.' + nombre
        if texto == '':
            self.w, self.h = self.fuente.size(self.texto)
            self.image = Surface((self.w, self.h))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.set_text(texto)

        if hasattr(self.parent, 'agregar'):
            self.parent.agregar(self)

    def set_text(self, texto, fgcolor=None, bgcolor=None):
        if fgcolor is None:
            fgcolor = color('sysElmText')
        if bgcolor is None:
            bgcolor = color('sysElmFace')
        w, h = self.fuente.size(texto)
        rect = Rect(self.x, self.y, w, h + 1)
        self.image = render_textrect(texto, self.fuente, rect, fgcolor, bgcolor)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.w, self.h = self.image.get_size()
        self.dirty = 1
