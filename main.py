# -*- coding: utf-8 -*-
'''
Created on 21/03/2014

@author: Busquet
'''
from PIL import Image
import dropbox
from image.ImageOpener import smooth, median, sobel, gaussian
import sys
import os

APP_KEY = or.environ.get('APP_KEY')
APP_SECRET = or.environ.get('APP_SECRET')
prog_folder = '/Public/'
ACCESS_TOKEN = or.environ.get('ACCESS_TOKEN')
uploader_file = open('uploader.html').read()
success_file = open('success.html').read()
error_file = open('error.html').read()


def getDropboxClient():
    try:
        client = dropbox.client.DropboxClient(ACCESS_TOKEN)
        print 'linked account: ', client.account_info()
        return client
    except:
        return None


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


def main():
    if len(sys.argv) < 2:
        print "usage: main.py arquivo efeito"
        print "efeitos: negativo, smooth, median, sobel"
        return
    filename = sys.argv[1]
    tipo = sys.argv[2] if len(sys.argv) == 3 else ''
    print filename, tipo
    if "\\" in filename:
        filedir = ('\\'.join(filename.split('\\')[:-1])or '.') + '\\'
        filename = filename.split('\\')[-1] or '\.\\'
    else:
        filedir = ('/'.join(filename.split('/')[:-1]) or '.') + '/'
        filename = filename.split('/')[-1]
    im = Image.open(filedir + filename)
    out = im.convert('L')
    if tipo == 'negativo':
        out = out.point(lambda i: 255 - i)
    elif tipo == 'smooth':
        out = smooth(out)
    elif tipo == 'median':
        out = median(out)
    elif tipo == 'sobel':
        out = sobel(out)
    elif tipo == 'gaussian':
        out = gaussian(out)
    print 'saving to ./' + 'modified_' + tipo + '_' + filename
    out.save('./' + 'modified_' + tipo + '_' + filename)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
