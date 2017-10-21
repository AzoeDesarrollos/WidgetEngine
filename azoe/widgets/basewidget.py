from pygame.sprite import DirtySprite
from pygame import draw


class BaseWidget(DirtySprite):
    """clase base para todos los widgets"""
    focusable = True
    # si no es focusable, no se le llaman focusin y focusout
    # (por ejemplo, un contenedor, una etiqueta de texto)
    hasFocus = False
    # indica si el widget está en foco o no.
    enabled = True
    # un widget con enabled==False no recibe ningun evento
    nombre = ''
    # identifica al widget en el renderer
    hasMouseOver = False
    # indica si el widget tuvo el mouse encima o no, por el onMouseOut
    opciones = None
    # las opciones con las que se inicializo
    setFocus_onIn = False
    # if True: Renderer.setFocus se dispara onMouseIn también.
    KeyCombination = ''

    layer = 0
    rect = None
    x, y, w, h = 0, 0, 0, 0

    def __init__(self, parent=None):
        if parent is not None:
            self.parent = parent
            # self.layer = self.parent.layer + 1
        super().__init__()

    def on_focus_in(self):
        self.hasFocus = True

    def on_focus_out(self):
        self.hasFocus = False

    def on_mouse_down(self, mousedata):
        pass

    def on_mouse_up(self, mousedata):
        pass

    def on_mouse_over(self):
        pass

    def on_mouse_in(self):
        self.hasMouseOver = True

    def on_mouse_out(self):
        self.hasMouseOver = False

    def on_key_down(self, keydata):
        pass

    def on_key_up(self, keydata):
        pass

    def on_destruction(self):
        # esta funcion se llama cuando el widget es quitado del renderer.
        pass

    @staticmethod
    def _biselar(imagen, color_luz, color_sombra):
        w, h = imagen.get_size()
        draw.line(imagen, color_sombra, (0, h - 2), (w - 1, h - 2), 2)
        draw.line(imagen, color_sombra, (w - 2, h - 2), (w - 2, 0), 2)
        draw.lines(imagen, color_luz, 0, [(w - 2, 0), (0, 0), (0, h - 4)], 2)
        return imagen

    def reubicar_en_ventana(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)
        self.x += dx
        self.y += dy
        self.dirty = 1

    def __repr__(self):
        return self.nombre

    def is_visible(self):
        return self._visible
