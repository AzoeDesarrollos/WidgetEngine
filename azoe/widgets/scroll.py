from pygame import Rect, Surface, mouse, draw
from azoe.engine import color, EventHandler
from . import BaseWidget


class BaseScroll(BaseWidget):
    nombre = ''
    parent = None
    cursor = None
    BtnPos = None  # derecha, o abajo
    BtnNeg = None  # izquierda, o arriba

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.image = self._crear(self.w, self.h)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if hasattr(self.parent, 'agregar'):
            self.parent.agregar(self)

    @staticmethod
    def _crear(w, h):
        imagen = Surface((w, h))
        imagen.fill(color('sysScrBack'))
        return imagen

    def on_destruction(self):
        EventHandler.del_widgets(self.cursor, self.BtnPos, self.BtnNeg)

    def reubicar_en_ventana(self, dx=0, dy=0):
        # super().reubicar_en_ventana(dx, dy)
        # self.cursor.reubicar_en_ventana(dx, dy)
        # self.BtnPos.reubicar_en_ventana(dx, dy)
        # self.BtnNeg.reubicar_en_ventana(dx, dy)
        for obj in [super(), self.cursor, self.BtnNeg, self.BtnPos]:
            obj.reubicar_en_ventana(dx, dy)


class ScrollV(BaseScroll):
    def __init__(self, parent, x, y, w=16):
        super().__init__(parent, x, y + 12, w, parent.h - 12 * 2)
        self.nombre = self.parent.nombre + '.ScrollV'
        self.area = Rect(0, 0, self.w, self.h)
        self.BtnPos = BotonVertical(self, self.rect.bottom, 'abajo')
        self.BtnNeg = BotonVertical(self, self.y - 12, 'arriba')
        self.cursor = CursorV(self, parent, self.x, self.y, 16)

    def actualizar_tamanio(self, doc_h):
        win_h = 480
        self_h = self.area.h

        h = (win_h * self_h) // doc_h
        if h == self_h:
            h = 0

        self.cursor.velocidad = (doc_h - win_h) / (self_h - h)

        self.cursor.actualizar_tamanio(self.cursor.w, h)


class ScrollH(BaseScroll):
    def __init__(self, parent, x, y, h=16):
        super().__init__(parent, x + 12, y, parent.w - 12 * 2, h)
        self.nombre = self.parent.nombre + '.ScrollH'
        self.area = Rect(0, 0, self.w, self.h)
        self.BtnPos = BotonHorizontal(self, self.rect.right, 'derecha')
        self.BtnNeg = BotonHorizontal(self, self.x - 12, 'izquierda')
        self.cursor = CursorH(self, parent, self.x, self.y, 16)

    def actualizar_tamanio(self, doc_w):
        win_w = 480
        self_w = self.area.w

        w = (win_w * self_w) // doc_w
        if w == self_w:
            w = 0

        self.cursor.velocidad = (doc_w - win_w) / (self_w - w)

        self.cursor.actualizar_tamanio(w, self.cursor.h)


class BaseScrollCursor(BaseWidget):
    parent = None
    pressed = False
    dx, dy = 0, 0
    velocidad = 0
    image = None
    px, py = 0, 0

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.crear(w, h)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.pressed = False

    def _agregar_barras(self, *args):
        pass

    def crear(self, w, h):
        cf, cl, cs = color('sysElmFace'), color('sysElmLight'), color('sysElmShadow')
        self.image = self._biselar(self._agregar_barras(self._crear(w, h, cf), cl, cs), cl, cs)
        self.dirty = 1

    def _arrastrar(self):
        abs_x, abs_y = mouse.get_pos()
        new_x, new_y = abs_x - self.x, abs_y - self.y

        dx = new_x - self.px
        dy = new_y - self.py

        self.dx = dx
        self.dy = dy

    @staticmethod
    def _crear(w, h, _color):
        imagen = Surface((w, h))  # crear la base absoluta
        imagen.fill(_color)
        return imagen

    def actualizar_tamanio(self, new_w, new_h):
        self.w, self.h = new_w, new_h
        self.crear(new_w, new_h)
        self.rect.size = new_w, new_h

    def on_mouse_down(self, button):
        if button == 1:
            x, y = mouse.get_pos()
            self.px = x - self.x
            self.py = y - self.y
            self.pressed = True

    def on_mouse_up(self, button):
        if button == 1:
            self.pressed = False

    def update(self):
        self.dx, self.dy = 0, 0


