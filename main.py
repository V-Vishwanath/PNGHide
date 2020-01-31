import cv2
import numpy as np
import os


def binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])

    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, '08b') for i in data]

    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, '08b')

    return None


def encrypt(file, plain_text):
    img = cv2.imread(file)

    max_bytes = img.shape[0] * img.shape[1] * 3 // 8

    if len(plain_text) > max_bytes:
        print('Can\'t encode data! Insufficient bytes!')
        return None

    print('[*] Encoding data...', end='')

    plain_text += '!007!'
    data_index = 0

    plain_text = binary(plain_text)
    length = len(plain_text)

    for i in img:
        for pixel in i:
            r, g, b = binary(pixel)

            if data_index < length:
                pixel[0] = int(r[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index < length:
                pixel[1] = int(g[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index < length:
                pixel[2] = int(b[:-1] + plain_text[data_index], 2)
                data_index += 1

            if data_index >= length:
                break

    print(' Done!')
    cv2.imwrite('Encrypted.png', img)


def decrypt(file):
    print('[*] Decoding data...')

    img = cv2.imread(file)
    bin_str = ''

    for i in img:
        for pixel in i:
            r, g, b = binary(pixel)
            bin_str += r[-1] + g[-1] + b[-1]

    img_bytes = [bin_str[i: i + 8] for i in range(0, len(bin_str), 8)]

    plain_text = ''
    for b in img_bytes:
        plain_text += chr(int(b, 2))
        if plain_text[-5:] == '!007!':
            break

    return plain_text[:-5]

while True :
    choice = input('''\n\n
    Choose operation : 
    1) Encryption
    2) Decryption 
    3) Exit
    
    Your choice : ''')

    if choice == '1' :
        img = input('\n\nEnter image name with extension : ')
        img = os.path.join(os.getcwd(), img)
        msg = input('Enter message to encrypt : ')

        encrypt(img, msg)

    elif choice == '2' :
        img = input('\n\nEnter image name with extension : ')
        img = os.path.join(os.getcwd(), img)
        print(f'Message : {decrypt(img)}')

    else :
        break 

