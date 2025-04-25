'''
Cabe recalcar que este codigo eta diseñado para dos clases
data = {
      'id' = [0,1,2,3,4,5,6,7]
      'class' =[1,0,1,0,0,0,1]
      'var1' = [1,1,1,0,0,1,0]
      'var2' = [1,0,1,0,0,0,1]
      'var3' = [1,1,1,0,0,1,0]
}
Necesitamos excluir las variables que ya no se
'''
import math

# Función para contar la cantidad de veces que un valor aparece en la variable
def contar_valor(data, index, variable, valor):
  return sum(1 for ind in index if data[variable][ind] == valor)

#Funcion para contar la cantidad de veces que un valor aparece en una clase
def contar_clase(data, index, variable, valor, clase):
  return sum(1 for ind in index if data[variable][ind] == valor and data['class'][ind] == clase)

def tamano_clase(data, index,  clase):
  return sum(1 for ind in index if data['class'][ind] == clase)

#Calcular la probabilidad condicional de un valor en una clase
def probabilidad_condicional(data, index, variable, valor, clase):
  p = 0
  if contar_valor(data, index, variable, valor) != 0:

    num = contar_clase(data, index, variable, valor, clase)
    den = contar_valor(data, index, variable, valor)
    p = num / den
  if p!= 0:


    return p * math.log(p, 2)
  else:
    return 0

# Calcular la probabilidad de que un valor sea tomado por la variable
def probabilidad_valor_en_variable(data, index, variable, valor):
    if len(index) == 0:
      return -1
    return contar_valor(data, index, variable, valor) / len(index)

# Calcular la probabilidad de que una clase ocurra en el conjunto de datos
def probabilidad_clase(data, index, variable, clase):
    return tamano_clase(data, index, variable, clase) / len(index)

# Calcular la suma de la entropía de una variable considerando una clase y un valor
def sumatoria_entropia_clases_variable(data, index, variable, valor):
    return probabilidad_condicional(data, index, variable, valor, 0) + probabilidad_condicional(data, index, variable, valor, 1)

# Calcular la entropía de una variable considerando los valores binarios (0, 1)
def entropia_variable(data, index, variable):
    p1 = probabilidad_valor_en_variable(data, index, variable,  1) * sumatoria_entropia_clases_variable(data, index, variable, 1)
    p0 = probabilidad_valor_en_variable(data, index, variable,  0) * sumatoria_entropia_clases_variable(data, index, variable, 0)
    return abs(p0 + p1)

# Calcular la entropía de una clase considerando su probabilidad
def entropia_clase(data, index, variable, clase):

    p = probabilidad_clase(data, index, variable, clase)
    return p * math.log(p, 2) if p != 0 else 0

# Calcular la entropía general de un conjunto de datos considerando todas las clases
def entropia_general(data, index, variable):
    return abs(entropia_clase(data, index, variable, 0) + entropia_clase(data, index, variable, 1))



def obtener_entropia_variables(data, index, exclude):
    filtered_headers = [header for header in data.keys() if header not in exclude]
    entropias = {}
    for key in filtered_headers:
        entropias[key] = entropia_variable(data, index, key)


    return entropias


def obtener_entropia_minima(data, index, exclude):
    entropias = obtener_entropia_variables(data, index, exclude)
    key = min(entropias, key=entropias.get)
    return key, entropias[key]

#Aun no se para que sirve
def obtener_valor(data, key):
    variable = data[key]
    return variable[0][0]


#OBTINE LOS INDICES DE UN VALOR X EN UNA VARIABLE
def obtener_indices(data, index, variable):
    in1 = []
    in0 = []

    for ind in index:
        if(data[variable][ind]  == 0):
            in0.append(ind)
        else:
            in1.append(ind)

    return in1, in0


def get_num_clase(data, index, variable):
    lis = []
    for ind in index:
        if data[variable][ind] not in lis:
            lis.append(data[variable][ind])
    return len(lis)


def iterable_data(data, index, exclude):
    if len(index) == 0:
      return False
    if len(data.keys()) - len(exclude)<2:
      return False
    return True