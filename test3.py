from ID3 import *
from Utilities.readFile import *
from Kmeans import *
import pickle

data = read_procesed_covid("pueblaGob.csv")

vars = [
'INTUBADO',
'NEUMONIA',
'EDAD',
'EMBARAZO',
'INDIGENA',
'DIABETES',
'EPOC',
'ASMA',
'INMUSUPR',
'HIPERTENSION',
'CARDIOVASCUL',
'OBESIDAD',
'RENAL_CRONIC',
'TABAQUISMO',
'TOMA_MUESTRA',
]
t, a = (generate_binary_decition_tree(data, data['id'],exclude=['id', 'class']))
print(len(a))
'''
anoms = []
for v in vars:
    t, a = (generate_binary_decition_tree(data, data['id'],exclude=['id', 'class', v]))
    anoms.append([v,a])
    print(f'var: {v}, notc: {len(a)}')

'''



