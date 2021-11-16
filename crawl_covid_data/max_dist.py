import os
# import time
import datetime
directory = 'dat/'
fmt = '%Y%m%d'
pair = None
last = datetime.datetime.strptime('20201230', fmt)
max_dist = datetime.timedelta(0)
for i in sorted(os.listdir(directory)):
    t = datetime.datetime.strptime(i.split('.')[0], fmt)
    if t - last > max_dist:
        pair = [t, last]
        max_dist = t - last
    last = t
print(max_dist)
print(pair)

