# implementacion de prueba de blockchain

Blockchain es un tipo de sistema que se compone de dos principios basicos:

- red p2p
- almacenamiento gestionado por concenso

## red p2p

blockchain se compone de un conjunto de nodos de tal manera que cada uno de ellos
puede comportarse a la vez como cliente o servidor, usualmente con propiedades de
descubrimiento de nodos, por lo cual cada miembro de la red puede ser conocido por
los demás, aumentando la capacidad de la red para estar disponible a peticiones.

## almacenamiento gestionado por concenso

en blockchain cada nodo completo posee una copia completa de la información del
sistema. para asegurar que cada copia es integra, la manera de gestionar la
información en la misma es a través de un algoritmo de concenso.

estos algoritmos de concenso se basan usualmente en una competencia matemática
entre los diferentes nodos para organizar la información en paquetes llamados
bloques, los cuales dependen matematicamente unos de otros, haciendo que cada
bloque tenga a su vez la información suficiente para validar los datos anteriores,
lo cual hace que un atacante que quiera modificar un bloque determinado, tenga
que modificar una cantidad _n_ de bloques que va aumentando conforme pasa el tiempo,
lo que aumenta la dificultad de calculo de manera exponencial.


## uso de sistemas blockchain

el uso de sistemas blockchain se realiza cuando se presentan los siguientes
supuestos:

- no es posible tener el control del resto de participantes del sistema o
confiar en que el resto de participantes de un sistema no van a intentar
falsificar o corromper la información (zero trust systems)
- se necesita alta disponibilidad, redundancia y tolerancia a fallos
- puede permitirse altos tiempos de respuesta no-deterministicos y uso excesivo
de almacenamiento y recursos, así como de ancho de banda
- los interesados del sistema se benefician de tener copias locales del sistema
- la verificación de eventos en el tiempo es un requisito critico

## debilidades

- sistemas altamente ineficientes
- susceptibles a deserializacion insegura y a ataques con la metadata
- si un componente del sistema consigue el 51% del poder de computo, el sistema es inseguro
- poco escalable
- posibilidad de ramas secundarias (forks)


## acciones por hacer

- buscar diferentes algoritmos de concenso

## elances de interes

- https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html
- https://github.com/macsnoeren/python-p2p-network

- https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
- https://www.youtube.com/watch?v=kXyVqk3EbwE
- https://www.youtube.com/watch?v=oCS05QSQ-1k
- https://www.youtube.com/watch?v=Rvfs6Xx3Kww
