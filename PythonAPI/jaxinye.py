from PIL import Image
import os
import glob
import math
from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
import numpy as np


def crop(path, input, height, width, k, page, area=(0,0,255,255)):
    '''
    Crop input image into pieces of size specified as height X witdth
    '''
    im = Image.open(input)
    imgwidth, imgheight = im.size
    print(im.size)
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            a.save(os.path.join(path,"IMG-%s.png" % str(k).zfill(2)))
            try:
                o = a.crop(area)
                o.save(os.path.join(path,"PNG","%s" % page,"IMG-%s.png" % k))
            except:
                pass
            k +=1

def stitch(path, origin, height, width):
    '''
    Stitch pieces of image of size specified as height X width into the size of origin
    '''
    image_list = glob.glob(path)
    print(sorted(image_list))
    images = map(Image.open, image_list)
    ori = Image.open(origin)
    imgwidth, imgheight = ori.size
    horizontalNum = math.ceil(imgwidth/width)
    verticalNum = math.ceil(imgheight/height)
    new_im= Image.new('RGB', (imgwidth, imgheight))
    #TODO

def data_loader_coco(category_list=['traffic light','car']):
    # display COCO categories
    dataDir='.'
    dataType='val2017'
    annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
    coco = COCO(annFile)
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats]
    print('COCO categories: \n{}\n'.format(' '.join(nms)))

    # get all images containing given categories (I'm selecting the "bird")
    catIds = coco.getCatIds(catNms=category_list)
    imgIds = coco.getImgIds(catIds=catIds)

    for k in range(0, len(imgIds)):
        img = coco.loadImgs(imgIds[k])[0]
        I = io.imread(img['coco_url'])
        im = Image.fromarray(I)
        im.save("./savedImage/{}.png".format(k))
    print(len(imgIds), "images saved")

if __name__ == "__main__":
    data_loader_coco(category_list=['traffic light','car'])