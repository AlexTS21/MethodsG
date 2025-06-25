from .binaryTree import BinaryTree
from .node import Node
from .entropy import  *
from .entropyC4 import *

def generate_binary_decition_tree(data, index, exclude=['id', 'class']):
    tree = BinaryTree()
    anomaly = []
    node = Node(0, [index, exclude])
    tree.keys.append(0)
    tree.root = node
    decition_tree(tree, 0, data, index, exclude, anomaly)
    return tree, anomaly

def generate_binary_decition_tree_C4(data, index, exclude=['id', 'class']):
    tree = BinaryTree()
    anomaly = []
    node = Node(0, [index, exclude])
    tree.keys.append(0)
    tree.root = node
    decision_tree_C4(tree, 0, data, index, exclude, anomaly)
    return tree, anomaly

#Se agrega a l1
def insert_list(l1, l2):
  for l in l2:
    if l not in l1:
      l1.append(l)
  return l1

def generate_key(tree):
  key = tree.keys[-1] + 1
  tree.keys.append(key)
  return key

#Try to add the vairbale with less entrophy in data position 2
def decition_tree(tree, key, data, index, exclude, anomaly):

    variable, value = obtener_entropia_minima(data, index, exclude)
    node = tree.search(key)
    node.data.append(variable)
    node.data.append(value)
    #print(f'nodo{key}, {value}, {variable}')
    if(value != 0 and iterable_data(data, index, exclude) and value!=1):
        #print("HOLAAAAAAAAAAAAA")
        dataL, dataR =obtener_indices(data, index, variable)
        excvariableL = exclude.copy()
        excvariableL.append(variable)
        excvariableR = excvariableL.copy()
        keyL = generate_key(tree)

        keyR = generate_key(tree)


        tree.insert_left(key, keyL, [dataL, excvariableL])
        tree.insert_right(key, keyR, [dataR, excvariableR])
        decition_tree(tree, keyL,data, dataL, excvariableL, anomaly)

        decition_tree(tree, keyR,data, dataR, excvariableR, anomaly)
    elif(not iterable_data(data, index, exclude) or value==1):
        #print("HEREEEEEEEEE")
        insert_list(anomaly, node.data[0])
        node.key = node.key*(-1)
    else:
        return

def decision_tree_C4(tree, key, data, index, exclude, anomaly, umbral=0.01, min_samples=2):
    from collections import Counter

    clases = [data['class'][i] for i in index]

    # Criterio 1: todas las instancias tienen la misma clase
    if len(set(clases)) == 1:
        node = tree.search(key)
        node.data.append(clases[0])
        return

    # Criterio 2: no hay más atributos disponibles
    if set(data.keys()) - set(exclude) - {'class'} == set():
        node = tree.search(key)
        node.key = -key
        node.data.append('Hoja')
        mayoritaria = Counter(clases).most_common(1)[0][0]
        node.data.append(mayoritaria)
        insert_list(anomaly, index)  # Agregar los índices actuales
        return

    # Obtener mejor división
    variable, gain, gain_ratio = mejor_variable_por_gain_ratio(data, index, exclude)

    node = tree.search(key)
    node.data.append(variable)
    node.data.append(gain_ratio)

    # Criterios 3 y 4: ganancia baja o pocos datos
    if gain_ratio < umbral or len(index) < min_samples:
        node.key = -key
        mayoritaria = Counter(clases).most_common(1)[0][0]
        node.data.append(mayoritaria)
        insert_list(anomaly, index)  # Agregar los índices actuales
        return

    # División válida: generar hijos
    dataL, dataR = obtener_indices(data, index, variable)
    excL = exclude + [variable]
    excR = exclude + [variable]
    keyL = generate_key(tree)
    keyR = generate_key(tree)

    tree.insert_left(key, keyL, [dataL, excL])
    tree.insert_right(key, keyR, [dataR, excR])

    decision_tree_C4(tree, keyL, data, dataL, excL, anomaly, umbral, min_samples)
    decision_tree_C4(tree, keyR, data, dataR, excR, anomaly, umbral, min_samples)