class Node:
    def __init__(self, clave, data):
        self.data = data
        self.key = clave
        self.right = None
        self.left = None

    @staticmethod
    def search_in_postOrder(node, clave):
        if node is None:
            return None
        if node.key == clave:
            return node
        # Traverse left and then right
        left_result = node.search_in_postOrder(node.left, clave)
        if left_result:
            return left_result
        return node.search_in_postOrder(node.right, clave)


    @staticmethod
    def print_postOrder(node, data):
        if(node.right != None):
            node.print_postOrder(node.right, data)
        if(node.left != None):
            node.print_postOrder(node.left, data)

        ind = node.data[0]
        exc = node.data[1]
        key = node.data[2]
        dat = node.data[3]
        if(node.left ==None):
            if(node.key >= 0):
                print(f"({node.key}, {key},  {dat}) , {Node.getClass(data, node.data[0], key )}")
            else:
                print(f'{node.key},{key}  NO RESULT')
        else:
            print(f'({node.key},{key}, {dat})')

    @staticmethod
    def getClass(data, index, variable):
        cals = data['class'][index[0]]
        flag = 0
        i=1
        for ind in index:
            if(cals != data[variable][ind]):
                flag = 1
                break
        if(flag == 0):
            if(cals == 1):
                return "GREEN"
            else:
                return "RED"
        else:
            if(data['class'][index[0]] == data[variable][index[0]]):
                return "BLUE"
        return "VIOLET"



# La clase node es un nodo que tiene dos enlaces, uno para la dereha y otro para la izuierda

    @staticmethod
    def path_by_dic(node, data, id):
        variable = node.data[2]
        if node is None:
            return None
        if node.right is None and node.left is None:
            return node
        #Traverse
        if(data[variable][id] == 1):
            return Node.path_by_dic(node.left, data, id)
        return Node.path_by_dic(node.right, data, id)
