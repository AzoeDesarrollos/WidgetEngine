from . import SubVentana, BotonAceptarCancelar, Checkbox, Label
from azoe.libs.textrect import render_textrect
from azoe.engine import color
from pygame import font, Rect

__all__ = ['Alerta', 'Pregunta', 'Error', 'Info']


class DialogBox(SubVentana):
    def __init__(self, nombre):
        super().__init__(32 * 8 - 2, 32 * 4, nombre)
        self.nombre = 'DialogBox:' + nombre


class Alerta(DialogBox):
    # layer = 20
    _cerrar = False
    accion_true = None
    accion_false = None
    status = None  # of the checkbox

    def __init__(self, indentifier, texto, accion_si, accion_no):
        super().__init__('Alerta')
        self.identifier = indentifier
        self.accion_true = accion_si
        self.accion_false = accion_no

        fuente = font.SysFont('Verdana', 13)

        self.area = Rect(3, 20, self.w - 6, (fuente.get_height() + 1) * 3)
        x, y, w, h = self.x, self.y, self.area.w, self.area.h + 20

        render = render_textrect(texto, fuente, self.area, (0, 0, 0), color('sysElmFace'))
        self.image.blit(render, self.area)

        self.check = Checkbox(self, False, x + 3, y + h + 13)
        self.status = self.check.state
        Label(self, 'lblChk', x + 3 + 12 + 3, self.check.y - 2, "No mostrar esto nuevamente", fuente=fuente)

        self.btnTrue = BotonAceptarCancelar(self, x + w - (62 * 2) - 12, y + h + 30, self.aceptar)
        self.btnFalse = BotonAceptarCancelar(self, x + w - 62 - 4, y + h + 30, self.cancelar, 'Cancelar')

    def aceptar(self):
        self.accion_true()
        self._cerrar = True

    def cancelar(self):
        self.accion_false()
        self._cerrar = True

    def update(self):
        if self._cerrar:
            self.cerrar()
            return True
        else:
            return False


class Pregunta(DialogBox):
    pass


class Error(DialogBox):
    pass


class Info(DialogBox):
    pass
