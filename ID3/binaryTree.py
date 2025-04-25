from .node import Node
from .entropy import get_num_clase
import networkx as nx
import matplotlib.pyplot as plt

class BinaryTree:

    def __init__(self):
        self.root:Node = None
        self.keys = []

    def insert_right(self, clave, key, data):
        node = Node(key, data)
        if(self.root.right == None or clave == None):
            self.root.right = node
        else:
            insert = self.search(clave)
            if(insert != None):
                insert.right = node
            else:
                return False

    def insert_left(self, clave, key, data):
        node = Node(key, data)
        if(self.root.left == None or clave == None):
            self.root.left = node
        else:
            insert = self.search(clave)
            if(insert != None):
                insert.left = node
            else:
                return False


    def find_parent(self, node, key, parent=None):
      """
      Encuentra el nodo padre de un nodo con una clave específica.

      :param node: El nodo actual (inicio con self.root).
      :param key: La clave del nodo cuyo padre se desea encontrar.
      :param parent: El nodo padre actual (None para la raíz).
      :return: El nodo padre si se encuentra, o None si no existe.
      """
      if node is None:
          return None
      if node.key == key:
          return parent  # Se encontró el nodo, devolvemos el padre
      # Buscar recursivamente en los hijos izquierdo y derecho
      left_result = self.find_parent(node.left, key, node)
      if left_result:
          return left_result
      return self.find_parent(node.right, key, node)


    def search(self, key):
        nodo = Node.search_in_postOrder(self.root, key)
        return nodo

    def printTree(self, data):
        Node.print_postOrder(self.root, data)

    def test_path(self, data, id):
        node =  Node.path_by_dic(self.root, data, id)
        if node.key < 0:
            return -1
        else:
            variable = node.data[2]
            if get_num_clase(data,node.data[0], variable) > 1:

                if(data[variable][id] == 1):
                    return 1
                else:
                    return 0
            else:
                if data[variable][node.data[0][0]] == 0:
                    return 0
                else:
                    return 1
    def traverse_tree(self, node, graph, pos, x=0, y=0, layer=1, h_sep=2, v_sep=1):
        if node:
            graph.add_node(node.key)
            pos[node.key] = (x, y)
            if node.left:
                graph.add_edge(node.key, node.left.key)
                self.traverse_tree(node.left, graph, pos, x - h_sep / (2**layer), y - v_sep, layer + 1, h_sep, v_sep)
            if node.right:
                graph.add_edge(node.key, node.right.key)
                self.traverse_tree(node.right, graph, pos, x + h_sep / (2**layer), y - v_sep, layer + 1, h_sep, v_sep)

    def visualize(self, h_sep=16, v_sep=1):
        """
        Visualiza el árbol binario.

        Parámetros:
        - h_sep: Separación horizontal inicial entre nodos.
        - v_sep: Separación vertical entre niveles.
        """
        graph = nx.DiGraph()
        pos = {}
        self.traverse_tree(self.root, graph, pos, h_sep=h_sep, v_sep=v_sep)
        plt.figure(figsize=(20, 10))
        nx.draw(graph, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_weight="bold")
        plt.show()