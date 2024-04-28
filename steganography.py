import numpy
from PIL import Image


RGB = 'RGB'
RGBA = 'RGBA'


def Encode(src, msg, dest, lsb_tag='$t3g0', switch='08b'):
    raw = Image.open(src, 'r')
    h, w = raw.size
    arr = numpy.array(list(raw.getdata()))
    if raw.mode == RGB:
        n = 3
    elif raw.mode == RGBA:
        n = 4
    total_pixels = arr.size//n
    msg += lsb_tag
    b_msg = ''.join([format(ord(i), switch) for i in msg])
    req_pixels = len(b_msg)
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    arr[p][q] = int(bin(arr[p][q])[2:9] + b_msg[index], 2)
                    print(arr[p][q], "=>", bin(arr[p][q])[2:9] + b_msg[index], 2)
                    index += 1

    arr = arr.reshape(h, w, n)
    enc_img = Image.fromarray(arr.astype('uint8'), raw.mode)
    enc_img.save(dest)
    print("Image Encoded Successfully")


def Decode(src, lsb_tag="$t3g0"):
    img = Image.open(src, 'r')
    array = numpy.array(list(img.getdata()))
    if img.mode == RGB:
        n = 3
    elif img.mode == RGBA:
        n = 4
    total_pixels = array.size//n
    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    message = ""
    for i in range(len(hidden_bits)):
        if message[-len(lsb_tag):] == lsb_tag:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if lsb_tag in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


if __name__ == '__main__':
    Encode("./resources/base.png", "test", "./resources/dest/edited.png")
    Decode("./resources/dest/edited.png")
