# Fuentes de Algoritmos y Adaptaciones Propias

## Punto 1: Algoritmos de Ordenamiento

| Algoritmo | Fuente | Adaptaciones propias |
|---|---|---|
| Insertion Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/insertion-sort-algorithm/) | Ninguna. |
| Dual-Pivot QuickSort | [GeeksforGeeks](https://www.geeksforgeeks.org/dual-pivot-quicksort/) | Partición integrada directamente en la recursión (sin método auxiliar que instancie tuplas de índices); particionado de 3 vías con punteros `lt`, `gt` e `i` en un solo bucle sin bucles `while` internos anidados. |
| Merge Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/merge-sort/) | Arreglo auxiliar único preasignado al inicio (evita instanciar arreglos `L[]` y `R[]` en cada llamada a mezcla como hace GfG); copias por bloque eficiente (`System.arraycopy`/slices). |
| Heap Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/heap-sort/) | Sift-down (`hundir`) iterativo en lugar del `heapify` recursivo de GfG, eliminando sobrecosto de pila de llamadas. |
| Radix Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/radix-sort/) | Reutilización de un único arreglo de salida preasignado (en GfG se asigna un `output[]` en cada dígito); uso de `long` para `exp` en Java para prevenir desbordamiento aritmético con claves de 8 dígitos; retorno temprano si $n < 2$. |
| Bucket Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/bucket-sort-2/) | Adaptación a enteros en rango arbitrario $[min, max]$ escalados a $k=n$ cubetas; eliminación de colecciones dinámicas (`Vector`/`ArrayList`) mediante conteo de prefijos sobre un arreglo plano contiguo ordenado con Insertion Sort por bloques. |

## Punto 2: Algoritmos de Búsqueda

| Algoritmo | Fuente | Adaptaciones propias |
|---|---|---|
| Linear Search | [GeeksforGeeks](https://www.geeksforgeeks.org/linear-search/) | Estandarización de interfaz `buscar(arr, x)` retornando el índice de la clave encontrada o `-1` si no existe. Implementación idéntica en Java y Python iterando secuencialmente. |
| Binary Search | [GeeksforGeeks](https://www.geeksforgeeks.org/binary-search/) | Implementación iterativa uniforme en ambos lenguajes con cálculo seguro de punto medio `mid = low + (high - low) / 2` para prevenir desbordamiento de enteros (*integer overflow*). |
| Ternary Search | [GeeksforGeeks](https://www.geeksforgeeks.org/ternary-search/) | Corrección del tipo de retorno: la versión de GeeksforGeeks retornaba un valor booleano (`true`/`false`). Se adaptó para retornar el índice entero de la coincidencia (`mid1`, `mid2`) o `-1` si está ausente, garantizando consistencia con los demás algoritmos del taller. |
| Jump Search | [GeeksforGeeks](https://www.geeksforgeeks.org/jump-search/) | Precomputación del tamaño de bloque `step = sqrt(n)` una sola vez en lugar de recalculaciones de punto flotante en cada iteración del bucle en Java (`Math.floor(Math.sqrt(n))`). Parada anticipada durante el sondeo lineal si `arr[prev] > x` en el arreglo ordenado. |
| Interpolation Search | [GeeksforGeeks](https://www.geeksforgeeks.org/interpolation-search/) | **1. Transformación a iterativo**: se reemplazó la recursión de GfG por bucle `while` para eliminar el sobrecosto de pila.<br>**2. Corrección de desbordamiento de enteros (Java)**: se convirtió el cálculo a `long` antes del producto `(long)(hi - lo) * (x - arr[lo])`, evitando desbordamiento a 32 bits y división entera errónea `(hi - lo)/(arr[hi] - arr[lo]) == 0` presente en la implementación ingenua de GfG.<br>**3. Control de división por cero**: validación cuando `arr[hi] == arr[lo]` para prevenir excepciones cuando los extremos son iguales. |
| Exponential Search | [GeeksforGeeks](https://www.geeksforgeeks.org/exponential-search/) | **1. Desacoplamiento de librerías nativas**: la versión de GfG en Java delegaba la búsqueda binaria en `Arrays.binarySearch`, mientras que la de Python utilizaba una función recursiva auxiliar. Se unificó utilizando la misma implementación iterativa de Búsqueda Binaria desarrollada para el taller en ambos lenguajes.<br>**2. Firma estandarizada**: invocación directa `buscar(arr, x)` abstrayendo el tamaño del arreglo. |
