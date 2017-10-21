from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
from pygame import K_ESCAPE, QUIT, K_F1, K_F2, K_RCTRL, K_LCTRL, K_RALT, K_LALT, key
from pygame.sprite import LayeredDirty


class EventHandler:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    control = False
    alt = False
    key = None

    @classmethod
    def add_widgets(cls, *widgets):
        for widget in widgets:
            if widget not in cls.contents:
                cls.contents.add(widget, layer=widget.layer)
                cls.widgets[widget.nombre] = widget

    @classmethod
    def del_widgets(cls, *widgets):
        for widget in widgets:
            if isinstance(widget, str):
                widget = cls.widgets[widget]
            widget.on_destruction()
            cls.contents.remove(widget)
            if widget.nombre in cls.widgets:
                del cls.widgets[widget.nombre]

    @classmethod
    def get_widget(cls, widget):
        if isinstance(widget, str):  # suponemos que es su nombre
            widget = cls.widgets[widget]
        return widget

    @classmethod
    def set_focus(cls, widget):
        if widget != cls.currentFocus and widget is not None:
            if cls.currentFocus is not None:
                cls.currentFocus.on_focus_out()
            cls.currentFocus = widget
            cls.currentFocus.on_focus_in()

    @classmethod
    def update(cls, events, fondo):
        cls.key = None
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_RCTRL or event.key == K_LCTRL:
                    cls.control = True
                elif event.key == K_LALT:
                    cls.alt = True
                elif event.key == K_RALT:
                    cls.control = True
                    cls.alt = True
                elif event.key == K_ESCAPE:
                    return False
                elif event.key == K_F1:
                    i = 0
                    print('--Inicio de lista')
                    for widget in cls.contents:
                        i += 1
                        print(widget.nombre)
                    print('--Fin de lista')
                    print('Nº Total de widgets: ' + str(i))
                elif event.key == K_F2:
                    print('--Inicio de lista')
                    layers = cls.contents.layers()
                    for idx in layers:
                        print('\n--Widgets en layer ' + str(idx))
                        sprites = cls.contents.get_sprites_from_layer(idx)
                        for widget in sprites:
                            print(widget.nombre)
                    print('--Fin de lista')
                else:
                    cls.key = key.name(event.key)
                cls.currentFocus.on_key_down(event)

            elif event.type == KEYUP:
                if event.key == K_RCTRL or event.key == K_LCTRL:
                    cls.control = False
                elif event.key == K_LALT:
                    cls.alt = False
                elif event.key == K_RALT:
                    cls.control = False
                    cls.alt = False
                else:
                    cls.currentFocus.on_key_up(event)

            elif event.type == MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    found_widget = None
                    for widget in cls.contents:
                        if widget.is_visible():
                            if widget.rect.collidepoint(event.pos):
                                if widget.focusable:
                                    found_widget = widget

                    cls.set_focus(found_widget)

                if cls.currentFocus.enabled:
                    cls.currentFocus.on_mouse_down(event.button)

            elif event.type == MOUSEBUTTONUP:
                cls.currentFocus.on_mouse_up(event.button)

            elif event.type == MOUSEMOTION:
                for widget in cls.contents:
                    if widget.rect.collidepoint(event.pos):
                        if not widget.hasMouseOver:
                            widget.on_mouse_in()
                            if widget.setFocus_onIn:
                                cls.set_focus(widget)
                    else:
                        if widget.hasMouseOver:
                            widget.on_mouse_out()

        # top = cls.contents.get_top_layer()
        # print(cls.contents.get_sprites_from_layer(top))
        for widget in cls.contents:
            if widget.hasMouseOver:
                widget.on_mouse_over()

        cls.contents.update()
        return cls.contents.draw(fondo)
