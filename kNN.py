from statistics import mean, sqrt
from math import fsum
import csv
import os
from datetime import datetime

def Coef_Linear(x,y):
    b = 0
    a1 = 0
    a2 = 0
    n = len(x)
    for i in range(n):
        a1 = x[i]*y[i]
        a2 = (x[i]**2)
    a = (a1 - n*mean(x)*mean(y))/(a2 - ((fsum(x)**2)/n))
    b = mean(y) - a*mean(x)
    return a,b

def Prediccion(u,v,t, ref):
    dist = []
    for fila in ref: #lista con los módulos cartesianos para su posterior organización así como el módulo del viento
        dist.append([sqrt(((u - fila[1])**2) + ((v - fila[2])**2) + ((t - fila[3])**2)), fila[0], fila[1], fila[2], fila[3], sqrt((fila[1]**2) + (fila[2]**2))])
    
    dist.sort(key = lambda x: x[0]) #hago una pequeña función lambda que organice el orden en la columna 0
    
    dist = dist[0:20] #selecciono los k=20 valores más cercanos
    
    #Realizo el ajuste entre el módulo del viento y la observación
    a,b = Coef_Linear([columna[-1] for columna in dist], [columna[1] for columna in dist])
    
    return a*sqrt((u**2) + (v**2)) + b #Sustituyo el módulo de la entrada y esta es la predicción

def errores(O,P):
    n = len(O)
    temp1 = []
    temp2= []
    for i in range(n):
        temp1.append(abs(O[0]-P[0]))
        temp2.append((O[0]-P[0])**2)
    
    EMA = (100/sum(O)) * sum(temp1)
    ECM = ((100 * n)/sum(O)) * (sqrt(sum(temp2))/n)
    
    return EMA, ECM

def es_enunciado(fila):
    try:
        list(map(float,fila))
        return False
    except ValueError or TypeError:
        return True

path = os.getcwd()
Referencia = []
Predecir = []
ref = False

with open(path + '/Meteologica_vacante_ProgPredR_ProblemaDatos_20240923.txt', mode ='r') as file:
    Temp = csv.reader(file) #Es un iterable compuesto por listas
    #Estructura de la lista [Observacion, u, v, t] y convierto los números string en float
    for fila in Temp:
        if es_enunciado(fila[0].split(sep = ';')): #filtro el enunciado
            if fila[0].split(sep = ';')[0] == 'observaciones': #reviso cuál enunciado es
                ref = True
            elif fila[0].split(sep = ';')[0] == 'predicciones':
                ref = False
        else:
            if ref == True: #Separo los bloques de entradas
                Referencia.append(list(map(float,fila[0].split(sep = ';')))) #convierto los valores a números
            else:
                Predecir.append(list(map(float,fila[0].split(sep = ';'))))
    
Predicciones = []

for a in Predecir:
    Predicciones.append([datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M'), Prediccion(a[-3], a[-2], a[-1], Referencia)])

EMA, ECM = errores([columna1[0] for columna1 in Predecir], [columna2[-1] for columna2 in Predicciones])

print('Errores referencia')

print(round(EMA,2),round(ECM,2))

print('Predicciones')

for i in Predicciones:
    print(i[0], i[1], round(i[2]))
