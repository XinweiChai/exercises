import re

# seg = ['which', 'where', 'who', 'why', 'how', 'because', 'what', 'that', ',']
text = 'Mr. Bruno said that The American economic system is, organized around a basically private-enterprise, market-oriented economy in which consumers largely determine what shall be produced by spending their money in the marketplace for those goods and services that they want most. Wow.'
sentences = re.sub('(Mr|Mrs|Ms|etc|e\.g|i\.e)\.', '\g<0>\r', text)
sentences = re.sub('\.([^\r])', '\g<0>\n', sentences)
sentences = re.split(' *\n', sentences)
sentences = [i.replace('\r', '') for i in sentences]
after = []
for i in sentences:
    temp = i
    temp = re.sub('((in|on|at|from|by|with|about|of) )?(which|where|who|why|how|because|what|that)', '\n\g<0>', temp)
    temp = re.sub('[,;:]\s*', '\g<0>\n', temp)
    temp = re.split('\n', temp)
    after.append(temp)

for i in after:
    count = 0
    for j in i:
        print(' ' * count + j)
        count += 2
