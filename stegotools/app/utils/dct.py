from PIL import Image
import numpy
import math
import scipy

class dct:
    def __init__(self, delimiter = "..."):
        self.delimiter = delimiter
        self.quant = numpy.array([[16,11,10,16,24,40,51,61],
                               [12,12,14,19,26,58,60,55],
                               [14,13,16,24,40,57,69,56],
                               [14,17,22,29,51,87,80,62],
                               [18,22,37,56,68,109,103,77],
                               [24,35,55,64,81,104,113,92],
                               [49,64,78,87,103,121,120,101],
                               [72,92,95,98,112,100,103,99]])
        self.m = 8
        self.n = 8
    
    # dec is a number
    # bit is the position of the bit from right to left to set in dec
    def set_bit(self, dec, bit):
        return dec | (1 << bit)

    # dec is a number
    # bit is the position of the bit from right to left to clear in dec
    def clear_bit(self, dec, bit):
        return dec & ~(1 << bit)

    # dec is a number
    # bit is a string "0" or "1"
    def set_lsb(self, dec, bit):
        if bit == "0":
            # clear bit
            return self.clear_bit(dec, 0)
        else:
            # set bit
            return self.set_bit(dec, 0)

    def dct2(self, a):
        return scipy.fftpack.dct( scipy.fftpack.dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )
    
    def dctn(self, a):
        return numpy.array(scipy.fft.dctn(a, norm="ortho"))

    def idctn(self, a):
        return numpy.array(scipy.fft.idctn(a, norm="ortho"))

    def idct2(self, a):
        return scipy.fftpack.idct( scipy.fftpack.idct( a, axis=0 , norm='ortho'), axis=1 , norm='ortho')

    # algorithm implementation by: phasing17 https://www.geeksforgeeks.org/discrete-cosine-transform-algorithm-program
    # a is an 8x8 matrix
    def apply_dct(self, a):
        m = 8
        n = 8
        pi = 3.1415926535897931

        dct = numpy.zeros((m, n))
    
        for i in range(m):
            for j in range(n):
    
                # ci and cj depends on frequency as well as
                # number of row and columns of specified matrix
                if (i == 0):
                    ci = 1 / (m ** 0.5)
                else:
                    ci = (2 / m) ** 0.5
                if (j == 0):
                    cj = 1 / (n ** 0.5)
                else:
                    cj = (2 / n) ** 0.5
    
                # sum will temporarily store the sum of
                # cosine signals
                sum = 0
                for k in range(m):
                    for l in range(n):
    
                        dct1 = a[k, l] * math.cos((2 * k + 1) * i * pi / (
                            2 * m)) * math.cos((2 * l + 1) * j * pi / (2 * n))
                        sum = sum + dct1
    
                dct[i, j] = ci * cj * sum
        return dct

    def apply_quantization(self, a):
        quantized = numpy.zeros((self.m, self.n))

        for i in range(0, self.m):
            for j in range(0, self.n):
                quantized[i, j] = a[i, j] / self.quant[i, j]

        return numpy.rint(quantized)

    def apply_iquantization(self, a):
        iquantized = numpy.zeros((self.m, self.n))

        for i in range(0, self.m):
            for j in range(0, self.n):
                iquantized[i, j] = a[i, j] * self.quant[i, j]
        
        return iquantized

    def check_equal(self, a, b):
        for i in range(self.m):
            for j in range(self.n):
                if a[i, j] != b[i, j]: print(a[i, j], b[i, j], end='\n')
        return True

    # https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html
    def encode(self, img, msg):
        # add delimiter to msg
        msg = msg + self.delimiter

        # convert msg to bit string
        b = ''.join(format(ord(i), '08b') for i in msg) # b is ALWAYS even in length
        b_iter = iter(b)

        # convert img from RGB to YCbCr
        im = Image.open(img)
        im = im.convert("YCbCr")

        # work on Cb channel
        cb_channel = im.getchannel("Cb")

        # downsample chrominance components (Cb, Cr) by a factor of 4

        a = numpy.array(cb_channel)
        width, height = a.shape
        try:
            for i in range(8, height, 8):
                for j in range(8, width, 8):
                    # get 8x8 square
                    sliced = numpy.copy(a[i - 8: i, j - 8: j])

                    # # apply DCT to square
                    # dcted = self.dctn(sliced)

                    # # apply quantization to square
                    # quantized = self.apply_quantization(dcted)

                    # # insert message bit into DC (discrete cosine transform coefficient)
                    # bit = next(b_iter)
                    # DC = int(quantized[0 , 0])
                    # DC_prime = self.set_lsb(DC, bit)
                    # quantized[0, 0] = DC_prime

                    # # apply inverse quantization to square
                    # iquantized = self.apply_iquantization(quantized)

                    # # apply inverse DCT to square
                    # idcted = self.idctn(iquantized)

                    # apply DCT to square
                    dcted = self.dctn(sliced)

                    # insert message bit into DC (discrete cosine transform coefficient)
                    bit = next(b_iter)
                    DC = int(dcted[0 , 0])
                    DC_prime = self.set_lsb(DC, bit)
                    dcted[0, 0] = DC_prime

                    # apply inverse DCT to square
                    idcted = numpy.rint(self.idctn(dcted))

                    # insert slice back into a
                    # a[i - 8: i, j - 8: j] = dcted
                    print(a[0, 0], sliced[0, 0], dcted[0, 0], idcted[0, 0])


        except StopIteration: pass

        # update im's Cb channel with the new cb_channel
        original = numpy.array(im)
        original[...,1] = a
        im = Image.fromarray(original, mode="YCbCr")
        im = im.transpose(Image.Transpose.ROTATE_270)

        # save new image
        im.save("steg/test1.JPG")

    # given a number dec, return the lsb of dec as a string
    def get_lsb(self, dec):
        if (dec & 1) == 1: return "1"
        else:              return "0"

    def decode(self, img):
        # open jpg
        im = Image.open(img)

        # convert to YCbCr mode
        im = im.convert("YCbCr")

        # get Ch channel since that's where message is stored
        cb_channel = im.getchannel("Cb")

        # convert cb_channel to array
        a = numpy.array(cb_channel)
        print(a)

        width, height = a.shape
        result = ""
        bitstring = ""
        for i in range(8, height, 8):
            for j in range(8, width, 8):
                # get 8x8 square
                sliced = a[i - 8: i, j - 8: j]
                if sliced.size == 0: continue

                # apply DCT to square
                dcted = self.dctn(sliced)

                # # apply quantization to square
                # quantized = self.apply_quantization(dcted)

                # # retrieve message bit from DC (discrete cosine transform coefficient)
                # DC = int(quantized[0, 0])
                # print(DC)
                # bitstring += self.get_lsb(DC)

                # retrieve message bit from DC (discrete cosine transform coefficient)
                DC = int(dcted[0, 0])
                print(DC)
                bitstring += self.get_lsb(DC)

                if len(bitstring) == 8:
                    c = chr(int(bitstring, 2))
                    print(c)
                    result += c
                    bitstring = ""
                    return

                    if result.endswith(self.delimiter):
                        print(result)
                        return result