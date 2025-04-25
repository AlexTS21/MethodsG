from ID3 import *
from Utilities.readFile import *
from Kmeans import *


data = read_procesed_noID_Diabetes("E.csv")

#kmeans grupos 5

grp  = Kmeans(data,  data['id'], manhattan_distance, exclude=['id', 'class'], grp=5,  maxiter=100, cenfunc=0)

trees = []
anom = []

for k in grp.keys():
    t, a = (generate_binary_decition_tree(data, grp[k]))
    trees.append(t)
    anom.append(a)
    print(f'tamaño de los que no pudieron ser clasificados {len(a)} tamaño del grupo {len(grp[k])}')

t, a = generate_binary_decition_tree(data, data['id'])
print(len(a))