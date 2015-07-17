'''
Created on 21/03/2014

@author: Busquet
'''
from PIL import Image
import BaseHTTPServer
import dropbox
import cgi
import re
import platform
from lib.ImageOpener import smooth, median, sobel

APP_KEY = 'kd5x27tgtdjlyaq'
APP_SECRET = '8al6pwk1fkhe4al'
prog_folder = '/Public/'
access_token = 'zDDpST2IFvsAAAAAAAAAAT9prguCRs-48Oe3SMCsE2rwXG78jjIC0cd7SkGrh4-2'
uploader_file = open('../uploader.html').read()
success_file = open('../success.html').read()
error_file = open('../error.html').read()


def getDropboxClient():
    try:
        client = dropbox.client.DropboxClient(access_token)
        print 'linked account: ', client.account_info()
        return client
    except:
        return None


class GetHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    dbClient = getDropboxClient()

    def respond200(self, message):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

    def do_GET(self):
        self.respond200(uploader_file)
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'], })
        upfile = form['upfile']
        tipo = form['select'].value
        # extract basename of input filename, remove non-alphanumeric characters
        if '\\' in upfile.filename:
            filename = upfile.filename.split('\\')[-1]
        else:
            filename = upfile.filename.split('/')[-1]
        filename = re.sub('[ \t]', '-', filename)
        filename = re.sub('[^a-zA-Z0-9_.:-]', '', filename)
        if filename and ('.jpg' in filename or '.jpeg' in filename):
            fout = file(filename, 'wb')
            while 1:
                chunk = upfile.file.read(100000)
                print 'uploading'
                if not chunk:
                    break
                fout.write(chunk)
            fout.close()

            im = Image.open(filename)
            out = im.convert('L')
            if tipo == 'negativo':
                out = out.point(lambda i: 255 - i)
            elif tipo == 'smooth':
                out = smooth(out)
            elif tipo == 'median':
                out = median(out)
            elif tipo == 'sobel':
                out = sobel(out)
            out.save('modified-' + tipo + '-' + filename)
            bigFile = open(filename, 'rb')
            modified = open('modified-' + tipo + '-' + filename, 'rb')
            media = {'url': ''}
            if self.dbClient:
                print 'sending to dropbox'
                response = self.dbClient.put_file(prog_folder + filename, bigFile, True)
                response = self.dbClient.put_file(prog_folder + 'modified-' + filename, modified, True)
                print "uploaded:", response
                media = self.dbClient.media(prog_folder + 'modified-' + filename)
            self.respond200(success_file % media['url'])

        else:
            self.respond200(error_file)


def roll(image, delta):
    "Roll an image sideways"

    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0:
        return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize - delta, ysize))
    image.paste(part1, (xsize - delta, 0, xsize, ysize))

    return image


if __name__ == '__main__':
    try:
        port = 8080
        url = "http://%s:%d/" % (platform.node(), port)
        server = BaseHTTPServer.HTTPServer(('', port), GetHandler)
        print "Ask user to visit this URL:\n\t%s" % url
        server.serve_forever()
    except KeyboardInterrupt:
        pass
