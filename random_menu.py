import random

main_dishes = ['红烧肉', '番茄牛腩', '土豆牛腩', '白萝卜牛腩', '白萝卜棒骨', '红烧羊肉', '鸡翅', '红烧鸡块', '清蒸鲈鱼', '红烧排骨', '淮山排骨', '玉米排骨', '土豆排骨',
               '牛排', '黄鳝鱼', '鳝鱼', '白灼大虾', '煎鳕鱼', '煎带鱼']

vege_dishes = ['西芹百合', '蒸南瓜', '生菜', '空心菜', '油菜', '白菜', '蒿子杆', '红菜苔', '苋菜', '土豆丝']
mix_dishes = ['辣椒炒肉', '青椒肉丝', '番茄炒蛋', '香干炒芹菜', '平菇炒肉', '平菇炒鸡蛋', '黄瓜炒鸡蛋']

soup_dishes = ['西红柿蛋花汤', '平菇肉丝汤', '鲫鱼汤', '紫菜蛋花汤']
staple_foods = ['杂粮饭', '馒头', '手抓饼', '米粉', '面条']
staple_foods_weight = [5, 3, 1, 1, 1]

k = 12
main = random.sample(main_dishes, k=k)
vege = random.choices(vege_dishes, k=k)
mix = random.choices(mix_dishes, k=k)
soup = random.choices(soup_dishes, k=k)
staple_food = random.choices(staple_foods, weights=staple_foods_weight, k=k)
for i in zip(main, vege, mix, soup, staple_food):
    print(i)
