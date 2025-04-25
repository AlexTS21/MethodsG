'''
Es donde este algoritmo correara
data = {
      'id' = [0,1,2,3,4,5,6,7]
      'class' =[1,0,1,0,0,0,1]
      'var1' = [1,1,1,0,0,1,0]
      'var2' = [1,0,1,0,0,0,1]
      'var3' = [1,1,1,0,0,1,0]
}
Necesitamos excluir las variables que ya no se utlizan
'''

import random
from collections import Counter

def Kmeans(data,  index, distance, exclude=['id', 'class'], grp=5,  maxiter=100, cenfunc=1):
    grups = {}
    centroides = {}
    vars =  [item for item in data.keys() if item not in exclude]
    #Obtener los centroides de forma aleatoria
    for i in range(grp):
        aux = {}
        num = random.choice(index)
        
        for var in vars:
            aux[var] = data[var][num]
        
        centroides[i] = aux
        #print(f'Se eligio el indice {num} y el objeto se ve asi {centroides[i]}')

    for i in range(maxiter):
        #Cada objeto lo metemos en su grupo correspondiente
        for a in range(grp):
            grups[a] = []
        for j in index:
            #Calcular la distancia menor del objeto a cada centroide
            dist = 2**31 - 1
            aux = 0
            for k in range(grp):
                aqui = distance(data, vars, centroides[k], j )
                #print(f'La distancia del centroide {k} es {aqui} y la ant es{dist}')
                if (aqui < dist):
                    dist = aqui
                    aux=k
            
            grups[aux].append(j)
        #print(f'los indices se ven asi {[len(grups[gr]) for gr in grups.keys()]}')
        #Recalcular los centroides
        for k in range(grp):
            for var in vars:
                if cenfunc == 1:
                    suma =sum(data[var][i] for i in grups[k])
                    if len(grups[k]) != 0:
                        centroides[k][var] = suma/len(grups[k])
                    else:
                        centroides[k][var] = 0
                elif cenfunc == 0:
                    valores = [data[var][i] for i in grups[k]]
                    contador = Counter(valores)
                    # Tomamos la moda (el valor más común)
                    try:
                        moda = contador.most_common(1)[0][0]
                    except:
                        moda = 0
                    centroides[k][var] = moda
            #print(f'el centride se ve asi {centroides[k]}')


    return grups