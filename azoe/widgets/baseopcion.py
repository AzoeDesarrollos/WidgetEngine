from . import BaseWidget
from pygame import font, Rect, Surface
from azoe.engine import color


class BaseOpcion(BaseWidget):
    def __init__(self, parent, nombre, x, y, w=0, h=14):
        super().__init__(parent)
        self.x, self.y = x, y
        self.font_h = h
        self.nombre = self.parent.nombre + '.Opcion:' + nombre
        self.img_des = self.crear(nombre, color('sysElmText'), color('sysMenBack'), w)
        self.img_sel = self.crear(nombre, color('sysElmText'), color('sysBoxSelBack'), w)
        self.image = self.img_des
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def crear(nombre, fgcolor, bgcolor, w=0, h=14):
        fuente = font.SysFont('Courier new', h)
        if w == 0:
            w, h = fuente.size(nombre)

        rect = Rect(0, 0, w, h)
        render = fuente.render(nombre, True, fgcolor, bgcolor)
        image = Surface(rect.size)
        image.fill(bgcolor)
        image.blit(render, rect)

        return image

    def set_text(self, text):
        self.nombre = self.parent.nombre + '.Opcion.' + text
        self.img_des = self.crear(text, color('sysElmText'), color('sysMenBack'), self.w)
        self.img_sel = self.crear(text, color('sysElmText'), color('sysBoxSelBack'), self.w)
        self.image = self.img_des
        self.dirty = 1
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
