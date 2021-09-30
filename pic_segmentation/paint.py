from PIL import Image, ImageDraw
import json
import os

pwd = "/home/chai/Desktop/semantic-segmentation-editor-1.6.0/"
json_path = pwd + 'sse_json/'
ori_pic_path = '/home/chai/sse-images_all/'
out_path = pwd + 'out/'
class_name = 'Lab430-街景'

with open(pwd + 'settings.json', 'r') as f:
    settings = json.load(f)
    dct = [i for i in settings['sets-of-classes'] if i['name'] == class_name][0]['objects']

for doc in os.listdir(json_path):
    fn = os.path.splitext(doc)[0]
    with open(json_path + doc, 'r') as f:
        content = json.load(f)
        # More robust
        # class_name = content['socName']
        # with open('settings.json', 'r') as f2:
        #     settings = json.load(f2)
        #     dct = [i for i in settings['sets-of-classes'] if i['name'] == class_name][0]['objects']
        with Image.open(ori_pic_path + fn + '.jpg').convert('RGBA') as img:
            img2 = img.copy()
            draw = ImageDraw.Draw(img2)
            for i in content['objects']:
                polygon = [(j['x'], j['y']) for j in i['polygon']]
                color = dct[i['classIndex']]['color']
                draw.polygon(polygon, fill=color)
            img3 = Image.blend(img, img2, 0.5)
            img3.save(out_path + fn + '.png')

    # Another way, if we need to keep the transparency, we can paint directly on img instead of paste
    # with open(json_path + doc, 'r') as f:
    #     content = json.load(f)
    #     with Image.open(ori_pic_path + fn + '.jpg').convert('RGB') as img:
    #         poly = Image.new('RGBA', img.size)
    #         draw = ImageDraw.Draw(poly)
    #         for i in content['objects']:
    #             polygon = [(j['x'], j['y']) for j in i['polygon']]
    #             color = dct[i['classIndex']]['color']
    #             draw.polygon(polygon, fill=color + '7f')
    #         img.paste(poly, (0, 0), mask=poly)
    #         img.save(out_path + fn + '.png')
