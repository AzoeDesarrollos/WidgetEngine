from azoe.libs.textrect import render_textrect
from azoe.engine.colores import color
from pygame import Rect, font, mouse
from . import Marco, BotonCerrar
from globales import ANCHO, ALTO


class SubVentana(Marco):
    pressedTitle = False

    def __init__(self, w, h, nombre, titular=True):
        _r = Rect(0, 0, w, h)
        _r.center = Rect(0, 0, ANCHO, ALTO).center
        x, y = _r.topleft
        super().__init__(x, y, w, h)
        self.px, self.py = self.rect.topleft
        if titular:
            self.titular(nombre)
        BotonCerrar(self, x + w - 18, y + 3, 13, 15, 'Cerrar', self.cerrar)

    def titular(self, texto):
        fuente = font.SysFont('verdana', 12)
        rect = Rect(2, 2, self.w - 6, fuente.get_height() + 1)
        render = render_textrect(texto, fuente, rect, color('sysBoxBack'), color('sysMenText'))
        self.image.blit(render, rect)

    def on_mouse_over(self):
        if self.pressedTitle:
            abs_x, abs_y = mouse.get_pos()
            new_x, new_y = abs_x - self.x, abs_y - self.y

            dx = new_x - self.px
            dy = new_y - self.py
            if dx or dy:
                self.reubicar_en_ventana(dx, dy)

    def on_mouse_down(self, button):
        x, y = mouse.get_pos()
        rect = Rect(self.x + 2, self.y + 2, self.w - 4, 17)
        if rect.collidepoint(x, y):
            self.pressedTitle = True

            self.px = x - self.x
            self.py = y - self.y

    def on_mouse_up(self, button):
        self.pressedTitle = False

    def on_mouse_out(self):
        if not self.pressedTitle:
            super().on_mouse_out()
