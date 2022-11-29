from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import Base
from PIL.PngImagePlugin import PngInfo
import os
import piexif

class exf:
    def __init__(self, image):
        # self.img = Image(image)
        cd = os.getcwd()
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
            if d is not None:
                for k, v in d.items():
                    result[k] = v
            return result

        # for jpg
        tags = self.img._getexif()
        # tags = self.img['Exif']
        for k, v in tags.items():
            if isinstance(v, str):
                result[TAGS[k]] = v
        return result
    
    # type = false means jpg
    # type = true means png
    def set_exif(self, dict):
        for k, v in dict.items():
            print(k)


    # def get_all_exif(self):
    #     return self.img.get_all()

    # def get_exif(self, attribute):
    #     return self.img.get(attribute)

    # def set_exif(self, attribute, value):
    #     self.img.set(attribute, value)

    # def del_exif(self, attribute):
    #     self.img.delete(attribute)
