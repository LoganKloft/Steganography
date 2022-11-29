from PIL import Image
import os
import numpy

class lsb:
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

    # img is the string location
    # msg is the string to encode
    def encode(self, img, msg):
        print("encoding", msg, "in", img)

        # load img
        cd = os.getcwd()
        im = Image.open(cd + img)

        # convert image to rows of pixels [Row1[P11, P12, ..., P1M], Row2[P21, P22, ..., P2M], ... RowN[PN1, PN2, ..., PNM]]
        a = numpy.array(im)

        # convert message to bit string
        b = ''.join(format(ord(i), '08b') for i in msg) # b is ALWAYS even in length

        b_iter = iter(b)

        for i, row in enumerate(a):
            for j, pixel in enumerate(row):
                R, G, B = pixel

                try:
                    # grab next bit from message
                    bit = next(b_iter)
                except StopIteration:
                    # end of message, set lsb of third byte to 1
                    a[i, j, 2] = self.set_lsb(B, "1")

                    # save the image and return
                    im = Image.fromarray(a)
                    im.save(cd + img)
                    print('saved', msg)
                    return

                # set lsb of first byte in pixel
                a[i, j, 0] = self.set_lsb(R, bit)

                # grab next bit from message
                bit = next(b_iter)

                # set lsb of second byte in pixel
                a[i, j, 1] = self.set_lsb(G, bit)

                # set lsb of third byte in pixel to 0
                a[i, j, 2] = self.set_lsb(B, "0")
    
    # given a number dec, return the lsb of dec as a string
    def get_lsb(self, dec):
        if (dec & 1) == 1: return "1"
        else:              return "0"

    # img is a string to the image location
    def decode(self, img):
        print("decoding", img)

        # load img
        cd = os.getcwd()
        im = Image.open(cd + img)

        # convert image to rows of pixels [Row1[P11, P12, ..., P1M], Row2[P21, P22, ..., P2M], ... RowN[PN1, PN2, ..., PNM]]
        a = numpy.array(im)

        # stores the encoded message
        result = ""

        # stores 8 bits at a time
        bitstring = ""

        for row in a:
            for pixel in row:
                # check if at end of message
                if self.get_lsb(pixel[2]) == "1":
                    print(result)
                    return result
                
                # not end of message - get the two lsbs in the pixel
                bitstring += self.get_lsb(pixel[0]) + self.get_lsb(pixel[1])

                # every 8 bits read = a new character to append to result
                if len(bitstring) == 8:
                    c = chr(int(bitstring, 2))
                    result += c
                    bitstring = ""