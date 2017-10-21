from pygame import mask, Surface, PixelArray


def serialize(surf):
    mascara = mask.from_threshold(surf, (255, 0, 255), (1, 1, 1, 255))
    w, h = mascara.get_size()
    serial = str(w) + ',' + str(h) + '!'
    for y in range(h):
        for x in range(w):
            serial += str(mascara.get_at([x, y]))
    return serial


def encode(input_string):
    count = 1
    prev = ''
    code = ''
    dimensions, serial = input_string.split('!')
    string = serial.replace('0', 'A').replace('1', 'B')

    for character in string:
        if character != prev:
            if prev != '':
                entry = prev + str(count)
                code += entry
            count = 1
            prev = character
        else:
            count += 1
    code += prev + str(count)

    return dimensions + '!' + code


def decode(code):
    dim, code = code.split('!')
    q = ""
    num = ''
    char = ''
    for character in code:
        if character.isalpha():
            if num != '':
                q += char * int(num)
                num = ''
            if character == 'A':
                char = '0'
            elif character == 'B':
                char = '1'

        elif character.isnumeric():
            num += character
    q += char * int(num)
    return dim + '!' + q


def deserialize(serial):
    size, code = serial.split('!')
    sw, sh = size.split(',')
    w, h = int(sw), int(sh)
    _surf = Surface((w, h))
    img = PixelArray(_surf)
    idx = -1
    for y in range(h):
        for x in range(w):
            idx += 1
            if serial[idx] == '1':
                img[x, y] = 255, 0, 255

            else:
                img[x, y] = 0, 0, 0

    return img.make_surface()


def comprimir(encoded):
    s = 'B'
    d, e = encoded.split('!')
    if s in e:
        while e.replace(s, 'J').count('JJ') == 0:
            if len(s) < len(e):
                s += e[e.find(s[-1], e.find(s)) + 1]
            else:
                return s

        if 'J' in e.replace(s, 'J'):
            comp = e.replace(s, 'J')
            Js = comp.count('J')
            split = comp.split('J' * Js)

            comp = ('J' + str(Js)).join(split) + ':' + s
        else:
            print('No se pudo comprmir')
            return e

    else:
        print('La compresión es innecesaria')
        return e
    return d + '!' + comp


def descomprimir(comp):
    dimensions, code = comp.split('!')
    key, val = code.split(':')
    n = int(key[key.find('J') + 1])
    missing = val * int(n)
    return dimensions + '!' + missing.join(key.split('J' + str(n)))


__all__ = ['serialize', 'encode', 'comprimir', 'descomprimir', 'decode', 'deserialize']

# if __name__ == '__main__':
#     import pygame, sys
#
#     pygame.init()
#
#     surf = Surface((53, 71))
#     surf.fill((255, 0, 255), (22, 61, 10, 16))
#
#     serial = serialize(surf)
#     encoded = encode(serial)
#     compressed = comprimir(encoded)
#     decompressed = descomprimir(compressed)
#     decoded = decode(decompressed)
#     image = deserialize(decoded)
#
#     fondo = pygame.display.set_mode((200, 200))
#     while True:
#         fondo.fill((255, 255, 255))
#
#         fondo.blit(image, (10, 10))
#         fondo.blit(surf, (90, 10))
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
