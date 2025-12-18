"""Datos iniciales de lecciones para PiLearn.

Nota: Esta base puede ampliarse con más lecciones según el currículo.
"""


def get_lecciones_iniciales():
    """
    Retorna lista de tuplas con lecciones iniciales
    """
    return [

                (
                    "Aprendamos a Sumar y Restar",
                    "matematicas",
                    "basico",
                    "aritmetica",
                    """
=== SUMAR Y RESTAR: TUS PRIMERAS OPERACIONES ===

¿QUE ES SUMAR?
Sumar es juntar cosas. Imagina que tienes caramelos:
- Tienes 3 caramelos rojos
- Tu amigo te da 5 caramelos azules
- Ahora tienes 3 + 5 = 8 caramelos en total

Se lee: "tres MAS cinco IGUAL a ocho"

¿QUE ES RESTAR?
Restar es quitar cosas. Siguiendo con los caramelos:
- Tienes 10 caramelos
- Te comes 4 caramelos
- Te quedan 10 - 4 = 6 caramelos

Se lee: "diez MENOS cuatro IGUAL a seis"


--- SUMA DE NUMEROS GRANDES ---

A veces los numeros son grandes y necesitamos "llevar":

Ejemplo: 145 + 67
  
  1 4 5
+   6 7
-------

Paso 1: Suma las unidades (5 + 7 = 12)
        Escribe 2 y lleva 1

Paso 2: Suma las decenas (4 + 6 = 10, mas el 1 que llevamos = 11)
        Escribe 1 y lleva 1

Paso 3: Suma las centenas (1 + 0 = 1, mas el 1 que llevamos = 2)

Resultado: 212


--- RESTA DE NUMEROS GRANDES ---

A veces necesitamos "pedir prestado":

Ejemplo: 521 - 347

  5 2 1
- 3 4 7
-------

Paso 1: Unidades (1 no puede menos 7)
        Pide prestado: 11 - 7 = 4

Paso 2: Decenas (1 no puede menos 4, porque prestamos)
        Pide prestado: 11 - 4 = 7

Paso 3: Centenas (4 - 3 = 1)

Resultado: 174


RECUERDA:
* Siempre empieza desde la derecha (unidades)
* Alinea bien los numeros
* Verifica tu respuesta sumando o restando al reves
                    """,
                    """
=== PRACTICA CON ESTOS EJEMPLOS ===

SUMAS FACILES:
--------------
1) 32 + 41 = ?
   
   Unidades: 2 + 1 = 3
   Decenas: 3 + 4 = 7
   
   Respuesta: 73


2) 58 + 26 = ?
   
   Unidades: 8 + 6 = 14 (escribo 4, llevo 1)
   Decenas: 5 + 2 = 7, mas 1 que llevo = 8
   
   Respuesta: 84


RESTAS FACILES:
--------------
3) 95 - 42 = ?
   
   Unidades: 5 - 2 = 3
   Decenas: 9 - 4 = 5
   
   Respuesta: 53


4) 73 - 28 = ?
   
   Unidades: 3 no puede menos 8, pido prestado
            13 - 8 = 5
   Decenas: 6 - 2 = 4 (porque preste 1)
   
   Respuesta: 45


DESAFIO MAS DIFICIL:
-------------------
5) 234 + 189 = ?
   
   4 + 9 = 13 (escribo 3, llevo 1)
   3 + 8 = 11, mas 1 = 12 (escribo 2, llevo 1)
   2 + 1 = 3, mas 1 = 4
   
   Respuesta: 423
                    """,
                    """
=== TRUCOS Y CONSEJOS PARA SER UN EXPERTO ===

TRUCOS PARA SUMAR MAS RAPIDO:
-----------------------------
* Si sumas 9, es como sumar 10 y restar 1
  Ejemplo: 25 + 9 = 25 + 10 - 1 = 34

* Suma los numeros redondos primero
  Ejemplo: 23 + 47 = 20 + 40 + 3 + 7 = 60 + 10 = 70

* Usa tus dedos para numeros pequeños


TRUCOS PARA RESTAR MAS RAPIDO:
-----------------------------
* Si restas 9, es como restar 10 y sumar 1
  Ejemplo: 35 - 9 = 35 - 10 + 1 = 26

* Cuenta hacia arriba
  Ejemplo: 50 - 23 = ?
  Piensa: 23 + ? = 50
  23 + 7 = 30, 30 + 20 = 50
  Entonces 7 + 20 = 27


COMO VERIFICAR TUS RESPUESTAS:
-----------------------------
* Si hiciste una suma: resta el resultado
  Ejemplo: 12 + 8 = 20
  Verificar: 20 - 8 = 12 (Correcto!)

* Si hiciste una resta: suma el resultado
  Ejemplo: 20 - 8 = 12
  Verificar: 12 + 8 = 20 (Correcto!)


PRACTICA DIVERTIDA:
------------------
* Cuenta tus juguetes, libros o lapices
* Suma los puntos cuando juegues
* Cuenta cuanto dinero tienes
* Ayuda en la cocina midiendo ingredientes

Recuerda: Todos cometemos errores, lo importante es aprender!
                    """,
                    15,
                    1
                ),
                
                (
                    "Multiplicación y División",
                    "matematicas",
                    "basico",
                    "aritmetica",
                    """
MULTIPLICACIÓN Y DIVISIÓN

1. MULTIPLICACIÓN (×)
   - Suma repetida
   - 3 × 4 = 3 + 3 + 3 + 3 = 12
   - Leer: "tres POR cuatro IGUAL doce"
   
   TABLAS DE MULTIPLICAR:
   • Tabla del 2: 2,4,6,8,10,12,14,16,18,20
   • Tabla del 5: 5,10,15,20,25,30,35,40,45,50
   • Tabla del 10: 10,20,30,40,50,60,70,80,90,100

2. DIVISIÓN (÷)
   - Repartir en partes iguales
   - 12 ÷ 3 = 4
   - Leer: "doce ENTRE tres IGUAL cuatro"
   - Significa: "¿Cuántas veces cabe 3 en 12?"

3. MULTIPLICACIÓN DE DOS DÍGITOS
   - Ejemplo: 24 × 13
   - Paso 1: 24 × 3 = 72
   - Paso 2: 24 × 10 = 240
   - Paso 3: 72 + 240 = 312

4. RELACIÓN ENTRE × y ÷
   - Son operaciones inversas
   - Si 3 × 4 = 12, entonces 12 ÷ 3 = 4
   - Verifica divisiones multiplicando
                    """,
                    """
EJEMPLOS:

1) 7 × 8 = ?
   7 × 8 = 56 (tabla del 7)

2) 36 ÷ 6 = ?
   ¿6 por qué numero da 36?
   6 × 6 = 36
   Respuesta: 6

3) 15 × 4 = ?
   Método 1: 15 + 15 + 15 + 15 = 60
   Método 2: 10×4=40, 5×4=20, 40+20=60

4) 144 ÷ 12 = ?
   ¿12 por qué número da 144?
   12 × 12 = 144
   Respuesta: 12
                    """,
                    """
TRUCOS:
• Tabla del 9: la suma de dígitos da 9
  (9×2=18: 1+8=9, 9×3=27: 2+7=9)
• Multiplicar por 10: agregar un 0
• Dividir por 10: quitar un 0
• Aprende las tablas del 2, 5 y 10 primero
                    """,
                    20,
                    2
                ),
                
                (
                    "Fracciones Básicas",
                    "matematicas",
                    "basico",
                    "fracciones",
                    """
INTRODUCCIÓN A LAS FRACCIONES

1. ¿QUÉ ES UNA FRACCIÓN?
   - Representa PARTES de un ENTERO
   - Ejemplo: 1/2 = una mitad
   - Formato: NUMERADOR / DENOMINADOR
   
   Numerador: partes que tomamos
   Denominador: partes totales

2. FRACCIONES COMUNES
   • 1/2 = mitad (medio)
   • 1/3 = un tercio
   • 1/4 = un cuarto
   • 3/4 = tres cuartos

3. SUMA DE FRACCIONES (mismo denominador)
   - Se suman los numeradores
   - El denominador se mantiene
   - Ejemplo: 1/4 + 2/4 = 3/4

4. ENCONTRAR COMÚN DENOMINADOR
   - Para sumar fracciones diferentes
   - Ejemplo: 1/2 + 1/4
     * 1/2 = 2/4 (multiplicar por 2)
     * 2/4 + 1/4 = 3/4

5. FRACCIONES EQUIVALENTES
   - Representan la misma cantidad
   - Ejemplos:
     * 1/2 = 2/4 = 4/8
     * 1/3 = 2/6 = 3/9
                    """,
                    """
EJEMPLOS VISUALES:

Pizza de 8 rebanadas:
• 1/2 de pizza = 4 rebanadas
• 1/4 de pizza = 2 rebanadas
• 3/4 de pizza = 6 rebanadas

EJERCICIOS:

1) 1/3 + 1/3 = ?
   Mismo denominador: suma numeradores
   1 + 1 = 2
   Respuesta: 2/3

2) 1/2 + 1/4 = ?
   Convertir 1/2 a cuartos: 1/2 = 2/4
   2/4 + 1/4 = 3/4

3) 2/5 + 1/5 = ?
   2 + 1 = 3
   Respuesta: 3/5
                    """,
                    """
CONSEJOS:
• Dibuja círculos y divídelos
• Usa objetos reales (chocolates, pizza)
• El denominador dice "en cuántos pedazos"
• El numerador dice "cuántos tomo"
• Practica con comida, es más divertido!
                    """,
                    15,
                    3
                ),
                
                # INGLÉS - BÁSICO
                (
                    "Vocabulario Básico en Inglés",
                    "ingles",
                    "basico",
                    "vocabulario",
                    """
VOCABULARIO ESENCIAL EN INGLÉS

1. LA CASA (HOME)
   • House = casa
   • Door = puerta
   • Window = ventana
   • Room = habitación
   • Kitchen = cocina
   • Bathroom = baño

2. LA FAMILIA (FAMILY)
   • Father/Dad = padre/papá
   • Mother/Mom = madre/mamá
   • Brother = hermano
   • Sister = hermana
   • Family = familia

3. ANIMALES (ANIMALS)
   • Dog = perro
   • Cat = gato
   • Bird = pájaro
   • Fish = pez

4. OBJETOS COMUNES
   • Book = libro
   • Table = mesa
   • Chair = silla
   • Computer = computadora
   • Phone = teléfono

5. BEBIDAS Y COMIDAS
   • Water = agua
   • Milk = leche
   • Bread = pan
   • Apple = manzana

PRONUNCIACIÓN:
• House: JAUS
• Dog: DOG
• Cat: KAT
• Water: UÓTER
• Book: BUK
                    """,
                    """
PRÁCTICA CON FRASES:

1) "This is my house"
   (Dis is mai jaus)
   = Esta es mi casa

2) "I have a dog"
   (Ai jav a dog)
   = Tengo un perro

3) "I like books"
   (Ai laik buks)
   = Me gustan los libros

4) "My family is big"
   (Mai famili is big)
   = Mi familia es grande

EJERCICIOS:
• Etiqueta objetos en tu casa
• Di las palabras en voz alta
• Practica con un espejo
                    """,
                    """
TÉCNICAS DE MEMORIZACIÓN:
• Asocia palabras con imágenes
• Crea flashcards
• Ve películas con subtítulos
• Escucha música en inglés
• Practica 10 palabras por día
• Usa post-its en objetos
                    """,
                    10,
                    1
                ),
                
                # MATEMÁTICAS - INTERMEDIO
                (
                    "Fracciones: La Magia de Dividir",
                    "matematicas",
                    "intermedio",
                    "fracciones",
                    """
=== ENTENDIENDO LAS FRACCIONES ===

¿QUE ES UNA FRACCION?
Una fraccion es una forma de representar PARTES de algo completo.

Imagina una pizza:
- La pizza completa = 1 pizza entera
- Si la cortas en 4 partes iguales = 4/4
- Si comes 1 pedazo = 1/4
- Si comes 3 pedazos = 3/4

PARTES DE UNA FRACCION:
  
  3  ← NUMERADOR (cuantos pedazos tomas)
  -
  4  ← DENOMINADOR (en cuantas partes divides)


--- FRACCIONES COMUNES ---

1/2 = Una mitad (medio)
    Ejemplo: Media manzana, medio vaso

1/4 = Un cuarto
    Ejemplo: Un cuarto de hora (15 minutos)

3/4 = Tres cuartos
    Ejemplo: Tres cuartos de pizza

1/3 = Un tercio
    Ejemplo: Un tercio del pastel


--- SUMAR FRACCIONES (MISMO DENOMINADOR) ---

Cuando el denominador es igual, solo sumas los numeradores:

Ejemplo: 2/5 + 1/5 = ?

Paso 1: Denominadores iguales (5)
Paso 2: Suma numeradores: 2 + 1 = 3
Resultado: 3/5


--- SUMAR FRACCIONES (DIFERENTE DENOMINADOR) ---

Necesitas encontrar un denominador comun:

Ejemplo: 1/2 + 1/4 = ?

Paso 1: Convertir 1/2 a cuartos
        1/2 = 2/4 (multiplicas arriba y abajo por 2)

Paso 2: Ahora suma: 2/4 + 1/4 = 3/4


--- MULTIPLICAR FRACCIONES ---

Es mas facil que sumar!

Ejemplo: 1/2 × 3/4 = ?

Paso 1: Multiplica numeradores: 1 × 3 = 3
Paso 2: Multiplica denominadores: 2 × 4 = 8

Resultado: 3/8


--- FRACCIONES EQUIVALENTES ---

Son fracciones que representan la misma cantidad:

1/2 = 2/4 = 3/6 = 4/8 = 5/10

Todas son IGUALES, solo estan escritas diferente!


RECUERDA:
* El denominador dice en cuantas partes divides
* El numerador dice cuantas partes tomas
* Practica con objetos reales (chocolates, frutas)
                    """,
                    """
=== PRACTICA CON FRACCIONES ===

IDENTIFICAR FRACCIONES:
----------------------
1) Tienes una barra de chocolate con 8 cuadros.
   Te comes 3 cuadros.
   
   Fraccion: 3/8 (tres octavos)


2) Un pastel se divide en 6 pedazos.
   Quedan 5 pedazos.
   
   Fraccion: 5/6 (cinco sextos)


SUMAS CON MISMO DENOMINADOR:
----------------------------
3) 3/7 + 2/7 = ?
   
   Denominador igual (7)
   Suma numeradores: 3 + 2 = 5
   
   Respuesta: 5/7


4) 5/9 + 3/9 = ?
   
   5 + 3 = 8
   
   Respuesta: 8/9


SUMAS CON DIFERENTE DENOMINADOR:
--------------------------------
5) 1/3 + 1/6 = ?
   
   Convertir 1/3 a sextos:
   1/3 = 2/6
   
   Ahora: 2/6 + 1/6 = 3/6
   
   Simplificar: 3/6 = 1/2


MULTIPLICACIONES:
----------------
6) 2/3 × 1/4 = ?
   
   Numeradores: 2 × 1 = 2
   Denominadores: 3 × 4 = 12
   
   Resultado: 2/12 = 1/6 (simplificado)


PROBLEMAS DEL MUNDO REAL:
-------------------------
7) Tienes 3/4 de litro de jugo.
   Tomas 1/4 de litro.
   ¿Cuanto queda?
   
   3/4 - 1/4 = 2/4 = 1/2 litro


8) Una receta necesita 1/2 taza de azucar.
   Quieres hacer el doble.
   ¿Cuanta azucar necesitas?
   
   1/2 × 2 = 2/2 = 1 taza completa
                    """,
                    """
=== TRUCOS PARA DOMINAR LAS FRACCIONES ===

TRUCOS DE SUMA:
--------------
TRUCO 1: Mismo denominador
Solo suma los numeradores!
2/5 + 1/5 = 3/5

TRUCO 2: Busca multiplos
Para 1/2 + 1/4: piensa en 4
1/2 = 2/4, entonces 2/4 + 1/4 = 3/4

TRUCO 3: Visualiza
Dibuja circulos o rectangulos
Colorea las partes


TRUCOS DE MULTIPLICACION:
------------------------
TRUCO 1: Linea por linea
Arriba × arriba
Abajo × abajo

TRUCO 2: Simplifica ANTES
Si puedes, simplifica antes de multiplicar
2/4 × 1/2 = 1/2 × 1/2 = 1/4


COMO SIMPLIFICAR:
----------------
Dividir arriba y abajo por el mismo numero

4/8 ÷ 2 = 2/4 ÷ 2 = 1/2

Busca el numero mas grande que divide a ambos


FRACCIONES EN LA VIDA REAL:
--------------------------
* Cocinar: 1/2 taza, 3/4 cucharada
* Tiempo: 1/4 de hora = 15 minutos
* Dinero: 1/2 dolar = 50 centavos
* Deportes: 3/4 partes del juego
* Musica: 1/2 nota, 1/4 nota


PRACTICA DIVERTIDA:
------------------
* Corta frutas en partes iguales
* Reparte dulces entre amigos
* Mide ingredientes en la cocina
* Usa bloques de construccion
* Colorea dibujos por fracciones

Recuerda: Las fracciones estan en todos lados!
                    """,
                    20,
                    1
                ),
                
                (
                    "Porcentajes y Geometria Basica",
                    "matematicas",
                    "intermedio",
                    "geometria",
                    """
=== DESCUBRE LOS PORCENTAJES ===

¿QUE ES UN PORCENTAJE?
Un porcentaje es una fraccion de 100.
El simbolo es: %

50% = 50 de cada 100 = 50/100 = 1/2


--- PORCENTAJES COMUNES ---

100% = Todo completo
50% = La mitad
25% = Un cuarto
75% = Tres cuartos
10% = Una decima parte
0% = Nada


--- CALCULAR PORCENTAJES ---

Para calcular el 25% de 80:

Metodo 1: Division
25% = 1/4
80 ÷ 4 = 20

Metodo 2: Multiplicacion
25% = 0.25
80 × 0.25 = 20


=== GEOMETRIA BASICA ===

--- FIGURAS PLANAS ---

RECTANGULO:
- 4 lados
- Lados opuestos iguales
- 4 angulos rectos (90°)

PERIMETRO = suma de todos los lados
AREA = base × altura

Ejemplo:
Base = 6 cm, Altura = 4 cm
Perimetro = 6 + 4 + 6 + 4 = 20 cm
Area = 6 × 4 = 24 cm²


CUADRADO:
- 4 lados IGUALES
- 4 angulos rectos

PERIMETRO = lado × 4
AREA = lado × lado = lado²

Ejemplo:
Lado = 5 cm
Perimetro = 5 × 4 = 20 cm
Area = 5 × 5 = 25 cm²


TRIANGULO:
- 3 lados
- 3 angulos

PERIMETRO = suma de los 3 lados
AREA = (base × altura) ÷ 2

Ejemplo:
Base = 8 cm, Altura = 5 cm
Area = (8 × 5) ÷ 2 = 40 ÷ 2 = 20 cm²


CIRCULO:
- Redondo
- Sin esquinas

RADIO = centro al borde
DIAMETRO = de borde a borde (radio × 2)


RECUERDA:
* Porcentaje = partes de 100
* Area = espacio dentro de la figura
* Perimetro = borde alrededor de la figura
                    """,
                    """
=== PRACTICA DE PORCENTAJES ===

CALCULOS BASICOS:
----------------
1) ¿Cuanto es el 50% de 120?
   
   50% = mitad
   120 ÷ 2 = 60


2) ¿Cuanto es el 25% de 60?
   
   25% = 1/4
   60 ÷ 4 = 15


3) ¿Cuanto es el 10% de 90?
   
   10% = divide entre 10
   90 ÷ 10 = 9


PROBLEMAS REALES:
----------------
4) Una camisa cuesta 40 dolares.
   Tiene 25% de descuento.
   ¿Cuanto descuentan?
   
   25% de 40 = 40 ÷ 4 = 10 dolares
   Precio final: 40 - 10 = 30 dolares


=== PRACTICA DE GEOMETRIA ===

RECTANGULOS:
-----------
5) Rectangulo: base 9 cm, altura 6 cm
   
   Perimetro = 9+6+9+6 = 30 cm
   Area = 9 × 6 = 54 cm²


CUADRADOS:
---------
6) Cuadrado de lado 7 cm
   
   Perimetro = 7 × 4 = 28 cm
   Area = 7 × 7 = 49 cm²


TRIANGULOS:
----------
7) Triangulo: base 10 cm, altura 8 cm
   
   Area = (10 × 8) ÷ 2 = 80 ÷ 2 = 40 cm²


PROBLEMAS MIXTOS:
----------------
8) Un jardin rectangular mide 12m × 8m
   ¿Cuanta cerca necesitas?
   
   Perimetro = 12+8+12+8 = 40 metros


9) Una pizza circular tiene 30cm de diametro.
   ¿Cual es el radio?
   
   Radio = diametro ÷ 2 = 30 ÷ 2 = 15 cm
                    """,
                    """
=== TRUCOS Y CONSEJOS ===

TRUCOS DE PORCENTAJES:
---------------------
TRUCO 1: El 10% es facil
Divide entre 10
10% de 350 = 35

TRUCO 2: Para 5%
Calcula 10% y dividelo entre 2
5% de 60 = 10% es 6, entonces 6÷2 = 3

TRUCO 3: Para 25%
Divide entre 4
25% de 80 = 80÷4 = 20

TRUCO 4: Para 50%
Divide entre 2 (la mitad)
50% de 140 = 70


TRUCOS DE GEOMETRIA:
-------------------
TRUCO 1: Rectangulo
Si conoces area y un lado:
Area = 48, base = 8
Altura = 48 ÷ 8 = 6

TRUCO 2: Cuadrado
Si conoces el area:
Area = 36
Lado = 6 (porque 6 × 6 = 36)

TRUCO 3: Triangulo
Es la mitad del rectangulo
Base 6, altura 4:
Rectangulo seria 6 × 4 = 24
Triangulo = 24 ÷ 2 = 12


FORMULAS PARA RECORDAR:
----------------------
Rectangulo:
* Perimetro = 2×(base + altura)
* Area = base × altura

Cuadrado:
* Perimetro = lado × 4
* Area = lado²

Triangulo:
* Area = (base × altura) ÷ 2


EN LA VIDA REAL:
---------------
PORCENTAJES:
* Descuentos en tiendas
* Calificaciones en la escuela
* Bateria del telefono
* Probabilidad en juegos

GEOMETRIA:
* Medir habitaciones
* Calcular pintura necesaria
* Diseñar jardines
* Construir maquetas

Practica midiendo cosas en tu casa!
                    """,
                    25,
                    2
                ),
                
                # MATEMATICAS - AVANZADO
                (
                    "Algebra: Resolviendo Ecuaciones",
                    "matematicas",
                    "avanzado",
                    "algebra",
                    """
=== BIENVENIDO AL ALGEBRA ===

¿QUE ES EL ALGEBRA?
El algebra usa letras (x, y, z) para representar numeros desconocidos.

Es como un acertijo matematico:
"Pienso un numero, le sumo 5 y obtengo 12. ¿Que numero pense?"

En algebra: x + 5 = 12


--- CONCEPTOS BASICOS ---

VARIABLE: Letra que representa un numero desconocido
Ejemplos: x, y, n

ECUACION: Igualdad con una variable
Ejemplos: x + 3 = 10, 2y = 14

DESPEJAR: Encontrar el valor de la variable


--- RESOLVER ECUACIONES SIMPLES ---

Regla de Oro: Lo que hagas a un lado, hazlo al otro

Ejemplo 1: x + 7 = 15

Paso 1: Queremos x sola
Paso 2: Restamos 7 de ambos lados
        x + 7 - 7 = 15 - 7
Paso 3: x = 8

Verificar: 8 + 7 = 15 ✓


Ejemplo 2: 3x = 21

Paso 1: Queremos x sola
Paso 2: Dividimos ambos lados entre 3
        3x ÷ 3 = 21 ÷ 3
Paso 3: x = 7

Verificar: 3 × 7 = 21 ✓


--- ECUACIONES CON DOS PASOS ---

Ejemplo: 2x + 6 = 16

Paso 1: Quitar el 6 (restar 6)
        2x + 6 - 6 = 16 - 6
        2x = 10

Paso 2: Quitar el 2 (dividir entre 2)
        2x ÷ 2 = 10 ÷ 2
        x = 5

Verificar: 2(5) + 6 = 10 + 6 = 16 ✓


--- POTENCIAS Y RAICES ---

POTENCIAS:
x² = x × x (x al cuadrado)
x³ = x × x × x (x al cubo)

Ejemplos:
5² = 5 × 5 = 25
3³ = 3 × 3 × 3 = 27


RAICES:
√ = raiz cuadrada (numero que multiplicado por si mismo da el resultado)

Ejemplos:
√16 = 4 (porque 4 × 4 = 16)
√25 = 5 (porque 5 × 5 = 25)
√64 = 8 (porque 8 × 8 = 64)


RECUERDA:
* La variable es un numero desconocido
* Despeja paso a paso
* Verifica tu respuesta siempre
* Lo mismo a ambos lados de la ecuacion
                    """,
                    """
=== PRACTICA DE ALGEBRA ===

ECUACIONES SIMPLES:
------------------
1) x + 12 = 20
   
   Restar 12:
   x = 20 - 12
   x = 8


2) 5x = 45
   
   Dividir entre 5:
   x = 45 ÷ 5
   x = 9


3) x - 8 = 15
   
   Sumar 8:
   x = 15 + 8
   x = 23


ECUACIONES DE DOS PASOS:
-----------------------
4) 3x + 4 = 19
   
   Paso 1: Restar 4
   3x = 19 - 4
   3x = 15
   
   Paso 2: Dividir entre 3
   x = 15 ÷ 3
   x = 5


5) 4x - 7 = 21
   
   Paso 1: Sumar 7
   4x = 21 + 7
   4x = 28
   
   Paso 2: Dividir entre 4
   x = 28 ÷ 4
   x = 7


POTENCIAS:
---------
6) Calcula 6²
   
   6 × 6 = 36


7) Calcula 4³
   
   4 × 4 × 4 = 64


RAICES:
------
8) √36 = ?
   
   ¿Que numero × si mismo da 36?
   6 × 6 = 36
   Respuesta: 6


9) √81 = ?
   
   9 × 9 = 81
   Respuesta: 9


PROBLEMAS DEL MUNDO REAL:
-------------------------
10) Tienes x pesos. Gastas 25 y te quedan 40.
    ¿Cuanto tenias?
    
    x - 25 = 40
    x = 40 + 25
    x = 65 pesos


11) Compras 3 libros iguales por 45 dolares.
    ¿Cuanto cuesta cada libro?
    
    3x = 45
    x = 45 ÷ 3
    x = 15 dolares
                    """,
                    """
=== TRUCOS DE ALGEBRA ===

ESTRATEGIAS PARA RESOLVER:
-------------------------
PASO 1: Identifica la variable
¿Que letra hay? (x, y, n)

PASO 2: Decide que hacer primero
Si tiene + o -, hazlo primero
Si tiene × o ÷, hazlo despues

PASO 3: Operacion inversa
+ se quita con -
- se quita con +
× se quita con ÷
÷ se quita con ×

PASO 4: Verifica SIEMPRE
Sustituye tu respuesta en la ecuacion original


TRUCOS RAPIDOS:
--------------
TRUCO 1: Ecuaciones con x+
Resta el numero del otro lado
x + 8 = 15 → x = 15 - 8

TRUCO 2: Ecuaciones con x-
Suma el numero del otro lado
x - 6 = 10 → x = 10 + 6

TRUCO 3: Ecuaciones con 2x, 3x
Divide el otro lado
5x = 30 → x = 30 ÷ 5

TRUCO 4: Raices cuadradas comunes
Memoriza:
√1=1, √4=2, √9=3, √16=4
√25=5, √36=6, √49=7, √64=8


ERRORES COMUNES A EVITAR:
------------------------
ERROR 1: No hacer lo mismo en ambos lados
x + 5 = 10
❌ x = 10 (olvidaste restar 5)
✓ x = 10 - 5 = 5

ERROR 2: Confundir signos
x - 3 = 7
❌ x = 7 - 3 = 4
✓ x = 7 + 3 = 10

ERROR 3: No verificar
Siempre sustituye para verificar


POTENCIAS Y RAICES:
------------------
Potencias pequeñas para memorizar:
2² = 4,  3² = 9,  4² = 16,  5² = 25
6² = 36, 7² = 49, 8² = 64,  9² = 81, 10² = 100

Usa estas para calcular raices rapido!


APLICACIONES REALES:
-------------------
* Calcular edades
* Problemas de compras
* Repartir cantidades
* Calcular tiempos
* Resolver acertijos
* Programacion de computadoras

El algebra esta en todas partes!
                    """,
                    30,
                    1
                ),
                
                (
                    "El Verbo TO BE (Ser/Estar)",
                    "ingles",
                    "intermedio",
                    "gramatica",
                    """
EL VERBO TO BE - SER O ESTAR

1. FORMAS DEL VERBO TO BE
   Presente Simple:
   • I am = yo soy/estoy
   • You are = tú eres/estás
   • He/She/It is = él/ella es/está
   • We are = nosotros somos/estamos
   • They are = ellos/ellas son/están

2. FORMA CORTA (contracciones)
   • I'm = I am
   • You're = You are
   • He's/She's/It's = He/She/It is
   • We're = We are
   • They're = They are

3. FORMA NEGATIVA
   • I am not = I'm not
   • You are not = You aren't
   • He is not = He isn't
   • We are not = We aren't
   • They are not = They aren't

4. PREGUNTAS
   • Am I...?
   • Are you...?
   • Is he/she/it...?
   • Are we...?
   • Are they...?

USOS:
- Identidad: I am Juan
- Profesión: She is a teacher
- Estado: They are happy
- Ubicación: We are at home
                    """,
                    """
EJEMPLOS PRÁCTICOS:

AFIRMACIONES:
1) I am a student
   = Soy un estudiante

2) She is happy
   = Ella está feliz

3) We are friends
   = Somos amigos

NEGACIONES:
1) I am not tired
   = No estoy cansado

2) He is not at home
   = Él no está en casa

PREGUNTAS:
1) Are you ready?
   = ¿Estás listo?

2) Is she your sister?
   = ¿Es ella tu hermana?

3) Are they students?
   = ¿Son ellos estudiantes?
                    """,
                    """
REGLAS IMPORTANTES:
• Con "I" siempre usa "AM"
• Con "You/We/They" usa "ARE"
• Con "He/She/It" usa "IS"
• Singular = IS, Plural = ARE
• En preguntas, invierte el orden
  (You are → Are you?)

ERRORES COMUNES A EVITAR:
× I is a student (INCORRECTO)
✓ I am a student (CORRECTO)

× She are happy (INCORRECTO)
✓ She is happy (CORRECTO)
                    """,
                    15,
                    2
                ),
                
                # PROGRAMACIÓN - BÁSICO
                (
                    "Introducción a Python",
                    "programacion",
                    "basico",
                    "conceptos",
                    """
BIENVENIDO A PYTHON

1. ¿QUÉ ES PYTHON?
   - Lenguaje de programación
   - Fácil de aprender
   - Muy poderoso
   - Usado en: web, IA, juegos, ciencia

2. TU PRIMER PROGRAMA
   print("Hola Mundo")
   
   • print() = mostrar en pantalla
   • Texto entre comillas
   • Punto y coma NO necesario

3. VARIABLES
   ¿Qué son?
   - Cajas que guardan información
   - Tienen un nombre
   - Pueden cambiar de valor
   
   Ejemplos:
   nombre = "Juan"
   edad = 15
   altura = 1.75
   
   Declaración:
   nombre_variable = valor

4. TIPOS DE DATOS BÁSICOS
   
   • String (str) - Texto/Cadena:
     - "Hola", 'Python'
     - Se escribe entre comillas (' ' o " ")
     - Ejemplo: nombre = "Ana"
   
   • Integer (int) - Número Entero:
     - 5, 100, -3, 42
     - Sin punto decimal
     - Ejemplo: edad = 15
   
   • Float - Número Decimal:
     - 3.14, 2.5, 9.99
     - Con punto decimal
     - Ejemplo: precio = 19.99
   
   • Boolean (bool) - Lógico/Booleano:
     - True o False
     - Valores de verdad
     - Ejemplo: activo = True

5. COMENTARIOS EN PYTHON
   
   Los comentarios son NOTAS para humanos.
   Python los IGNORA al ejecutar.
   
   Símbolo: #
   
   Ejemplos:
   # Esto es un comentario
   edad = 15  # comentario al lado del código
   # Python ignora esta línea completa
   
   ¿Para qué sirven?
   - Explicar qué hace el código
   - Dejar notas para después
   - Desactivar código temporalmente
   
6. OPERADORES MATEMÁTICOS
   
   • + (suma/más): 5 + 3 = 8
   • - (resta/menos): 10 - 4 = 6
   • * (multiplicación): 3 * 4 = 12
   • / (división): 10 / 2 = 5.0
   
   Ejemplos:
   a = 10
   b = 5
   suma = a + b  # 15

7. FUNCIONES BÁSICAS
   
   • print() - Muestra/imprime texto
     print("Hola")
   
   • len() - Da la longitud/tamaño
     len("Hola") → 4
     len([1,2,3]) → 3
   
   • int() - Convierte a entero
     int("5") → 5
     int(3.9) → 3
   
   • input() - Lee entrada del usuario
     nombre = input("Tu nombre: ")
                    """,
                    """
EJEMPLOS DE CÓDIGO:

1) IMPRIMIR TEXTO CON print()
   print("Hola")
   print("Me llamo Python")
   # Salida:
   # Hola
   # Me llamo Python

2) VARIABLES Y TIPOS DE DATOS
   # String (cadena de texto)
   nombre = "Ana"
   apellido = 'García'  # comillas simples también
   
   # Integer (entero)
   edad = 12
   puntos = 100
   
   # Float (decimal)
   altura = 1.65
   precio = 19.99
   
   # Boolean (booleano/lógico)
   activo = True
   tiene_permiso = False

3) USO DE COMENTARIOS
   # Este programa calcula el área
   base = 10  # ancho del rectángulo
   altura = 5  # alto del rectángulo
   area = base * altura  # fórmula: b × h
   print("Área:", area)  # muestra resultado

4) OPERADORES MATEMÁTICOS
   a = 10
   b = 5
   
   suma = a + b        # 15
   resta = a - b       # 5
   mult = a * b        # 50
   div = a / b         # 2.0
   
   print("Suma:", suma)
   print("Resta:", resta)

5) FUNCIÓN len() PARA LONGITUD
   texto = "Hola"
   largo = len(texto)
   print(largo)  # 4
   
   lista = [1, 2, 3, 4, 5]
   cantidad = len(lista)
   print(cantidad)  # 5

6) FUNCIÓN int() PARA CONVERTIR
   # De string a entero
   numero_texto = "42"
   numero = int(numero_texto)
   print(numero + 10)  # 52
   
   # De float a entero
   decimal = 3.9
   entero = int(decimal)
   print(entero)  # 3

7) ENTRADA Y SALIDA
   nombre = input("¿Cómo te llamas? ")
   print("Hola", nombre)
   # El usuario escribe su nombre
   # Python lo saluda

8) STRING ENTRE COMILLAS
   # Puedes usar ' ' o " "
   mensaje1 = "Hola Mundo"
   mensaje2 = 'Hola Mundo'
   ambos_iguales = True
                    """,
                    """
CONSEJOS PARA PRINCIPIANTES:

1. REGLAS DE NOMBRES DE VARIABLES:
   ✓ edad, mi_nombre, numero1
   × 1numero, mi-nombre, mi nombre
   - Solo letras, números y _
   - No empezar con número
   - No usar espacios

2. INDENTACIÓN IMPORTA
   Python usa espacios al inicio
   4 espacios o 1 TAB

3. ERRORES COMUNES:
   × Print("hola")  # P mayúscula
   ✓ print("hola")  # p minúscula
   
   × print "hola"   # sin paréntesis
   ✓ print("hola")  # con paréntesis

4. PRACTICA:
   • Escribe código todos los días
   • Experimenta cambiando valores
   • No tengas miedo a errores
   • Los errores enseñan!

5. RECURSOS:
   • Python.org (documentación oficial)
   • Practica en línea
   • Únete a comunidades
                    """,
                    20,
                    1
                ),
                
                (
                    "Estructuras de Control en Python",
                    "programacion",
                    "intermedio",
                    "estructuras",
                    """
ESTRUCTURAS DE CONTROL

1. CONDICIONALES (IF/ELSE)
   Tomar decisiones en el código
   
   Sintaxis:
   if condicion:
       # código si es verdadero
   else:
       # código si es falso

   Ejemplo:
   edad = 18
   if edad >= 18:
       print("Eres adulto")
   else:
       print("Eres menor")

2. CONDICIONAL MÚLTIPLE (ELIF)
   if condicion1:
       # código 1
   elif condicion2:
       # código 2
   else:
       # código 3

3. BUCLE FOR
   Repetir código un número de veces
   
   for i in range(5):
       print(i)
   # Imprime: 0, 1, 2, 3, 4

4. BUCLE WHILE
   Repetir mientras sea verdadero
   
   contador = 0
   while contador < 5:
       print(contador)
       contador = contador + 1

5. OPERADORES DE COMPARACIÓN
   • == igual a
   • != diferente de
   • > mayor que
   • < menor que
   • >= mayor o igual
   • <= menor o igual
                    """,
                    """
EJEMPLOS COMPLETOS:

1) IF/ELSE CON NÚMEROS
   numero = 10
   if numero > 0:
       print("Positivo")
   elif numero < 0:
       print("Negativo")
   else:
       print("Cero")

2) FOR CON LISTA
   frutas = ["manzana", "pera", "uva"]
   for fruta in frutas:
       print("Me gusta la", fruta)

3) WHILE CON CONTADOR
   cuenta = 1
   while cuenta <= 5:
       print("Cuenta:", cuenta)
       cuenta = cuenta + 1

4) IF ANIDADO
   edad = 20
   tiene_licencia = True
   
   if edad >= 18:
       if tiene_licencia:
           print("Puedes conducir")
       else:
           print("Necesitas licencia")
   else:
       print("Eres muy joven")

5) FOR CON RANGE
   # Tabla del 5
   for i in range(1, 11):
       print(f"5 × {i} = {5*i}")
                    """,
                    """
TIPS IMPORTANTES:

1. INDENTACIÓN:
   - Usa 4 espacios después de :
   - Mantén consistencia
   - Python es estricto con espacios

2. EVITAR BUCLES INFINITOS:
   # MAL - nunca termina
   while True:
       print("Ayuda!")
   
   # BIEN - tiene condición de salida
   contador = 0
   while contador < 10:
       print(contador)
       contador += 1

3. OPTIMIZACIÓN:
   # Usa range() para números
   # Usa enumerate() para índices
   # Evita modificar listas en bucles

4. OPERADORES LÓGICOS:
   • and = Y (ambos verdaderos)
   • or = O (al menos uno verdadero)
   • not = NO (invierte)
   
   if edad >= 18 and tiene_licencia:
       print("OK")

5. BREAK Y CONTINUE:
   • break = salir del bucle
   • continue = saltar iteración
   
   for i in range(10):
       if i == 5:
           break  # sale en 5
       print(i)
                    """,
                    25,
                    2
                ),
                
                # INGLÉS - AVANZADO
                (
                    "Tiempos Verbales en Ingles",
                    "ingles",
                    "avanzado",
                    "gramatica",
                    """
=== DOMINA LOS TIEMPOS VERBALES ===

Los tiempos verbales nos dicen CUANDO pasa algo:
* Pasado = ya paso
* Presente = esta pasando ahora
* Futuro = pasara despues


--- PRESENTE SIMPLE ---

USO: Cosas que pasan siempre o regularmente

ESTRUCTURA:
I/You/We/They + verbo
He/She/It + verbo + S

Ejemplos:
* I play soccer (Yo juego futbol)
* She plays piano (Ella toca piano)
* They eat apples (Ellos comen manzanas)

PALABRAS CLAVE:
always, usually, often, sometimes, never
every day/week/month


--- PRESENTE CONTINUO ---

USO: Cosas que pasan AHORA

ESTRUCTURA:
Sujeto + AM/IS/ARE + verbo + ING

Ejemplos:
* I am studying (Estoy estudiando)
* He is running (El esta corriendo)
* They are playing (Ellos estan jugando)

PALABRAS CLAVE:
now, right now, at the moment


--- PASADO SIMPLE ---

USO: Cosas que ya pasaron

ESTRUCTURA:
Sujeto + verbo en pasado

Verbos regulares: agregar ED
* play → played
* walk → walked
* watch → watched

Verbos irregulares (memorizar):
* go → went
* eat → ate
* see → saw
* have → had
* do → did

Ejemplos:
* I played soccer yesterday
* She went to school
* They ate pizza last night

PALABRAS CLAVE:
yesterday, last week/month/year, ago


--- FUTURO CON WILL ---

USO: Cosas que pasaran

ESTRUCTURA:
Sujeto + WILL + verbo

Ejemplos:
* I will study (Yo estudiare)
* She will go (Ella ira)
* They will play (Ellos jugaran)

PALABRAS CLAVE:
tomorrow, next week/month/year


--- PREGUNTAS Y NEGACIONES ---

PRESENTE SIMPLE:
Pregunta: Do/Does + sujeto + verbo?
* Do you like pizza?
* Does she play tennis?

Negativo: Don't/Doesn't + verbo
* I don't like broccoli
* He doesn't play guitar


PASADO SIMPLE:
Pregunta: Did + sujeto + verbo?
* Did you go to school?

Negativo: Didn't + verbo
* I didn't see the movie


RECUERDA:
* Cada tiempo tiene su estructura
* Las palabras clave te ayudan a identificar el tiempo
* Practica con verbos comunes primero
                    """,
                    """
=== PRACTICA DE TIEMPOS VERBALES ===

PRESENTE SIMPLE:
---------------
1) I _____ (play) videogames
   
   Respuesta: I play videogames


2) She _____ (watch) TV
   
   He/She/It = agregar S
   Respuesta: She watches TV


3) They _____ (go) to school
   
   Respuesta: They go to school


PRESENTE CONTINUO:
-----------------
4) I _____ (read) a book now
   
   AM + verbo + ING
   Respuesta: I am reading a book


5) He _____ (play) soccer right now
   
   IS + verbo + ING
   Respuesta: He is playing soccer


PASADO SIMPLE:
-------------
6) I _____ (walk) to school yesterday
   
   Verbo regular + ED
   Respuesta: I walked to school


7) She _____ (go) to the park last week
   
   Verbo irregular: go → went
   Respuesta: She went to the park


8) They _____ (eat) pizza last night
   
   Verbo irregular: eat → ate
   Respuesta: They ate pizza


FUTURO:
-------
9) I _____ (visit) my grandma tomorrow
   
   WILL + verbo
   Respuesta: I will visit my grandma


10) They _____ (play) basketball next week
    
    Respuesta: They will play basketball


PREGUNTAS:
---------
11) _____ you like chocolate? (presente)
    
    Respuesta: Do you like chocolate?


12) _____ she go to the party? (pasado)
    
    Respuesta: Did she go to the party?


NEGACIONES:
----------
13) I _____ like vegetables (presente)
    
    Respuesta: I don't like vegetables


14) He _____ play yesterday (pasado)
    
    Respuesta: He didn't play yesterday
                    """,
                    """
=== TRUCOS PARA LOS TIEMPOS ===

IDENTIFICAR EL TIEMPO:
---------------------
Busca las palabras clave:

PRESENTE:
* always, usually, often
* every day/week
* → Presente Simple

AHORA:
* now, right now
* at the moment
* → Presente Continuo

PASADO:
* yesterday, last...
* ago (hace...)
* → Pasado Simple

FUTURO:
* tomorrow, next...
* in the future
* → Futuro (will)


TRUCOS DE PRESENTE SIMPLE:
-------------------------
TRUCO 1: Tercera persona
He/She/It siempre lleva S
* He playS
* She watchES
* It goES

TRUCO 2: Verbos que terminan en consonante+Y
Cambiar Y por IES
* study → studies
* try → tries


TRUCOS DE PASADO:
----------------
TRUCO 1: Verbos regulares
Solo agregar ED
* play → played
* walk → walked

TRUCO 2: Memoriza irregulares comunes
* go → went
* have → had
* see → saw
* do → did
* make → made
* get → got
* come → came
* take → took


TRUCOS DE PREGUNTAS:
-------------------
TRUCO 1: Presente Simple
Do/Does al inicio
* Do you...?
* Does he...?

TRUCO 2: Pasado Simple
Did para todos
* Did you...?
* Did she...?
* Did they...?

TRUCO 3: Futuro
Will al inicio
* Will you...?
* Will they...?


PRACTICA DIARIA:
---------------
* Describe tu dia en presente simple
* Di que estas haciendo ahora (presente continuo)
* Cuenta que hiciste ayer (pasado)
* Planea que haras mañana (futuro)


CANCIONES Y PELICULAS:
---------------------
* Escucha canciones en ingles
* Identifica los tiempos verbales
* Ve peliculas con subtitulos
* Repite frases que escuches

La practica hace al maestro!
                    """,
                    25,
                    1
                ),
                
                # PROGRAMACIÓN - AVANZADO
                (
                    "Listas y Diccionarios en Python",
                    "programacion",
                    "avanzado",
                    "estructuras_datos",
                    """
=== ESTRUCTURAS DE DATOS EN PYTHON ===

Las estructuras de datos son formas de organizar y guardar informacion.


--- LISTAS ---

Una LISTA guarda varios elementos en orden.
Se usan corchetes []

Crear una lista:
frutas = ["manzana", "platano", "naranja"]
numeros = [10, 20, 30, 40, 50]


ACCEDER A ELEMENTOS:
Los indices empiezan en 0

frutas[0] → "manzana" (primero)
frutas[1] → "platano" (segundo)
frutas[2] → "naranja" (tercero)


MODIFICAR LISTAS:

Agregar al final:
frutas.append("uva")

Agregar en posicion:
frutas.insert(1, "fresa")  # posicion 1

Eliminar:
frutas.remove("platano")  # por valor
frutas.pop(0)  # por indice

Tamaño de lista:
len(frutas)  # cuantos elementos hay


RECORRER UNA LISTA:

for fruta in frutas:
    print(fruta)


--- DICCIONARIOS ---

Un DICCIONARIO guarda pares clave:valor
Se usan llaves {}

Crear diccionario:
estudiante = {
    "nombre": "Ana",
    "edad": 12,
    "grado": 6
}


ACCEDER A VALORES:
estudiante["nombre"] → "Ana"
estudiante["edad"] → 12


AGREGAR O MODIFICAR:
estudiante["escuela"] = "Primaria Central"
estudiante["edad"] = 13  # modificar


ELIMINAR:
del estudiante["grado"]


RECORRER DICCIONARIO:

# Solo claves
for clave in estudiante:
    print(clave)

# Claves y valores
for clave, valor in estudiante.items():
    print(clave, ":", valor)


--- DIFERENCIAS CLAVE ---

LISTA:
* Usa numeros (indices)
* Orden importa
* Permite duplicados
* Ejemplo: [1, 2, 3, 2]

DICCIONARIO:
* Usa claves (strings u otros)
* Orden no importa
* Claves unicas
* Ejemplo: {"nombre": "Juan", "edad": 10}


CUANDO USAR CADA UNO:

Usa LISTA cuando:
* Tienes coleccion de elementos similares
* El orden importa
* Ejemplo: lista de calificaciones

Usa DICCIONARIO cuando:
* Tienes propiedades con nombres
* Quieres buscar por clave
* Ejemplo: informacion de persona


RECUERDA:
* Listas = [] (orden, indices numericos)
* Diccionarios = {} (claves con nombres)
* Ambos son muy utiles en programacion
                    """,
                    """
=== PRACTICA CON LISTAS ===

CREAR Y ACCEDER:
---------------
1) Crear lista de colores
   
   colores = ["rojo", "azul", "verde"]


2) Obtener primer color
   
   colores[0] → "rojo"


3) Obtener ultimo color
   
   colores[2] → "verde"
   # O tambien: colores[-1]


MODIFICAR LISTAS:
----------------
4) Agregar "amarillo" al final
   
   colores.append("amarillo")
   # colores = ["rojo", "azul", "verde", "amarillo"]


5) Insertar "morado" en posicion 1
   
   colores.insert(1, "morado")
   # colores = ["rojo", "morado", "azul", "verde"]


6) Eliminar "azul"
   
   colores.remove("azul")


OPERACIONES:
-----------
7) ¿Cuantos colores hay?
   
   len(colores) → devuelve cantidad


8) Imprimir todos los colores
   
   for color in colores:
       print(color)


=== PRACTICA CON DICCIONARIOS ===

CREAR Y ACCEDER:
---------------
9) Crear diccionario de mascota
   
   mascota = {
       "nombre": "Max",
       "tipo": "perro",
       "edad": 3
   }


10) Obtener nombre de mascota
    
    mascota["nombre"] → "Max"


MODIFICAR DICCIONARIOS:
----------------------
11) Cambiar edad a 4
    
    mascota["edad"] = 4


12) Agregar color
    
    mascota["color"] = "cafe"


13) Eliminar tipo
    
    del mascota["tipo"]


PROBLEMAS REALES:
----------------
14) Lista de calificaciones
    
    calificaciones = [85, 90, 78, 92, 88]
    
    # Calcular promedio
    promedio = sum(calificaciones) / len(calificaciones)
    print(promedio)  # 86.6


15) Inventario de tienda
    
    inventario = {
        "manzanas": 50,
        "platanos": 30,
        "naranjas": 40
    }
    
    # Vender 10 manzanas
    inventario["manzanas"] = inventario["manzanas"] - 10
    
    # Agregar nuevo producto
    inventario["uvas"] = 25
                    """,
                    """
=== TRUCOS Y CONSEJOS ===

TRUCOS DE LISTAS:
----------------
TRUCO 1: Ultimo elemento
lista[-1]  # siempre es el ultimo

TRUCO 2: Verificar si existe
if "manzana" in frutas:
    print("Si hay manzanas")

TRUCO 3: Ordenar lista
numeros = [3, 1, 4, 2]
numeros.sort()  # [1, 2, 3, 4]

TRUCO 4: Lista de rango
numeros = list(range(1, 6))  # [1, 2, 3, 4, 5]

TRUCO 5: Juntar listas
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
completa = lista1 + lista2  # [1,2,3,4,5,6]


TRUCOS DE DICCIONARIOS:
----------------------
TRUCO 1: Verificar clave existe
if "nombre" in estudiante:
    print(estudiante["nombre"])

TRUCO 2: Obtener con valor por defecto
estudiante.get("telefono", "No tiene")
# Si no existe "telefono", devuelve "No tiene"

TRUCO 3: Todas las claves
claves = estudiante.keys()

TRUCO 4: Todos los valores
valores = estudiante.values()

TRUCO 5: Copiar diccionario
copia = estudiante.copy()


ERRORES COMUNES:
---------------
ERROR 1: Indice fuera de rango
lista = [1, 2, 3]
# lista[5] ❌ ERROR (solo hay 0,1,2)

ERROR 2: Clave no existe
# diccionario["algo"] ❌ si no existe
✓ Usa .get("algo") en su lugar

ERROR 3: Olvidar que indices empiezan en 0
lista[0]  # primer elemento
lista[1]  # segundo elemento


PATRONES UTILES:
---------------
PATRON 1: Contar elementos
contador = {}
for fruta in frutas:
    if fruta in contador:
        contador[fruta] += 1
    else:
        contador[fruta] = 1


PATRON 2: Lista a diccionario
nombres = ["Ana", "Juan", "Maria"]
edades = [10, 12, 11]

personas = {}
for i in range(len(nombres)):
    personas[nombres[i]] = edades[i]


APLICACIONES REALES:
-------------------
LISTAS:
* Lista de tareas
* Calificaciones de estudiantes
* Inventario de productos
* Historial de acciones

DICCIONARIOS:
* Informacion de usuarios
* Configuracion de app
* Traducciones (español → ingles)
* Base de datos simple


PRACTICA:
--------
* Crea una lista de tus peliculas favoritas
* Haz un diccionario con informacion tuya
* Combina listas y diccionarios
* Experimenta con los metodos

La practica es clave para dominarlas!
                    """,
                    30,
                    1
                ),
                
                (
                    "Manejo de Errores en Python",
                    "programacion",
                    "avanzado",
                    "errores",
                    """
=== APRENDE A MANEJAR ERRORES ===

Los ERRORES son problemas que ocurren cuando el programa se ejecuta.
Aprender a manejarlos es importante!


--- TIPOS COMUNES DE ERRORES ---

SYNTAX ERROR (Error de Sintaxis):
Escribiste algo mal
print("Hola"  # ❌ Falta cerrar parentesis


RUNTIME ERROR (Error en Ejecucion):
El programa corre pero algo falla

TypeError:
numero = "5" + 3  # ❌ No puedes sumar texto y numero

ValueError:
numero = int("abc")  # ❌ "abc" no es un numero

ZeroDivisionError:
resultado = 10 / 0  # ❌ No se puede dividir entre 0

IndexError:
lista = [1, 2, 3]
elemento = lista[10]  # ❌ No existe posicion 10


--- MANEJO DE ERRORES CON TRY-EXCEPT ---

Estructura basica:

try:
    # Codigo que puede fallar
    numero = int(input("Escribe un numero: "))
except:
    # Que hacer si falla
    print("Eso no es un numero!")


Ejemplo completo:

try:
    edad = int(input("Tu edad: "))
    print("Tienes", edad, "años")
except ValueError:
    print("Por favor escribe solo numeros")


--- CAPTURAR MULTIPLES ERRORES ---

try:
    numeros = [1, 2, 3]
    indice = int(input("Posicion: "))
    print(numeros[indice])
except ValueError:
    print("Debes escribir un numero")
except IndexError:
    print("Esa posicion no existe")


--- BLOQUE ELSE ---

Se ejecuta si NO hubo error:

try:
    numero = int(input("Numero: "))
except ValueError:
    print("Error: no es numero")
else:
    print("Correcto! El numero es", numero)


--- BLOQUE FINALLY ---

Se ejecuta SIEMPRE (haya error o no):

try:
    archivo = open("datos.txt")
    # hacer algo con archivo
except FileNotFoundError:
    print("Archivo no encontrado")
finally:
    print("Programa terminado")


--- CREAR TUS PROPIOS ERRORES ---

Usa RAISE para crear errores:

edad = int(input("Tu edad: "))

if edad < 0:
    raise ValueError("La edad no puede ser negativa")

if edad > 150:
    raise ValueError("Edad no valida")


--- BUENAS PRACTICAS ---

1. Ser especifico con los errores
   ✓ except ValueError:
   ❌ except:  # muy general

2. Dar mensajes claros
   ✓ "Error: Debes escribir un numero entero"
   ❌ "Error"

3. No ocultar errores importantes
   Solo captura errores que puedes manejar

4. Usar finally para limpiar recursos
   Cerrar archivos, conexiones, etc.


RECUERDA:
* Los errores son normales en programacion
* Try-except evita que el programa se cierre
* Captura solo los errores que esperas
* Da mensajes utiles al usuario
                    """,
                    """
=== PRACTICA DE MANEJO DE ERRORES ===

EJERCICIO 1: Division Segura
----------------------------
Proteger division entre cero:

try:
    a = 10
    b = 0
    resultado = a / b
except ZeroDivisionError:
    print("No se puede dividir entre cero")
    resultado = None


EJERCICIO 2: Conversion de Numero
---------------------------------
Convertir texto a numero con proteccion:

try:
    texto = "abc123"
    numero = int(texto)
except ValueError:
    print("Error: eso no es un numero valido")
    numero = 0


EJERCICIO 3: Acceso a Lista
---------------------------
Acceder a posicion de lista:

numeros = [10, 20, 30]

try:
    posicion = 5
    elemento = numeros[posicion]
except IndexError:
    print("Esa posicion no existe")
    elemento = None


EJERCICIO 4: Multiples Errores
------------------------------
Calcular promedio con validacion:

try:
    nota1 = int(input("Primera nota: "))
    nota2 = int(input("Segunda nota: "))
    promedio = (nota1 + nota2) / 2
    print("Promedio:", promedio)
except ValueError:
    print("Debes escribir numeros")
except ZeroDivisionError:
    print("Error en calculo")


EJERCICIO 5: Con Else
---------------------
Validar edad con mensaje de exito:

try:
    edad = int(input("Tu edad: "))
except ValueError:
    print("Edad invalida")
else:
    print("Edad registrada:", edad)


EJERCICIO 6: Con Finally
------------------------
Simular abrir y cerrar archivo:

try:
    print("Abriendo archivo...")
    # operacion que puede fallar
    x = 10 / 2
    print("Resultado:", x)
except:
    print("Hubo un error")
finally:
    print("Cerrando archivo...")


EJERCICIO 7: Crear Error Propio
-------------------------------
Validar nota de examen:

nota = int(input("Tu nota (0-100): "))

if nota < 0 or nota > 100:
    raise ValueError("La nota debe estar entre 0 y 100")

print("Nota valida:", nota)


EJERCICIO 8: Programa Completo
------------------------------
Calculadora protegida:

try:
    num1 = float(input("Primer numero: "))
    operacion = input("Operacion (+, -, *, /): ")
    num2 = float(input("Segundo numero: "))
    
    if operacion == "+":
        resultado = num1 + num2
    elif operacion == "-":
        resultado = num1 - num2
    elif operacion == "*":
        resultado = num1 * num2
    elif operacion == "/":
        resultado = num1 / num2
    else:
        raise ValueError("Operacion no valida")
    
    print("Resultado:", resultado)
    
except ValueError as e:
    print("Error:", e)
except ZeroDivisionError:
    print("No puedes dividir entre cero")
except Exception as e:
    print("Error inesperado:", e)
                    """,
                    """
=== TRUCOS DE MANEJO DE ERRORES ===

ESTRATEGIA GENERAL:
------------------
1. Identifica donde puede fallar
2. Envuelve en try-except
3. Captura errores especificos
4. Da mensajes claros
5. Ofrece alternativas


TRUCOS RAPIDOS:
--------------
TRUCO 1: Capturar el mensaje de error
try:
    x = int("abc")
except ValueError as error:
    print("Error:", error)


TRUCO 2: Validar antes de operar
# Evita errores antes de que pasen
if texto.isdigit():
    numero = int(texto)
else:
    print("No es numero")


TRUCO 3: Usar valores por defecto
try:
    edad = int(input("Edad: "))
except ValueError:
    edad = 0  # valor por defecto


TRUCO 4: Ciclo hasta que sea valido
while True:
    try:
        edad = int(input("Tu edad: "))
        break  # Sale si es correcto
    except ValueError:
        print("Intenta de nuevo")


PATRONES UTILES:
---------------
PATRON 1: Validacion de entrada
def obtener_numero():
    while True:
        try:
            return int(input("Numero: "))
        except ValueError:
            print("Debes escribir un numero")


PATRON 2: Operacion segura
def division_segura(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


PATRON 3: Archivo seguro
try:
    with open("archivo.txt") as f:
        contenido = f.read()
except FileNotFoundError:
    contenido = ""


ERRORES COMUNES A EVITAR:
------------------------
ERROR 1: Except muy general
❌ except:  # captura TODO
✓ except ValueError:  # especifico

ERROR 2: Ocultar errores
❌ try:
      codigo
   except:
      pass  # ignora el error!

ERROR 3: No dar informacion
❌ print("Error")
✓ print("Error: Escribe un numero del 1 al 10")


MENSAJES DE ERROR BUENOS:
-------------------------
✓ "Error: Debes escribir un numero entero"
✓ "La edad debe ser entre 1 y 150"
✓ "Archivo no encontrado: datos.txt"
✓ "No puedes dividir entre cero"

❌ "Error"
❌ "Algo salio mal"
❌ "Input invalido"


APLICACIONES REALES:
-------------------
* Formularios de entrada de datos
* Lectura de archivos
* Conexion a internet
* Operaciones matematicas
* Validacion de configuracion
* APIs y servicios externos


DEBUGGING (DEPURACION):
----------------------
Si tu try-except no funciona:

1. Imprime el tipo de error:
   except Exception as e:
       print(type(e), e)

2. Revisa el traceback completo
3. Usa print() para ver valores
4. Prueba paso a paso


RECUERDA:
* Los errores son tus amigos (te dicen que arreglar)
* No tengas miedo de los errores
* Practica creando errores a proposito
* Aprende a leer mensajes de error

Un buen programador sabe manejar errores!
                    """,
                    30,
                    2
                )
            
    ]
