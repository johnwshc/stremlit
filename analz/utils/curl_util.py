import pycurl
class CurlTest: 
    def __init__(self):
        self.url = 'http://localhost:5000/puttest/put'
        self.fn = 'E:/recorded_shows/wnl/shows/pbtest.mp3'

        self.c = pycurl.Curl()
        self.c.setopt(self.c.URL, self.url)

        self.c.setopt(self.c.UPLOAD, 1)
    def performput(self):
        f = open(self.fn, "wb")
        self.c.setopt(self.c.READDATA, f)
        self.c.perform()
        self.c.close()
        # File must be kept open while Curl object is using it
        f.close()