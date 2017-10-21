from pygame import Rect


class Portapapeles:
    items = []
    _item = None
    _tipo = None

    @classmethod
    def put(cls, mode, *items):
        if len(items):
            if mode == 'cut':
                cls.items.append(CutCluster(mode, *items))
            elif mode == 'copy':
                cls.items = [CopyCluster(mode, *items)]

    @classmethod
    def take(cls, destino):
        if len(cls.items):
            if cls.items[-1].mode == 'cut':
                cluster = cls.items.pop()
                cls.items.clear()
            else:
                cluster = cls.items[-1]

            destino.paste(cluster)


class Element:
    relative_center = 0, 0

    def __init__(self, item):
        self.item = item
        if hasattr(item, 'texto'):
            self.item_type = 'text'
        elif type(self.item) is dict:
            self.item_type = 'dict'
        else:
            self.item_type = 'object'

    def paste(self, x, y):
        if self.item_type == 'dict':
            self.item['rect'].centerx = self.relative_center[0] + x
            self.item['rect'].centery = self.relative_center[1] + y

        elif self.item_type == 'object':
            self.item.rect.centerx = self.relative_center[0] + x
            self.item.rect.centery = self.relative_center[1] + y


class MetaCluster:
    mode = ''
    elements = None

    @staticmethod
    def get_relative_positions(bigrect, items):
        elements = []
        for item in items:
            element = Element(item)
            if element.item_type == 'dict':
                rect = element.item['rect']
            else:
                rect = element.item.rect

            if bigrect.right < rect.centerx:
                bigrect.w += rect.centerx - bigrect.right

            if bigrect.bottom < rect.centery:
                bigrect.h += rect.centery - bigrect.bottom

            element.relative_center = [rect.centerx - bigrect.left,
                                       rect.centery - bigrect.top]

            elements.append(element)

        return bigrect, elements

    def __repr__(self):
        return self.mode.title() + 'Cluster (' + str(len(self.elements)) + ' items)'


class CutCluster(MetaCluster):
    def __init__(self, mode, *items):
        self.mode = mode

        topmost = min(items, key=lambda item: item.rect.centery)
        leftmost = min(items, key=lambda item: item.rect.centerx)
        bigrect = Rect(leftmost.rect.centerx, topmost.rect.centery, 1, 1)
        self.rect, self.elements = self.get_relative_positions(bigrect, items)


class CopyCluster(MetaCluster):
    def __init__(self, mode, *items):
        self.mode = mode

        topmost = min(items, key=lambda item: item['rect'].centery)
        leftmost = min(items, key=lambda item: item['rect'].centerx)
        bigrect = Rect(leftmost['rect'].centerx, topmost['rect'].centery, 1, 1)
        self.rect, self.elements = self.get_relative_positions(bigrect, items)
