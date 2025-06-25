from ID3 import *
from Utilities.readFile import *
from NNetwork import nn

nn = nn([1,2], ['identidad'])

data = read_procesed_noID_Diabetes('E.csv')

t, a = generate_binary_decition_tree(data, data['id'], exclude=['id', 'class'])
#print(len(t.root.data))
#print(len(t.root.left.data))

pb = {'Polyuria': [1,1,1],
      'Polydipsia': [1,0,0],
      'Itching':[1,1,1],
      'Genital thrush':[1,1,0],
      'visual blurring':[1,1,0],
      'Obesity':[1,1],
      'muscle stiffness':[1,0],
      'Gender': [1,1]}

t.printTree(data)
print(t.test_path(data, pb, 2))


#Tenemos que hacer funcion para pasar un dicionario con los valores
#la data funciona de la siguiente manera, indices, variables excluidas, variable, entropia

