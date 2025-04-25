from .binaryTree import BinaryTree
from .node import Node
from .entropy import  *

def generate_binary_decition_tree(data, index, exclude=['id', 'class']):
    tree = BinaryTree()
    anomaly = []
    node = Node(0, [index, exclude])
    tree.keys.append(0)
    tree.root = node
    decition_tree(tree, 0, data, index, exclude, anomaly)
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