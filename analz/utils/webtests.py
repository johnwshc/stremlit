import requests
import cv2 as cv
from qreader import QReader
import segno

class WebTests:

    @staticmethod
    def wprest_test():
        url = "http://localhost:5000/manage/wprest"
        data = {'title': 'TestTitle', 'xpwd': 'vil3nin'}
        r = requests.get(url=url, params=data)
        print(r)
        return

class QRScanner:

    @staticmethod
    def Qr_Scanner(qr_img):
        scanner = QReader()
        img = cv.cvtColor(cv.imread(qr_img), cv.COLOR_BGR2RGB)
        data = scanner.detect_and_decode(image=img)
        print("Qr data: ", data)


    @staticmethod
    def make_qr(data: str='qr_hw.png'):

        qrcode = segno.make_qr("Hello, World")
        qrcode.save(
            data,
            scale=5,
            dark="darkblue",
            quiet_zone="maroon",
        )

class PBTests:

    text = "foo"

    @staticmethod
    def test_unicode():

        txt = """test"""

        txt2 = txt

        for c in txt2:
            if 0 <= ord(c) <= 127:
                # this is a ascii character.
                pass

            else:
                print(f'found bad char: {ord(c)}')
                txt = txt.translate({ord(c): None})
        # this is a non-ascii character. Do something.
        return txt








