from statistics import mean, sqrt
from math import fsum
import csv
import os
from collections import Counter

def Coef_Linear(x,y):
    '''Esta función calcula el coeficiente linear primero realizando la pendiente a en dos partes a1 y a2, 
    una vez se tiene el valor de a puedo computar la ordenada en el origen b'''
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

def Calc_Prediccion(u,v,t, ref):
    '''Predice la producción del parque eólico mediante un algoritmo simplificado de kNN con k = 20. 
    Primero empieza con una lista que guarde la distancia euclídea de las coordenadas u,v y t respecto
    a la entrada así como estas y su módulo para un posterior cálculo, después con una función simple 
    lambda y el método sort filtro los datos por la columna de la distancia euclídea en orden ascendente
    luego realizo un slice hasta k = 20 para obtener los 20 vecinos más cercanos.
    
    Finalmente llamo a la función Coef_linear para realizar el ajuste del módulo de u y v con las 
    observaciones y con esos coeficientes obtener la predicción basada en la entrada.'''
    data = []
    for fila in ref: #lista con los módulos cartesianos para su posterior organización así como el módulo del viento
        data.append([sqrt(((u - fila[1])**2) + ((v - fila[2])**2) + ((t - fila[3])**2)), fila[0], fila[1], fila[2], fila[3], sqrt((fila[1]**2) + (fila[2]**2))])
    
    data.sort(key = lambda x: x[0]) #hago una pequeña función lambda que organice el orden en la columna 0
    
    data = data[0:20] #selecciono los k=20 valores más cercanos
    
    #Realizo el ajuste entre el módulo del viento y la observación
    a,b = Coef_Linear([columna[-1] for columna in data], [columna[1] for columna in data])
    
    return a*sqrt((u**2) + (v**2)) + b #Sustituyo el módulo de la entrada y esta es la predicción

def errores(O,P):
    '''Calcula el error medio absoluto (EMA) y el error cuadrático medio (ECM) usando las fórmulas del
    apéndice A del pdf.'''
    n = len(O)
    sum1 = []
    sum2= []
    for i in range(n):
        sum1.append(abs(O[0]-P[0]))
        sum2.append((O[0]-P[0])**2)
    
    EMA = (100/sum(O)) * sum(sum1)
    ECM = ((100 * n)/sum(O)) * (sqrt(sum(sum2))/n)
    
    return EMA, ECM

def es_enunciado(fila):
    '''Función cuyo objetivo es funcionar dentro de un if para atrapar los errores que cause el cambio
    de strings a floats al leer los datos'''
    try:
        list(map(float,fila[-3:])) #Dónde tengo que comprobar es en las últimas tres filas
        return False
    except ValueError or TypeError:
        return True

'''Obtengo el directorio en el que se encuentra el .py y solicito el nombre del archivo de texto del que
se realizará la lectura'''
path = os.getcwd()
archivo = input('Introduce el nombre del archivo a usar junto con su extensión ') #Meteologica_vacante_ProgPredR_ProblemaDatos_20240923.txt
#Inicializo las variables
Referencia = []
Predecir = []
switch = False



'''Leo el archivo asegurándome de separar las entradas en dos bloques así como cambiar el tipo de los 
elementos en la lista de carácter a números de punto flotante.'''

with open(path + '/' + archivo, mode ='r') as file:
    Temp = csv.reader(file) #Es un iterable compuesto por listas y temporal
    #Estructura de la lista [Observacion, u, v, t] y convierto los números string en float
    for fila in Temp:
        if es_enunciado(fila[0].split(sep = ';')): #filtro el enunciado
            if fila[0].split(sep = ';')[0] == 'observaciones': #reviso cuál enunciado es
                switch = True
            elif fila[0].split(sep = ';')[0] == 'predicciones':
                switch = False
        else:
            if switch == True: #Separo los bloques de entradas
                Referencia.append(list(map(float,fila[0].split(sep = ';')))) #convierto los valores a números
            else:
                fila_temporal = fila[0].split(sep = ';')
                Predecir.append(fila_temporal[:2] + list(map(float,fila_temporal[-3:])))

'''Esta parte se asegura que aunque las observaciones y las predicciones no estén ordenadas los puntos
que comparten existen y extrae las filas en las que hay coincidencia con el fin calcular la salida. Para
ello hago uso de las tuplas para hacer inmutables las filas y luego lo convierto en counters (tipo de
almacenamiento especializado) de la librería collections nativa a Python con el fin de tener eficiencia 
y contemplar la existencia de filas en las que u,v y t se repiten pero la observación es diferente.'''

cuenta_obs = Counter(tuple(fila[-3:]) for fila in Referencia)
cuenta_predct = Counter(tuple(fila[-3:]) for fila in Predecir)
#Es importante tomar las tres últimas filas porque en los dos formatos es donde aparece u,v y t
coincidencias = []

for elemento in cuenta_obs: #Recorro las columnas que quiero comprobar
    if elemento in cuenta_predct:
        #Busco el mínimo de apariciones que se repiten para ver cuáles coinciden 
        repeticiones = min(cuenta_obs[elemento], cuenta_predct[elemento])
        #Añadir el elemento repetido el número de veces que coinciden
        coincidencias.extend([list(elemento)] * repeticiones)
        
#Recupero las filas completas usando la intersección
coinciden_obs = [] #Se usará para los errores
coinciden_predct = [] #Se usará en el cálculo

for fila in Referencia:
    if fila[-3:] in coincidencias:
        coinciden_obs.append(fila)

for fila in Predecir:
    if fila[-3:] in coincidencias:
        coinciden_predct.append(fila)


'''Esta parte crea la salida del programa y simplemente crea las variables de las cuales se va a extraer
las impresiones.'''

Predicciones = []

for a in coinciden_predct:
    Predicciones.append([a[0], a[1], Calc_Prediccion(a[-3], a[-2], a[-1], Referencia)])

EMA, ECM = errores([columna1[0] for columna1 in coinciden_obs], [columna2[-1] for columna2 in Predicciones])

print('Errores referencia')

print(round(EMA,2),round(ECM,2))

print('Predicciones')

for i in Predicciones:
    print(i[0], i[1], round(i[2]))
