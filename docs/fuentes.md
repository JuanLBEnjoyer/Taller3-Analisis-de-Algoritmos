| Algoritmo | Fuente | Adaptaciones propias |
|---|---|---|
| Insertion Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/insertion-sort-algorithm/) | Ninguna. |
| Dual-Pivot QuickSort | [GeeksforGeeks](https://www.geeksforgeeks.org/dual-pivot-quicksort/) | Partición integrada directamente en la recursión (sin método auxiliar que instancie tuplas de índices); particionado de 3 vías con punteros `lt`, `gt` e `i` en un solo bucle sin bucles `while` internos anidados. |
| Merge Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/merge-sort/) | Arreglo auxiliar único preasignado al inicio (evita instanciar arreglos `L[]` y `R[]` en cada llamada a mezcla como hace GfG); copias por bloque eficiente (`System.arraycopy`/slices). |
| Heap Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/heap-sort/) | Sift-down (`hundir`) iterativo en lugar del `heapify` recursivo de GfG, eliminando sobrecosto de pila de llamadas. |
| Radix Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/radix-sort/) | Reutilización de un único arreglo de salida preasignado (en GfG se asigna un `output[]` en cada dígito); uso de `long` para `exp` en Java para prevenir desbordamiento aritmético con claves de 8 dígitos; retorno temprano si $n < 2$. |
| Bucket Sort | [GeeksforGeeks](https://www.geeksforgeeks.org/bucket-sort-2/) | Adaptación a enteros en rango arbitrario $[min, max]$ escalados a $k=n$ cubetas; eliminación de colecciones dinámicas (`Vector`/`ArrayList`) mediante conteo de prefijos sobre un arreglo plano contiguo ordenado con Insertion Sort por bloques. |
