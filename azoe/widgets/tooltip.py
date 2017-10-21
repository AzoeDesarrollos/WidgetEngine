from pygame import Surface, font, display
from azoe.engine import color  # , EventHandler
from .basewidget import BaseWidget


class ToolTip(BaseWidget):
    focusable = False
    aparicion = -1

    def __init__(self, parent, mensaje, x, y):
        super().__init__(parent)
        self.x, self.y = x, y
        self.mensaje = mensaje
        self.nombre = self.parent.nombre + '.ToolTip'
        # self.layer = self.parent.layer
        self.image = self._crear(mensaje)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.w, self.h = self.rect.size
        w = display.get_surface().get_size()[0]
        self._ajustar(w)
        # if self.nombre not in EventHandler.widgets:
        #     EventHandler.add_widget(self)

    @staticmethod
    def _crear(texto):
        fuente = font.SysFont("tahoma", 11)
        fg_color = color('sysElmText')
        bg_color = color('sysMenBack')
        w, h = fuente.size(texto)
        fondo = Surface((w + 4, h + 2))
        fondo.fill(bg_color, (1, 1, w + 2, h))
        render = fuente.render(texto, True, fg_color, bg_color)
        fondo.blit(render, (2, 1))
        return fondo

    def _ajustar(self, ancho):
        while True:
            if self.rect.x + self.w > ancho:
                self.rect.x -= 1
            else:
                self.rect.y = self.parent.y + self.h + 16
                break

    def show(self, delay=20):
        self.aparicion += 1
        if self.mensaje != '':
            if self.aparicion >= delay:
                alpha = self.image.get_alpha()
                self.image.set_alpha(alpha + 60)
        self.dirty = 1

    def hide(self):
        self.image.set_alpha(0)
        # self.i = -1
        self.dirty = 1
