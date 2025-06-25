from ID3 import *
from Utilities.readFile import *
from Kmeans import *
import pickle

'''
data = read_procesed_covid("puebla.csv")

with open("anom2.pkl", "rb") as file:
    anom = pickle.load(file)
#kmeans grupos 5
print("Se termiinaron de leer los archivos")
grp  = Kmeans(data, anom, manhattan_distance, exclude=['id', 'class'], grp=5,  maxiter=100, cenfunc=0)
print("Kmeans termio de hacer los grupos")
trees = []
anom = []

sm = 0
for k in grp.keys():
   
    t, a = (generate_binary_decition_tree_C4(data, grp[k],exclude=['id', 'class']))
    trees.append(t)
    anom.append(a)
    print(f'tamaño de los que no pudieron ser clasificados {len(a)} tamaño del grupo {len(grp[k])}')s
print("EL TOTAL ES ", sm)
'''
#data = read_procesed_noID_Diabetes('E.csv')
data = read_procesed_covid('pueblaGob.csv')
print('El tamaño de la bese es: ', len(data['id']))
t, a = generate_binary_decition_tree_C4(data, data['id'], exclude=['id', 'class'])

t.visualize()
print(f'La cantidad no clasificada con 1 solo arbol:  {len(a)}')

grp  = Kmeans(data, data['id'], manhattan_distance, exclude=['id', 'class'], grp=5,  maxiter=100, cenfunc=0)
trees = []
anom = []

sm = 0
for k in grp.keys():
    
    tK, aK = (generate_binary_decition_tree(data, grp[k],exclude=['id', 'class']))
    trees.append(tK)
    anom.append(aK)
    print(f'tamaño de los que no pudieron ser clasificados {len(aK)} tamaño del grupo {len(grp[k])}')
    sm += len(aK)

print("La cantidad no clasificada con 5 arboles: ", sm)