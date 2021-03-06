# implementacion de prueba de blockchain

Blockchain es un tipo de sistema que se compone de dos principios basicos:

- red p2p
- almacenamiento gestionado por concenso

## red p2p

blockchain se compone de un conjunto de nodos de tal manera que cada uno de ellos
puede comportarse a la vez como cliente o servidor, usualmente con propiedades de
descubrimiento de nodos, por lo cual cada miembro de la red puede ser conocido por
los demas, aumentando la capacidad de la red para estar disponible a peticiones.

## almacenamiento gestionado por concenso

en blockchain cada nodo completo posee una copia completa de la informacion del
sistema. para asegurar que cada copia es integra, la manera de gestionar la
informacion en la misma es a traves de un algoritmo de concenso.

estos algoritmos de concenso se basan usualmente en una competencia matematica
entre los diferentes nodos para organizar la informacion en paquetes llamados
bloques, los cuales dependen matematicamente unos de otros, haciendo que cada
bloque tenga a su vez la informacion suficiente para validar los datos anteriores,
lo cual hace que un atacante que quiera modificar un bloque determinado, tenga
que modificar una cantidad _n_ de bloques que va aumentando conforme pasa el tiempo,
lo que aumenta la dificultad de calculo de manera exponencial.


## uso de sistemas blockchain

el uso de sistemas blockchain se realiza cuando se presentan los siguientes
supuestos:

- no es posible tener el control del resto de participantes del sistema o
confiar en que el resto de participantes de un sistema no van a intentar
falsificar o corromper la informacion (zero trust systems)
- se necesita alta disponibilidad, redundancia y tolerancia a fallos
- puede permitirse altos tiempos de respuesta no-deterministicos y uso excesivo
de almacenamiento y recursos, asi­ como de ancho de banda
- los interesados del sistema se benefician de tener copias locales del sistema
- la verificacion de eventos en el tiempo es un requisito critico
- necesitas monetizar completamente su uso

## debilidades

- sistemas altamente ineficientes
- susceptibles a deserializacion insegura y a ataques con la metadata
- si un componente del sistema consigue el 51% del poder de computo, el sistema es inseguro
- poco escalable
- posibilidad de ramas secundarias (forks)


## acciones por hacer

- buscar diferentes algoritmos de concenso

## Ejemplos de protocolos de consenso 

Se han elaborado distintos protocolos o algoritmos que solucionan este tipo de problemas (https://es.wikipedia.org/wiki/Problema_del_consenso). 
Cada uno se aplica para cierto tipo de entornos y tienen sus propias caracteristicas. Veamos algunos ejemplos:

- Commit de dos fases
- Commit de tres fases
- Raft
- Paxos y Multipaxos
- Prueba de trabajo
- Prueba de participacion tanto en su version original como en la version prueba de participacion delegada.
- Prueba de quemadura
- Algoritmo de consenso Protocolo Ripple. Es el usado en Ripple y Stellar
- Zookeeper Atomic Broadcast
- Viewstamped replication

## elances de interes

- https://benediktkr.github.io/dev/2016/02/04/p2p-with-twisted.html
- https://github.com/macsnoeren/python-p2p-network
- https://www.welivesecurity.com/la-es/2018/09/04/blockchain-que-es-como-funciona-y-como-se-esta-usando-en-el-mercado/

- https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
- https://www.youtube.com/watch?v=kXyVqk3EbwE
- https://www.youtube.com/watch?v=oCS05QSQ-1k
- https://www.youtube.com/watch?v=Rvfs6Xx3Kww
