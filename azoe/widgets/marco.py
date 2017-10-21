from azoe.engine import color, EventHandler
from pygame.sprite import LayeredDirty
from pygame import Surface
from . import BaseWidget


class Marco(BaseWidget):
    contenido = None
    indexes = []
    doc_w = None
    doc_h = None
    BORDER_STYLE_RAISED = 'raised'
    BORDER_STYLE_SUNKEN = 'sunken'

    def __init__(self, x, y, w, h, borde=BORDER_STYLE_RAISED, parent=None):
        self.contenido = LayeredDirty()
        super().__init__(parent)
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.image = Surface((self.w, self.h))
        self.image.fill(color('sysElmFace'))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        EventHandler.add_widgets(self)
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        if borde == self.BORDER_STYLE_RAISED:
            self.image = self._biselar(self.image, luz, sombra)
        elif borde == self.BORDER_STYLE_SUNKEN:
            self.image = self._biselar(self.image, sombra, luz)

    def reubicar_en_ventana(self, dx=0, dy=0):
        for widget in self.contenido:
            widget.reubicar_en_ventana(dx, dy)
        super().reubicar_en_ventana(dx, dy)

    def agregar(self, *objetos):
        for item in objetos:
            self.contenido.add(item)
            EventHandler.add_widgets(item)

    def quitar(self, objeto):
        if objeto in self.contenido:
            self.contenido.remove(objeto)
            EventHandler.del_widgets(objeto)
        else:
            raise IndexError('El objeto ' + objeto.nombre + ' no pertenece a este marco')

    def limpiar(self):
        for objeto in self.contenido:
            self.quitar(objeto)

    def cerrar(self):
        EventHandler.del_widgets(self)

    def devolver(self, objeto):
        if objeto in self.contenido:
            raise IndexError('El objeto ' + objeto.nombre + ' no pertenece a este marco')
        else:
            for sprite in self.contenido.sprites():
                if sprite == objeto:
                    return sprite

    def __contains__(self, item):
        if item in self.contenido:
            return True
        else:
            return False

    def on_destruction(self):
        for widget in self.contenido:
            self.quitar(widget)
            if hasattr(widget, 'tooltip'):
                if widget.tooltip is not None:
                    EventHandler.del_widgets(widget.tooltip)
