'''
Created on 19/03/2014

@author: Busquet
'''
from PIL import Image
from multiprocessing import Pool
import datetime


def smooth(img):
    copy_img = img.copy()
    pix_load = img.load()
    result = copy_img.load()
    w, h = img.size
    pix = []
    start = datetime.datetime.now()
    print 'starting'
    for x in range(1, h - 1):
        for y in range(1, w - 1):
            pix = []
            for xx in [x - 1, x, x + 1]:
                for yy in [y - 1, y, y + 1]:
                    pix.append(pix_load[xx, yy])
            mean = sum(pix) / 9
            result[x, y] = mean
    end = (datetime.datetime.now() - start).total_seconds()
    print 'finished in %s s' % end
    return copy_img


def median(img):
    copy_img = img.copy()
    pix_load = img.load()
    result = copy_img.load()
    w, h = img.size
    start = datetime.datetime.now()
    print 'starting'
    for x in xrange(2, w - 2):
        for y in xrange(2, h - 2):
            pix = []
            for xx in xrange(x - 2, x + 3):
                for yy in xrange(y - 2, y + 3):
                    pix.append(pix_load[xx, yy])
            result[x, y] = sorted(pix)[len(pix) / 2 + 1]
    end = (datetime.datetime.now() - start).total_seconds()
    print 'finished in %s s' % end
    return copy_img


def sobel(img):
    matrix_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    matrix_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    copy_img = img.copy()
    pix_load = img.load()
    result = copy_img.load()
    w, h = img.size
    start = datetime.datetime.now()
    print 'starting'
    for x in xrange(1, w - 1):
        for y in xrange(1, h - 1):
            pix = [pix_load[x - 1, y - 1], pix_load[x - 1, y], pix_load[x - 1, y + 1],
                   pix_load[x, y - 1], pix_load[x, y], pix_load[x, y + 1],
                   pix_load[x + 1, y - 1], pix_load[x + 1, y], pix_load[x + 1, y + 1]]
            t = (sum([a * b for a, b in zip(matrix_x, pix)]) ** 2 + \
                            sum([a * b for a, b in zip(matrix_y, pix)]) ** 2) ** 0.5
            # print t
            result[x, y] = t
    end = (datetime.datetime.now() - start).total_seconds()
    print 'finished in %s s' % end
    return copy_img


gauss = [0.053991, 0.241971, 0.398942, 0.241971, 0.053991]


def gaussian(img):
    copy_img = img.copy()
    pix_load = img.load()
    result = copy_img.load()
    w, h = img.size
    start = datetime.datetime.now()
    print 'starting'
    for y in xrange(h):
        for x in xrange(2, w - 2):
            matrix_x = [pix_load[x - 2, y], pix_load[x - 1, y], pix_load[x, y], pix_load[x + 1, y], pix_load[x + 2, y]]
            t = sum([a * b for a, b in zip(matrix_x, gauss)])
            # print t, matrix_x
            result[x, y] = t
    cpcp = copy_img.copy().load()
    for x in xrange(w):
        for y in xrange(2, h - 2):
            matrix_y = [cpcp[x, y - 2], cpcp[x, y - 1], cpcp[x, y], cpcp[x, y + 1], cpcp[x, y + 2]]
            t = sum([a * b for a, b in zip(matrix_y, gauss)])
            result[x, y] = t
    end = (datetime.datetime.now() - start).total_seconds()
    print 'finished in %s s' % end
    return copy_img
