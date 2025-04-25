from ID3 import *
from Utilities.readFile import *



data = read_procesed_noID_Diabetes("E.csv")

tree, anom = generate_binary_decition_tree(data, data['id'])

tree.printTree(data)
tree.visualize()
