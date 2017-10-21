from azoe.engine import EventHandler
from . import BaseWidget, Entry


class DataGrid(BaseWidget):
    def __init__(self, parent, nombre, x, y, n_col=3, n_fil=5, cel_w=0, cel_h=21, sep=0):
        super().__init__(parent)
        self.nombre = self.parent.nombre + '.DataGrid.' + nombre
        self.x, self.y = x, y

        fils, cols = 0, 0
        if n_col != 0 and n_fil != 0:
            fils = n_fil
            cols = n_col

        self.celdas = self._crear(fils=fils, cols=cols, celw=cel_w, celh=cel_h, sep=sep)
        for x, y in self.celdas:
            e = self.celdas[x, y]
            EventHandler.add_widgets(e)

        self.h = cel_h * fils + sep * (fils - 1)

    def _crear(self, fils=None, cols=None, celw=None, celh=None, sep=None):
        celdas = {}
        sep_y = -sep
        for oy in range(fils):
            sep_x = -sep
            sep_y += sep
            for ox in range(cols):
                sep_x += sep
                n = 'cel' + str(ox) + ',' + str(oy)
                dx = celw * ox + sep_x
                dy = celh * oy + sep_y

                celdas[ox, oy] = Entry(self, n, self.x + dx, self.y + dy, celw)

        return celdas

    def rellenar(self, datos):
        # try:
            for y in range(len(datos)):
                for x in range(len(datos[y])):
                    self.celdas[x, y].set_text(datos[y][x])
        # except:
        #     pass

    def scroll(self, dy):
        pass

    def reubicar_en_ventana(self, dx=0, dy=0):
        for x, y in self.celdas:
            celda = self.celdas[x, y]
            celda.reubicar_en_ventana(dx, dy)

    def on_destruction(self):
        for x, y in self.celdas:
            e = self.celdas[x, y]
            EventHandler.del_widgets(e)
