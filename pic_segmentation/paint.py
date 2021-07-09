from PIL import Image, ImageDraw
import json
import os

json_path = 'sse_json/'
ori_pic_path = 'sse-images/'
out_path = 'out/'

with open('settings.json', 'r') as f:
    settings = json.load(f)
    dct = settings['sets-of-classes'][0]['objects']

for doc in os.listdir(json_path):
    fn = os.path.splitext(doc)[0]
    # with open(json_path + doc, 'r') as f:
    #     content = json.load(f)['objects']
    #     with Image.open(ori_pic_path + fn + '.jpg').convert('RGBA') as img:
    #         img2 = img.copy()
    #         draw = ImageDraw.Draw(img2)
    #         for i in content:
    #             polygon = [(j['x'], j['y']) for j in i['polygon']]
    #             color = dct[i['classIndex']]['color']
    #             draw.polygon(polygon, fill=color)
    #         img3 = Image.blend(img, img2, 0.5)
    #         img3.save(out_path + fn + '.png')

    # Another way
    with open(json_path + doc, 'r') as f:
        content = json.load(f)['objects']
        with Image.open(ori_pic_path + fn + '.jpg').convert('RGB') as img:
            poly = Image.new('RGBA', img.size)
            draw = ImageDraw.Draw(poly)
            for i in content:
                polygon = [(j['x'], j['y']) for j in i['polygon']]
                color = dct[i['classIndex']]['color']
                draw.polygon(polygon, fill=color + '7f')
            img.paste(poly, (0, 0), mask=poly)
            img.save(out_path + fn + '.png')
