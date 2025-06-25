import numpy as np

class layer:
        #Por default genera una capa de entrada
        #numero de neuronas, activacion, capa de entrada?
    def __init__(self, nc, activation=None):
        alpha = 0.01
        function = {
            "identidad": lambda x: x,
            "sigmoide": lambda x: 1/(1+np.exp(-x)),
            "tanh": lambda x: np.tanh(x),
            "relu": lambda x: np.maximum(0, x),
            "leaky_relu": lambda x: x if x > 0 else alpha * x,
            "pol": lambda x, w: x**w
        }
        functionD ={
            "identidad": lambda x: 1,
            "sigmoide": lambda x: (1/(1+np.exp(-x))) * (1 - (1/(1+np.exp(-x)))),
            "tanh": lambda x: 1 - np.tanh(x)**2,
            "relu": lambda x: 1 if x > 0 else 0 ,
            "leaky_relu": lambda x: 1 if x > 0 else alpha,
            "pol": lambda x, w: w*x**(w-1)
        }
        #Si no es primera capa agregar bias
        if activation:
            self.bias = np.random.rand(nc)
            self.delta = np.empty(nc)
            self.fun = function[activation]
            self.funD = functionD[activation]
        self.actF = activation
        self.act = np.empty(nc)
        self.weights = None
        self.n = nc

    #Todas las capas menos la ultima tienen un arreglo de pesos
    def conect(self, nl):
        self.weights = np.random.randn(nl.n, self.n) * np.sqrt(2 / self.n)
        
    def sumary(self):
        print(f'N neuronas: {self.n}')
        if self.actF:
            print(f'Activacion: {self.actF}')
