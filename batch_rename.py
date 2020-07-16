import os
import re

for folder in os.listdir("data"):
    for filename in os.listdir("data/" + folder):
        x = re.split('\.', filename)
        x[0] = folder
        x = '.'.join(x)
        os.rename("data/" + folder + '/' + filename, "data/" + folder + '/' + x)
