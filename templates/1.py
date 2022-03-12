# Import QRCode from pyqrcode
import pyqrcode

s = "www.geeksforgeeks.org"
url = pyqrcode.create(s)
url.png('myqr.jpg', scale = 6)

