"""
Code extracted from Wake Up! to manage pixels manipulation from python
"""


def get_mode0_pixel0_byte_encoded(pen):
    """Return byte value of left pixel"""
    pen = int(pen)
    assert pen < 16

    byte = 0

    if pen & 1:
        byte = byte + (2**7)
    if pen & 2:
        byte = byte + (2**3)
    if pen & 4:
        byte = byte + (2**5)
    if pen & 8:
        byte = byte + (2**1)

    return byte

def get_mode0_pixel1_byte_encoded(pen):
    """Return byte value of right pixel"""
    pen = int(pen)
    assert pen < 16

    byte = 0

    if pen & 1: 
        byte = byte + (2**6)
    if pen & 2: 
        byte = byte + (2**2)
    if pen & 4:
        byte = byte + (2**4)
    if pen & 8: 
        byte = byte + (2**0)

    return byte



def get_mode1_pixel0_byte_encoded(pen):
    """Compute the byte fraction for the required pixel.
    Order of pixels : 0 1 2 3
    """
    pen = int(pen)
    assert pen < 4

    byte = 0

    if pen & 1:
        byte = byte + (2**7)
    if pen & 2:
        byte = byte + (2**3)

    return byte

def get_mode1_pixel1_byte_encoded(pen):
    """Compute the byte fraction for the required pixel.
    Order of pixels : 0 1 2 3
    """
    pen = int(pen)
    assert pen < 4

    byte = 0

    if pen & 1:
        byte = byte + (2**6)
    if pen & 2:
        byte = byte + (2**2)

    return byte

def get_mode1_pixel2_byte_encoded(pen):
    """Compute the byte fraction for the required pixel.
    Order of pixels : 0 1 2 3
    """
    pen = int(pen)
    assert pen < 4

    byte = 0

    if pen & 1:
        byte = byte + (2**5)
    if pen & 2:
        byte = byte + (2**1)

    return byte

def get_mode1_pixel3_byte_encoded(pen):
    """Compute the byte fraction for the required pixel.
    Order of pixels : 0 1 2 3
    """
    pen = int(pen)
    assert pen < 4

    byte = 0

    if pen & 1:
        byte = byte + (2**4)
    if pen & 2:
        byte = byte + (2**0)

    return byte



def get_mode2_pixel_postion(pos, pen):
    pen = int(pen)
    assert pos < 8
    assert pen <2
    return 2**(7-pos)*pen


def get_mode2_pixel0_byte_encoded(pen):
    return get_mode2_pixel_postion(0, pen)

def get_mode2_pixel1_byte_encoded(pen):
    return get_mode2_pixel_postion(1, pen)

def get_mode2_pixel2_byte_encoded(pen):
    return get_mode2_pixel_postion(2, pen)

def get_mode2_pixel3_byte_encoded(pen):
    return get_mode2_pixel_postion(3, pen)

def get_mode2_pixel4_byte_encoded(pen):
    return get_mode2_pixel_postion(4, pen)

def get_mode2_pixel5_byte_encoded(pen):
    return get_mode2_pixel_postion(5, pen)

def get_mode2_pixel6_byte_encoded(pen):
    return get_mode2_pixel_postion(6, pen)

def get_mode2_pixel7_byte_encoded(pen):
    return get_mode2_pixel_postion(7, pen)




def get_mode0_byte(pen0, pen1):
    """untested"""
    return get_mode0_pixel0_byte_encoded(pen0) |  get_mode0_pixel1_byte_encoded(pen1) 



def get_mode1_byte(pen0, pen1, pen2, pen3):
    return get_mode1_pixel0_byte_encoded(pen0) |  \
            get_mode1_pixel1_byte_encoded(pen1) | \
            get_mode1_pixel2_byte_encoded(pen2) | \
            get_mode1_pixel3_byte_encoded(pen3)


def get_mode2_byte(pen0, pen1, pen2, pen3, pen4, pen5, pen6, pen7):
    return get_mode2_pixel0_byte_encoded(pen0) |  \
            get_mode2_pixel1_byte_encoded(pen1) | \
            get_mode2_pixel2_byte_encoded(pen2) | \
            get_mode2_pixel3_byte_encoded(pen3) | \
            get_mode2_pixel4_byte_encoded(pen4) | \
            get_mode2_pixel5_byte_encoded(pen5) | \
            get_mode2_pixel6_byte_encoded(pen6) | \
            get_mode2_pixel7_byte_encoded(pen7)









