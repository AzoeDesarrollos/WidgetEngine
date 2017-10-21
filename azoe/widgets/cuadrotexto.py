from pygame import font, Rect, Surface, mouse, draw, cursors
from azoe.libs.textrect import render_textrect
from pygame import K_RETURN, K_BACKSPACE
from azoe.engine import color
from . import BaseWidget


class CuadroTexto(BaseWidget):
    texto = []
    idx = 0
    seleccion = None
    setFocus_onIn = True

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)
        self.nombre = self.parent.nombre + '.CuadroTexto'
        self.fuente = font.SysFont('courier new', 14)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cursor = ("        ",
                       "ooo ooo ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "   o    ",
                       "ooo ooo ")
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.image = Surface(self.rect.size)
        self.image.fill(color('sysBoxBack'))
        draw.rect(self.image, (0, 0, 0), (0, 0, self.w, self.h), 1)

    def ingresar_caracter(self, char):
        index = self.idx
        if self.seleccion is not None:
            self.borrar_seleccion()
        self.texto.insert(index, char)

    def borrar_seleccion(self):
        pass

    def on_mouse_over(self):
        if self.hasFocus:
            text = self.cursor
            curs, mask = cursors.compile(text, 'o', 'o')
            mouse.set_cursor([8, 16], [4, 1], curs, mask)
            # if self.seleccionando:
            #    self.sel_end = self.get_x()[1]
            #    self.seleccionar()

    def on_mouse_out(self):
        super().on_mouse_out()
        mouse.set_cursor(*cursors.arrow)

    def on_key_down(self, event):
        if event.key == K_RETURN:
            self.texto.append('\n')
        elif event.key == K_BACKSPACE:
            del self.texto[-1]
        else:
            self.texto.append(event.unicode)

    def update(self):
        texto = ''.join(self.texto)
        # h = self.fuente.get_height()
        fg = color('sysElmText')
        bg = color('sysBoxBack')
        # sg = color('sysBoxSelBack')
        # seleccion = Rect(8*32,h,8*10,h)

        # string, font, rect, text_color, background_color
        render = render_textrect(texto, self.fuente, self.rect, fg, bg)
        # selected = render_textrect(texto,self.fuente,self.rect,fg,sg).subsurface(seleccion)
        # selected.set_clip(seleccion)
        # render.blit(selected,seleccion)
        self.image.blit(render, (0, 0))

    def scroll(self, dx=0, dy=0):
        pass
