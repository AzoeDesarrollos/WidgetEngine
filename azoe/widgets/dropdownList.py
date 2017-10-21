from . import BaseWidget, Entry, BaseOpcion
from pygame import Surface, draw, Rect
from pygame.sprite import LayeredDirty
from azoe.engine import color, EventHandler


class DropDownList(BaseWidget):
    lista_de_opciones = None  # LayeredDirty

    def __init__(self, parent, nombre, x, y, w, lista=None):
        super().__init__(parent)
        self.nombre = self.parent.nombre + '.DropDownList.' + nombre
        if lista is None:
            self.lista = []
        else:
            self.lista = lista
        self.x, self.y = x, y
        self.w, self.h = w, 21
        self.entry = Entry(self, nombre, self.x, self.y, w - 18)
        self.flecha = _Flecha(self, 18)

        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.lista_de_opciones = LayeredDirty(*self.crear_lista(self.lista))
        self.ItemActual = ''
        if len(self.lista) == 1:
            self.ItemActual = self.lista[0]
        EventHandler.add_widgets(self.entry, self.flecha)
        self.visible = 0

        if hasattr(self.parent, 'agregar'):
            self.parent.agregar(self)

    def crear_lista(self, items):
        lista = []

        h = 0
        for i, nom in enumerate(items):
            dy = self.h + (i * h) - 19
            opcion = _Opcion(self, nom, self.x + 4, self.y + dy, self.w - 23)
            # opcion.layer = self.layer + 50
            h = opcion.image.get_height() - 1

            lista.append(opcion)

        if len(items) != 0:
            self.set_text(items[0])
        return lista

    def reubicar_en_ventana(self, dx=0, dy=0):
        self.entry.reubicar_en_ventana(dx, dy)
        self.flecha.reubicar_en_ventana(dx, dy)

    def set_text(self, texto):
        self.entry.set_text(texto)
        # acá podría stripearse el texto, si fuera onda Archivo de mapa (*.json)
        # extrayendo solo el .json
        self.ItemActual = texto

    def set_item(self, item):
        self.lista_de_opciones.empty()
        if item not in self.lista:
            self.lista.append(item)
        self.lista_de_opciones.add(*self.crear_lista(self.lista))

        self.set_text(item)

    def get_item_actual(self):
        return self.ItemActual

    def get_item(self, item):
        for opcion in self.lista_de_opciones:
            if hasattr(item, '_nombre'):
                if opcion.texto == item.get_real_name():
                    return opcion

    def del_item(self, item):
        opcion = self.get_item(item)
        self.lista_de_opciones.empty()
        self.entry.borrar_todo()
        self.lista.remove(opcion.texto)

        self.lista_de_opciones.add(*self.crear_lista(self.lista))

    def clear(self):
        self.lista.clear()
        self.entry.borrar_todo()

    def on_destruction(self):
        EventHandler.del_widgets(self.entry, self.flecha)
        self.hide_items()

    def show_items(self):
        for item in self.lista_de_opciones:
            EventHandler.add_widgets(item)

    def hide_items(self):
        for item in self.lista_de_opciones:
            EventHandler.del_widgets(item)

    def on_focus_out(self):
        super().on_focus_out()
        self.hide_items()

    def on_key_down(self, key):
        entry = self.entry.return_text()
        if self.ItemActual in self.lista:
            idx = self.lista.index(self.ItemActual)
            if entry != self.ItemActual:
                self.lista[idx] = entry
                self.lista_de_opciones.get_sprite(idx).set_text(entry)
                self.ItemActual = self.lista[idx]

        self.parent.on_key_down(key)


class _Flecha(BaseWidget):
    def __init__(self, parent, w):
        super().__init__(parent)
        self.nombre = parent.nombre + '.flecha'
        self.w, self.h = w, self.parent.h
        self.x, self.y = self.parent.x + self.parent.w - self.w, self.parent.y
        cf, cb = color('sysScrArrow'), color('sysElmFace')  # cFlecha, cBackground
        cl, cs = color('sysElmLight'), color('sysElmShadow')  # cLuz, cSombra
        self.img_pre = self._biselar(self._crear(self.w, self.h, cf, cb), cs, cl)
        self.img_uns = self._biselar(self._crear(self.w, self.h, cf, cb), cl, cs)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def _crear(w, h, color_flecha, color_fondo):
        imagen = Surface((w, h))
        imagen.fill(color_fondo)
        points = [[4, 7], [w // 2 - 1, h - 9], [w - 6, 7]]
        draw.polygon(imagen, color_flecha, points)
        return imagen

    def on_mouse_down(self, dummy):
        self.image = self.img_pre
        self.parent.show_items()
        self.dirty = 1

    def on_mouse_up(self, dummy):
        self.image = self.img_uns
        self.dirty = 1
        EventHandler.set_focus(self.parent)

    def on_mouse_out(self):
        self.image = self.img_uns
        self.dirty = 1


class _Opcion(BaseOpcion):
    command = None

    def __init__(self, parent, nombre, x, y, w=0):
        super().__init__(parent, nombre, x, y, w)
        self.texto = nombre

    def set_text(self, texto):
        super().set_text(texto)
        self.texto = texto

    def return_text(self):
        self.parent.set_text(self.texto)

    def on_mouse_down(self, button):
        self.return_text()
        self.parent.on_focus_out()

    def on_mouse_in(self):
        super().on_mouse_in()
        self.image = self.img_sel
        self.dirty = 1

    def on_mouse_out(self):
        super().on_mouse_out()
        self.image = self.img_des
        self.dirty = 1
