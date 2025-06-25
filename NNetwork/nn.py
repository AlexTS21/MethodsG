from .layer import layer
import numpy as np

class nn:
    def __init__(self, layers, functions):
        self.layers = layers.copy()
        self.normalizacion = {}
        for l in range(len(layers)):
            #Si es la primera capa no jalar funcion
            if l == 0:
                self.layers[l] = layer(layers[l])
            #Agregar la funcion en las capas y conectarlas
            else:
                self.layers[l] = layer(layers[l], functions[l-1])
                #Conectar las capas
                self.layers[l-1].conect(self.layers[l])

    def forward(self, patron):
        #Rercorrer las capas 
        for c in range(len(self.layers)):
            #c es indice una capa
            #Primera capa la activacion es el patron
            if c == 0:
                self.layers[c].act = patron.copy()
            else:
                #Sumatoira
                #print(f'Trabajando en la capa {c} con los pesos de la capa {c-1}')
                aux = np.dot(self.layers[c-1].weights, self.layers[c-1].act) + self.layers[c].bias
                for i in range(len(aux)):
                    self.layers[c].act[i] = self.layers[c].fun(aux[i])
        return self.layers[-1].act

    def backPropagation(self, salida, learningRate=0.1):
        #Por cada capa desde atras
        #C es una indice de capa se recorre desde el final hasta el segundo
        err = sum(((salida - self.layers[-1].act)**2)/2)
        for c in range(len(self.layers) - 1, 0, -1):
            #Para la ultima capa
            if c == len(self.layers)-1:
                #Crear array de (si - yi)
                errP = -(salida - self.layers[c].act)
                #Por cada neurona actualizar bias y peso relacionado
                for i in range(len(self.layers[c].bias)):
                    #calcular delta de la neurona
                    self.layers[c].delta[i] = errP[i]*self.layers[c].funD(self.layers[c].act[i])
                    self.layers[c].bias[i] = self.layers[c].bias[i] - learningRate*self.layers[c].delta[i]
                    #Pesos de la capa pasada      pesos de la capa pasada                             activacion de la capa pasada
                    self.layers[c-1].weights[i] = self.layers[c-1].weights[i] - (learningRate*self.layers[c].delta[i]) * self.layers[c-1].act.copy() 

            else:
                #Programamos para las capas ocultas
                #Calculo del nuevo delta neesistamos la sumatoria de todos los deltas por pesos de la capa siguiente
                delta_ant = np.sum(np.dot(self.layers[c+1].delta, self.layers[c].weights))
                #Para cada neurona de la capa
                for i in range(len(self.layers[c].bias)):
                    #Funcion derivada evaulada en weights*activacion +umbral = actviacion de esta neurona
                    self.layers[c].delta[i] = delta_ant*self.layers[c].funD(self.layers[c].act[i])
                    #Bias de la neurona
                    self.layers[c].bias[i] = self.layers[c].bias[i] - learningRate*self.layers[c].delta[i]
                    #Weights
                    self.layers[c-1].weights[i] = self.layers[c-1].weights[i] - (learningRate*self.layers[c].delta[i]) * self.layers[c-1].act.copy() 
        return err
    
    def backPropagationC(self, salida, learningRate=0.1):
        err = np.sum(((salida - self.layers[-1].act) ** 2) / 2)

        # Recorrer de la última capa hacia la primera oculta
        for c in range(len(self.layers) - 1, 0, -1):
            capa = self.layers[c]
            capa_anterior = self.layers[c - 1]

            # Si es la capa de salida
            if c == len(self.layers) - 1:
                # Calcular delta: (y - s) * f'(z)
                error = capa.act - salida  # Ojo: salida es la esperada
                capa.delta = error * np.array([capa.funD(a) for a in capa.act])

            else:
                # Capa oculta: delta = sum(delta_siguiente * pesos) * f'(z)
                # pesos de la capa actual: (n_siguiente, n_actual)
                suma = np.dot(self.layers[c].weights.T, self.layers[c + 1].delta)
                capa.delta = suma * np.array([capa.funD(a) for a in capa.act])

            # Actualizar pesos y bias usando los deltas
            for i in range(capa.n):
                capa.bias[i] -= learningRate * capa.delta[i]
                capa_anterior.weights[i] -= learningRate * capa.delta[i] * capa_anterior.act
                # Nota: capa_anterior.weights[i] afecta a la neurona i de la capa actual

        return err



    def evaluate(self, x, normalizar=False):
        if normalizar:
            x = self.normalizar(x, self.normalizacion["x_min"], self.normalizacion["x_max"])
            out = self.forward(x)
            return self.desnormalizar_minmax(out, self.normalizacion["s_min"], self.normalizacion["s_max"])
        else:
            return self.forward(x)
 
    
    def error(self, X, S):
        error = 0
        for x, s in zip(X, S):
            y = self.forward(x)
            error += sum(((s - y)**2)/2)
        return error/len(X)

                
    def train(self, X, S, epoch=100, learningRate=0.1, normalizar=False, quiet=True):
        if normalizar:
            x_min, x_max = X.min(), X.max()
            s_min, s_max = S.min(), S.max()
            self.normalizacion = {
                "x_min": x_min, "x_max": x_max,
                "s_min": s_min, "s_max": s_max
            }
            X = self.normalizar_vec(X, x_min, x_max)
            S = self.normalizar_vec(S, s_min, s_max)
           

        for e in range(epoch):
            for x, s in zip(X, S):
                self.forward(x)
               
                self.backPropagationC(s, learningRate=learningRate)
            if not quiet:
                print(f'Epoca: {e} Error: {self.error(X, S)}')
        print(f'Error en la red: {self.error(X, S)}')

    def validacion(self, X, S, epoch=100, normalizar=False, learningRate=0.01, val=0.8):
        #Split data
        len(X)
        trainX = X[:int(len(X)*val)]
        trainS = S[:int(len(X)*val)]
        testX = X[int(len(X)*val):]
        testS = S[int(len(X)*val):]
        if normalizar:
            x_min, x_max = trainX.min(), trainX.max()
            s_min, s_max = trainS.min(), trainS.max()
            self.normalizacion = {
                "x_min": x_min, "x_max": x_max,
                "s_min": s_min, "s_max": s_max
            }
            trainX = self.normalizar_vec(trainX, x_min, x_max)
            trainS = self.normalizar_vec(trainS, s_min, s_max)
            testX = self.normalizar_vec(testX, x_min, x_max )
            testS = self.normalizar_vec(testS, s_min, s_max)

        self.train(trainX, trainS, epoch=epoch, learningRate=learningRate, normalizar=normalizar)

        #Evaluar
        
    @staticmethod
    def normalizar(x, xmin, xmax, a=0, b=1):
        return a + (x - xmin) * (b - a) / (xmax - xmin)

    @staticmethod
    def normalizar_vec(X, xmin=None, xmax=None, a=0, b=1):
        if xmin is None:
            xmin = X.min()
        if xmax is None:
            xmax = X.max()
        return a + (X - xmin) * (b - a) / (xmax - xmin)

    @staticmethod
    def desnormalizar_minmax(x_norm, xmin, xmax, a=0, b=1):
        return ((x_norm - a) * (xmax - xmin)) / (b - a) + xmin
