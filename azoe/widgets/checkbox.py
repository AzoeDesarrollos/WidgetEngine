from pygame import Surface, draw
from .basewidget import BaseWidget


class Checkbox(BaseWidget):
    state = False

    def __init__(self, parent, initial_state, x, y):
        super().__init__(parent)
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + ".checkbox"
        self.img_true = self._crear(True)
        self.img_false = self._crear(False)
        self.state = initial_state
        if self.state:
            self.image = self.img_true
        else:
            self.image = self.img_false
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if hasattr(self.parent, 'agregar'):
            self.parent.agregar(self)

    @staticmethod
    def _crear(checked):
        lado = 12
        img = Surface((lado, lado))
        img.fill((255, 255, 255), (1, 1, lado - 2, lado - 2))

        if checked:
            draw.aaline(img, (0, 0, 0), [2, 2], [9, 10])  # \
            draw.aaline(img, (0, 0, 0), [2, 10], [9, 2])  # /

        return img

    def check(self):
        self.state = not self.state
        if self.state:
            self.image = self.img_true
        else:
            self.image = self.img_false
        self.dirty = 1
        self.parent.status = self.state

    def on_mouse_down(self, dummy):
        self.check()
