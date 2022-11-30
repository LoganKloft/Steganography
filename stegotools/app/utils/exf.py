from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import Base
from PIL.PngImagePlugin import PngInfo
import os
import piexif
import random
import time

TAGS_R = { v:k for k, v in TAGS.items() }

class exf:
    def __init__(self, image):
        # self.img = Image(image)
        self.url = image
        cd = os.getcwd()
        try:
            self.img = Image.open(cd + image)
        except:
            time.sleep(.5)
            self.img = Image.open(cd + image)
    
    # type = false means jpg
    # type = true means png
    def get(self, png):
        result = {}

        # by default allow user to have message1 and message2
        if png is True:
            result['message1'] = 'Blank'
            result['message2'] = 'Blank'
            d = self.img.text
            print(d)
            if d is not None:
                for k, v in d.items():
                    result[k] = v
            print('result', result)
            return result

        # for jpg
        tags = self.img._getexif()
        for k, v in tags.items():
            if isinstance(v, str):
                result[TAGS[k]] = v
        return result
    
    # type = false means jpg
    # type = true means png
    # return the url
    def set_exif(self, d, png):
        if png is True:
            metadata = PngInfo()
            for k, v in d.items():
                metadata.add_text(k, v)
            
            # save is not overriding the original location
            # solution: generate random name for image and return to frontend for download
            new_url = '/media/' + str(random.randint(0, 100000)) + '.PNG'
            print('saving at:', os.getcwd() + new_url)
            self.img.save(os.getcwd() + new_url, pnginfo=metadata)
            return new_url
            
        # jpg
        exif_dict = piexif.load(os.getcwd() + self.url)
        zero_th = exif_dict['0th']
        exif = exif_dict['Exif']

        for k, v in d.items():
            converted_key = TAGS_R[k]
            if converted_key in zero_th:
                zero_th[converted_key] = v
            elif converted_key in exif:
                exif[converted_key] = v

        
        exif_dict['0th'] = zero_th
        exif_dict['Exif'] = exif
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, os.getcwd() + self.url)
        return self.url


    # def get_all_exif(self):
    #     return self.img.get_all()

    # def get_exif(self, attribute):
    #     return self.img.get(attribute)

    # def set_exif(self, attribute, value):
    #     self.img.set(attribute, value)

    # def del_exif(self, attribute):
    #     self.img.delete(attribute)