class CursorH(BaseScrollCursor):
    def __init__(self, parent, scrollable, x, y, w, h=16):
        super().__init__(parent, x, y, w, h)
        self.nombre = parent.nombre + '.CursorH'
        self.scrollable = scrollable
        self.rel_rect = Rect((0, 0), (self.w, 2))
        EventHandler.add_widgets(self)

    @staticmethod
    def _agregar_barras(imagen, c1, c2):
        """Agrega 6 barritas de "agarre" verticales"""
        w, h = imagen.get_size()
        for i in range(-4, 3, 1):
            if i % 2 != 0:
                _color = c1
            else:
                _color = c2
            draw.line(imagen, _color, (w // 2 + i, 2), (w // 2 + i, h - 4))
        return imagen

    def actualizar_tamanio(self, new_w, new_h):
        super().actualizar_tamanio(new_w, new_h)
        self.rel_rect.w = new_w

    def mover(self):
        dx = self.dx
        opuesto = 0
        if dx > 0:
            opuesto = -1
        elif dx < 0:
            opuesto = +1
        while True:
            if self.parent.area.contains(self.rel_rect.move(dx, 0)):
                self.rect.x += dx
                self.rel_rect.x += dx
                self.x += dx
                self.dirty = 1
                break
            else:
                dx += opuesto

        self.scrollable.scroll(dx=round(dx * self.velocidad))

    def update(self):
        super().update()
        if self.pressed:
            self._arrastrar()
            if self.dx != 0:
                self.mover()


class CursorV(BaseScrollCursor):
    def __init__(self, parent, scrollable, x, y, h, w=16):
        super().__init__(parent, x, y, w, h)
        self.nombre = parent.nombre + '.CursorV'
        self.scrollable = scrollable
        self.rel_rect = Rect((0, 0), (2, self.h))
        EventHandler.add_widgets(self)

    @staticmethod
    def _agregar_barras(imagen, c1, c2):
        """Agrega 6 barritas de "agarre" horizontales"""
        w, h = imagen.get_size()
        for i in range(-4, 3, 1):
            if i % 2 != 0:
                color_linea = c1
            else:
                color_linea = c2
            draw.line(imagen, color_linea, (2, h // 2 + i), (w - 4, h // 2 + i))
        return imagen

    def actualizar_tamanio(self, new_w, new_h):
        super().actualizar_tamanio(new_w, new_h)
        self.rel_rect.h = new_h

    def mover(self):
        dy = self.dy
        opuesto = 0
        if dy > 0:
            opuesto = -1
        elif dy < 0:
            opuesto = +1

        while True:
            if self.parent.area.contains(self.rel_rect.move(0, dy)):
                self.rect.y += dy
                self.rel_rect.y += dy
                self.y += dy
                self.dirty = 1
                break
            else:
                dy += opuesto

        self.scrollable.scroll(dy=round(dy * self.velocidad))

    def update(self):
        super().update()
        if self.pressed:
            self._arrastrar()
            if self.dy != 0:
                self.mover()


class BaseScrollBoton(BaseWidget):
    nombre = ''
    parent = None
    pressed = False
    w, h = 0, 0

    def __init__(self, parent, x, y, orientacion):
        super().__init__(parent)
        self.pressed = False
        self.orientacion = orientacion
        self.x, self.y = x, y
        luz, sombra = color('sysElmLight'), color('sysElmShadow')
        self.img_pre = self._biselar(self._crear(self.w, self.h, self.orientacion), sombra, luz)
        self.img_uns = self._biselar(self._crear(self.w, self.h, self.orientacion), luz, sombra)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.nombre = self.parent.nombre + '.Btn.' + self.orientacion

    def _crear(self, *args, **kwargs):
        pass

    def deselect(self):
        self.image = self.img_uns
        self.dirty = 1

    def press(self):
        self.image = self.img_pre
        self.pressed = True
        self.dirty = 1

    def on_mouse_down(self, dummy):
        if self.enabled:
            self.press()

    def on_mouse_up(self, dummy):
        self.pressed = False
        self.deselect()

    def update(self):
        # if self.pressed:
        #    self.serPresionado()
        self.enabled = self.parent.enabled


class BotonVertical(BaseScrollBoton):
    def __init__(self, parent, y, orientacion):
        self.w, self.h = parent.w, 12
        super().__init__(parent, parent.x, y, orientacion)
        EventHandler.add_widgets(self)

    @staticmethod
    def _crear(w, h, orientacion):
        imagen = Surface((w, h))
        imagen.fill(color('sysElmFace'))
        points = []

        if orientacion == 'arriba':
            points = [[3, h - 4], [w // 2 - 1, 2], [w - 5, h - 4]]
        elif orientacion == 'abajo':
            points = [[3, 4], [w // 2 - 1, h - 4], [w - 5, 4]]

        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen

    def press(self):
        super().press()
        if self.orientacion == 'arriba':
            self.parent.cursor.dy = -1
        elif self.orientacion == 'abajo':
            self.parent.cursor.dy = +1
        self.parent.cursor.mover()


class BotonHorizontal(BaseScrollBoton):
    def __init__(self, parent, x, orientacion):
        self.w, self.h = 12, parent.h
        super().__init__(parent, x, parent.y, orientacion)
        EventHandler.add_widgets(self)

    @staticmethod
    def _crear(w, h, orientacion):
        imagen = Surface((w, h))
        imagen.fill(color('sysElmFace'))
        points = []

        if orientacion == 'derecha':
            points = [[4, 3], [w - 4, h // 2 - 1], [4, h - 5]]
        elif orientacion == 'izquierda':
            points = [[w - 5, 3], [3, h // 2 - 1], [w - 5, h - 5]]

        draw.polygon(imagen, color('sysScrArrow'), points)
        return imagen

    def press(self):
        super().press()
        if self.orientacion == 'izquierda':
            self.parent.cursor.dx = -1
        elif self.orientacion == 'derecha':
            self.parent.cursor.dx = +1
        self.parent.cursor.mover()
