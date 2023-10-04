from build_scrapper import get_one_champ_data
import urllib.request
from PIL import Image
import os


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def get_build_image(data):

    imgs = [] 
    for i, item in enumerate(data['build']):
        #print(item['image'])
        image_name = f"image{i+1}.png"
        urllib.request.urlretrieve(item['image'],image_name)
        img = Image.open(image_name)
        imgs.append(img)

    get_concat_h(imgs[0], imgs[1]).save('final1.jpg')
    temp = Image.open('final1.jpg')
    get_concat_h(temp, imgs[2]).save('final1.jpg')

    get_concat_h(imgs[3], imgs[4]).save('final2.jpg')
    temp = Image.open('final2.jpg')
    get_concat_h(temp, imgs[5]).save('final2.jpg')

    final1 = Image.open('final1.jpg')
    final2 = Image.open('final2.jpg')

    get_concat_v(final1, final2).save('result.jpg')
    
    res = Image.open('result.jpg')
    #res.show()
    #return res

    # clean up used files 
    for file in os.listdir(os.getcwd()):
        if (file.startswith('image') and file.endswith('.png')) or (file.startswith('final') and file.endswith('.jpg')):
            os.remove(file) 

def delete_image(img_name):
    for file in os.listdir(os.getcwd()):
        if (file.startswith(img_name)):
            os.remove(file) 
