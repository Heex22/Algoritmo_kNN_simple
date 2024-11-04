### Realizado por Alex Kaseng He Expósito

# Introducción

La finalidad de este documento es explicar la implementación del código en kNN.py así como enseñar cómo hacer uso de este.

# El código

Se trata de un algoritmo kNN simplificado para 3 variables y 20 vecinos más cercanos, de momento no se ha agregado aprendizaje supervisado pero eventualmente se implementará.

# Implementación

El código hace uso de 4 funciones 2 de las cuales serán las principales protagonistas, estas consisten en:

-Prediccion: Esta función principal implementa un algoritmo kNN simplificado aprovechando un bucle en el cual se guardará la información relevante en una lista de listas (matriz),
en esta se va a filtrar por la columna que contiene la distancia euclídea de la referencia a la entrada en orden descendiente de tal forma que al realizar un slice hasta la fila k
tendríamos los k valores más cercanos y con dichos valores se realiza un ajuste lineal aprovechando la función secundaria Coef_Linear para obtener sus coeficientes y así tener la
recta cuyo valor 'y' será la salida. 

-errores: Implemento las fórmulas del apéndice A mediante la creación de dos listas temporales con un bucle for y estas funcionarán como el conjunto de elementos a sumar aplicando
la función sum().

-es_enunciado: Esta es una función secundaria que resulta fundamental en reconocer los diferentes tipos de bloques de entradas atrapando el error que se comete al intentar cambiar
strings por puntos flotantes cuando dichos carácteres son letras.

Además de estas funciones hay un script externo que toma la ruta en la que se encuentra el ejecutable y en esta solicita el archivo a leer, una vez lo encuentra lo lee
y separa en dos bloques de entradas las cuales se les aplicarán las funciones correspondientes para que a posteriori se imprima en pantalla el formato de salida pedido.

## Nota importante

En los datos de ejemplo sólo hay observaciones por lo que los he modificado de tal forma que se conforme al formato de entrada solicitado.

# Uso

Es importante que antes de usarlo, el nombre del archivo a leer sea el mismo en la ruta de lectura en el código del .py además de que su localización debe ser en el mismo
directorio. En primer lugar la terminal solicitará al usuario el nombre del archivo a leer, una vez se escriba imprimirá en pantalla la salida requerida.
