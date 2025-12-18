"""Datos iniciales de ejercicios para PiLearn.

Nota: Esta base puede ampliarse con más ejercicios según el currículo.
"""


def get_ejercicios_iniciales():
    """
    Retorna lista de tuplas con ejercicios iniciales
    """
    return [

                # MATEMÁTICAS - BÁSICO
                ("Cuanto es 127 + 89?", "216", "Suma llevando: 7+9=16 (llevo 1), 2+8+1=11 (llevo 1), 1+0+1=2", "basico", "aritmetica", "matematicas",
                 "Suma de derecha a izquierda", "Recuerda llevar cuando sumas mas de 9", "127 + 89 = 216", 10, 60, ""),
                
                ("Cuanto es 456 - 189?", "267", "Resta prestando: 6-9 (pido prestado) 16-9=7, 4-8 (pido prestado) 14-8=6, 3-1=2", "basico", "aritmetica", "matematicas",
                 "Resta de derecha a izquierda", "Pide prestado cuando el numero de arriba es menor", "456 - 189 = 267", 10, 60, ""),
                
                ("Cuanto es 24 × 13?", "312", "24 × 13 = 24 × 10 + 24 × 3 = 240 + 72 = 312", "basico", "aritmetica", "matematicas",
                 "Multiplica por las unidades y decenas por separado", "24×3=72, 24×10=240", "72 + 240 = 312", 15, 90, ""),
                
                ("Cuanto es 144 ÷ 12?", "12", "144 ÷ 12 = 12 porque 12 × 12 = 144", "basico", "aritmetica", "matematicas",
                 "Piensa: que numero por 12 da 144?", "Usa la tabla del 12", "12 × 12 = 144", 10, 60, ""),
                
                ("Cuanto es 1/2 + 1/4?", "3/4", "1/2 = 2/4, entonces 2/4 + 1/4 = 3/4", "basico", "fracciones", "matematicas",
                 "Necesitas el mismo denominador", "1/2 = 2/4", "2/4 + 1/4 = 3/4", 15, 90, ""),
                
                ("Cuanto es 8 + 7?", "15", "8 + 7 = 15 (suma basica)", "basico", "aritmetica", "matematicas",
                 "Cuenta con tus dedos si es necesario", "8 + 7 = 15", "Suma simple", 10, 30, ""),
                
                ("Cuanto es 15 - 8?", "7", "15 - 8 = 7 (resta basica)", "basico", "aritmetica", "matematicas",
                 "Cuenta hacia atras desde 15", "15 - 8 = 7", "Resta simple", 10, 30, ""),
                
                ("Cuanto es 7 × 8?", "56", "7 × 8 = 56 (tabla del 7)", "basico", "aritmetica", "matematicas",
                 "Repasa la tabla del 7", "7 × 8 = 56", "7×8=56", 10, 45, ""),
                
                ("Cuanto es 36 ÷ 6?", "6", "36 ÷ 6 = 6 (division basica)", "basico", "aritmetica", "matematicas",
                 "Piensa: 6 por que numero da 36?", "6 × 6 = 36", "36 ÷ 6 = 6", 10, 45, ""),
                
                ("Cuanto es 1/3 + 1/3?", "2/3", "1/3 + 1/3 = 2/3 (mismo denominador)", "basico", "fracciones", "matematicas",
                 "Suma los numeradores, mantiene denominador", "1 + 1 = 2, denominador 3", "2/3", 10, 60, ""),
                
                ("Redondea 47 a la decena mas cercana", "50", "47 esta mas cerca de 50 que de 40", "basico", "redondeo", "matematicas",
                 "Si el ultimo digito es 5 o mas, sube", "7 >= 5, entonces sube a 50", "47 → 50", 10, 45, ""),
                
                ("Cuanto es 100 - 37?", "63", "100 - 37 = 63", "basico", "aritmetica", "matematicas",
                 "Resta desde 100", "100 - 30 = 70, 70 - 7 = 63", "63", 10, 60, ""),
                
                ("Cuanto es 9 × 6?", "54", "9 × 6 = 54 (tabla del 9)", "basico", "aritmetica", "matematicas",
                 "Tabla del 9", "9 × 6 = 54", "54", 10, 45, ""),
                
                ("Cuanto es 3/4 - 1/4?", "2/4", "3/4 - 1/4 = 2/4 = 1/2", "basico", "fracciones", "matematicas",
                 "Resta numeradores, mismo denominador", "3 - 1 = 2, denominador 4", "2/4 o 1/2", 10, 60, "1/2|0.5"),
                
                ("Cual es la mitad de 20?", "10", "La mitad de 20 es 10", "basico", "fracciones", "matematicas",
                 "Divide 20 entre 2", "20 ÷ 2 = 10", "10", 10, 30, ""),
                
                # MATEMÁTICAS - INTERMEDIO
                ("Cuanto es 2/3 × 3/4?", "1/2", "Multiplica numeradores: 2×3=6, denominadores: 3×4=12, simplifica: 6/12=1/2", "intermedio", "fracciones", "matematicas",
                 "Multiplica arriba por arriba, abajo por abajo", "2×3=6, 3×4=12", "6/12 se simplifica a 1/2", 15, 90, "2/4|6/12|0.5"),
                
                ("Calcula el 25% de 80", "20", "25% = 1/4, entonces 80÷4 = 20", "intermedio", "porcentajes", "matematicas",
                 "25% es lo mismo que 1/4", "Divide 80 entre 4", "80 × 0.25 = 20", 15, 90, ""),
                
                ("Cual es el area de un rectangulo de 8cm × 5cm?", "40", "Area = base × altura = 8 × 5 = 40 cm²", "intermedio", "geometria", "matematicas",
                 "Formula: base × altura", "Multiplica 8 por 5", "8 × 5 = 40 cm²", 15, 90, "40 cm2|40cm2|40 centimetros cuadrados"),
                
                ("Cuanto es 3² + 4²?", "25", "3² = 9, 4² = 16, entonces 9 + 16 = 25", "intermedio", "algebra", "matematicas",
                 "Calcula cada potencia primero", "3×3=9, 4×4=16", "9 + 16 = 25", 15, 90, ""),
                
                ("Calcula el 50% de 150", "75", "50% = mitad, 150÷2 = 75", "intermedio", "porcentajes", "matematicas",
                 "50% es la mitad", "150 ÷ 2 = 75", "75", 15, 60, ""),
                
                ("Cual es el perimetro de un cuadrado de lado 7cm?", "28", "Perimetro = 4 × lado = 4 × 7 = 28 cm", "intermedio", "geometria", "matematicas",
                 "Suma los 4 lados", "7 + 7 + 7 + 7 = 28", "4 × 7 = 28 cm", 15, 60, "28 cm|28cm"),
                
                ("Cuanto es 5² - 3²?", "16", "5² = 25, 3² = 9, entonces 25 - 9 = 16", "intermedio", "algebra", "matematicas",
                 "Calcula cada potencia", "25 - 9 = 16", "16", 15, 90, ""),
                
                ("Convierte 0.75 a fraccion", "3/4", "0.75 = 75/100 = 3/4 simplificado", "intermedio", "fracciones", "matematicas",
                 "75 centesimos = 3/4", "75/100 simplifica a 3/4", "3/4", 15, 90, ""),
                
                ("Calcula el 10% de 200", "20", "10% de 200 = 200 × 0.1 = 20", "intermedio", "porcentajes", "matematicas",
                 "10% = dividir entre 10", "200 ÷ 10 = 20", "20", 15, 60, ""),
                
                ("Cual es el area de un triangulo base 6 altura 4?", "12", "Area = (base × altura) ÷ 2 = (6 × 4) ÷ 2 = 12", "intermedio", "geometria", "matematicas",
                 "Formula: (b × h) ÷ 2", "6 × 4 = 24, 24 ÷ 2 = 12", "12 cm²", 15, 90, "12 cm2|12cm2"),
                
                ("Cuanto es √16?", "4", "√16 = 4 porque 4 × 4 = 16", "intermedio", "raices", "matematicas",
                 "Que numero al cuadrado da 16?", "4 × 4 = 16", "4", 15, 60, ""),
                
                ("Simplifica: 8/12", "2/3", "8/12 = 2/3 (dividiendo por 4)", "intermedio", "fracciones", "matematicas",
                 "Divide numerador y denominador por su MCD", "8÷4=2, 12÷4=3", "2/3", 15, 90, ""),
                
                ("Cuanto es 2³?", "8", "2³ = 2 × 2 × 2 = 8", "intermedio", "potencias", "matematicas",
                 "2 multiplicado 3 veces", "2 × 2 × 2 = 8", "8", 15, 60, ""),
                
                ("Calcula el 20% de 50", "10", "20% de 50 = 50 × 0.2 = 10", "intermedio", "porcentajes", "matematicas",
                 "20% = 1/5", "50 ÷ 5 = 10", "10", 15, 60, ""),
                
                ("Cual es el perimetro de un rectangulo 6×4?", "20", "Perimetro = 2(6+4) = 2(10) = 20", "intermedio", "geometria", "matematicas",
                 "Suma todos los lados", "6+4+6+4=20", "20 cm", 15, 60, "20 cm|20cm"),
                
                # MATEMÁTICAS - AVANZADO
                ("Resuelve: 2x + 5 = 15", "5", "2x = 15 - 5 = 10, entonces x = 10÷2 = 5", "avanzado", "algebra", "matematicas",
                 "Despeja x: pasa el 5 restando", "2x = 10", "x = 10÷2 = 5", 20, 120, "x=5"),
                
                ("Calcula la hipotenusa de un triangulo rectangulo con catetos 3 y 4", "5", "h² = 3² + 4² = 9 + 16 = 25, h = √25 = 5", "avanzado", "geometria", "matematicas",
                 "Usa el teorema de Pitagoras: a² + b² = c²", "3² + 4² = 9 + 16 = 25", "√25 = 5", 20, 120, ""),
                
                ("Resuelve: 3x - 7 = 14", "7", "3x = 14 + 7 = 21, x = 21÷3 = 7", "avanzado", "algebra", "matematicas",
                 "Despeja x paso a paso", "3x = 21", "x = 7", 20, 120, "x=7"),
                
                ("Calcula √64", "8", "√64 = 8 porque 8 × 8 = 64", "avanzado", "raices", "matematicas",
                 "Que numero al cuadrado da 64?", "8 × 8 = 64", "8", 20, 90, ""),
                
                ("Cuanto es 5³?", "125", "5³ = 5 × 5 × 5 = 125", "avanzado", "potencias", "matematicas",
                 "5 multiplicado 3 veces", "5 × 5 = 25, 25 × 5 = 125", "125", 20, 90, ""),
                
                ("Resuelve: x/3 = 9", "27", "x = 9 × 3 = 27", "avanzado", "algebra", "matematicas",
                 "Multiplica ambos lados por 3", "x = 9 × 3", "x = 27", 20, 90, "x=27"),
                
                ("Cual es el volumen de un cubo de lado 3?", "27", "Volumen = lado³ = 3³ = 27", "avanzado", "geometria", "matematicas",
                 "Formula: lado × lado × lado", "3 × 3 × 3 = 27", "27 cm³", 20, 90, "27 cm3|27cm3"),
                
                ("Simplifica: (x² × x³)", "x⁵", "x² × x³ = x^(2+3) = x⁵", "avanzado", "algebra", "matematicas",
                 "Suma los exponentes", "2 + 3 = 5", "x⁵", 20, 120, "x5|x^5"),
                
                ("Calcula el 15% de 240", "36", "240 × 0.15 = 36", "avanzado", "porcentajes", "matematicas",
                 "15% = 0.15", "240 × 0.15 = 36", "36", 20, 90, ""),
                
                ("Resuelve: 2(x + 3) = 16", "5", "2x + 6 = 16, 2x = 10, x = 5", "avanzado", "algebra", "matematicas",
                 "Distribuye el 2 primero", "2x + 6 = 16", "x = 5", 20, 120, "x=5"),
                
                # INGLÉS - BÁSICO
                ("Como se dice 'casa' en ingles?", "house", "House es la palabra correcta para casa en ingles", "basico", "vocabulario", "ingles",
                 "Es un sustantivo comun", "Piensa en donde vives", "H-O-U-S-E", 10, 30, ""),
                
                ("Como se dice 'perro' en ingles?", "dog", "Dog es la palabra correcta para perro en ingles", "basico", "vocabulario", "ingles",
                 "Es una mascota muy comun", "Hace 'woof woof'", "D-O-G", 10, 30, ""),
                
                ("Como se dice 'gato' en ingles?", "cat", "Cat es la palabra correcta para gato en ingles", "basico", "vocabulario", "ingles",
                 "Es otra mascota comun", "Hace 'meow'", "C-A-T", 10, 30, ""),
                
                ("Como se dice 'agua' en ingles?", "water", "Water es la palabra correcta para agua en ingles", "basico", "vocabulario", "ingles",
                 "La bebemos todos los dias", "Es un liquido esencial", "W-A-T-E-R", 10, 30, ""),
                
                ("Como se dice 'libro' en ingles?", "book", "Book es la palabra correcta para libro en ingles", "basico", "vocabulario", "ingles",
                 "Lo usas para leer", "Tiene paginas", "B-O-O-K", 10, 30, ""),
                
                ("Como se dice 'mesa' en ingles?", "table", "Table es la palabra para mesa", "basico", "vocabulario", "ingles",
                 "Es un mueble", "Comes sobre ella", "T-A-B-L-E", 10, 30, ""),
                
                ("Como se dice 'silla' en ingles?", "chair", "Chair es la palabra para silla", "basico", "vocabulario", "ingles",
                 "Te sientas en ella", "Esta junto a la mesa", "C-H-A-I-R", 10, 30, ""),
                
                ("Como se dice 'escuela' en ingles?", "school", "School es la palabra para escuela", "basico", "vocabulario", "ingles",
                 "Donde vas a aprender", "Tiene maestros y estudiantes", "S-C-H-O-O-L", 10, 30, ""),
                
                ("Como se dice 'computadora' en ingles?", "computer", "Computer es la palabra para computadora", "basico", "vocabulario", "ingles",
                 "Maquina electronica", "Usas teclado y mouse", "C-O-M-P-U-T-E-R", 10, 45, ""),
                
                ("Como se dice 'familia' en ingles?", "family", "Family es la palabra para familia", "basico", "vocabulario", "ingles",
                 "Padres, hijos, hermanos", "Grupo de personas relacionadas", "F-A-M-I-L-Y", 10, 30, ""),
                
                # INGLÉS - INTERMEDIO
                ("Completa: 'I ___ a student' (ser/estar)", "am", "I am a student - se usa AM con el pronombre I", "intermedio", "gramatica", "ingles",
                 "Verbo to be con 'I'", "I siempre va con AM", "I am, you are, he/she is", 15, 45, ""),
                
                ("Completa: 'She ___ happy' (estar)", "is", "She is happy - se usa IS con he/she/it", "intermedio", "gramatica", "ingles",
                 "Verbo to be con 'she'", "She/he/it siempre van con IS", "I am, you are, she/he/it is", 15, 45, ""),
                
                ("Plural de 'child'", "children", "Children es el plural irregular de child (nino)", "intermedio", "gramatica", "ingles",
                 "Es un plural irregular", "No termina en -s", "child → children", 15, 60, ""),
                
                ("Pasado de 'go'", "went", "Went es el pasado irregular del verbo go (ir)", "intermedio", "gramatica", "ingles",
                 "Es un verbo irregular", "No termina en -ed", "go → went", 15, 60, ""),
                
                ("Completa: 'They ___ students' (ser)", "are", "They are students - ARE con they/we/you", "intermedio", "gramatica", "ingles",
                 "Verbo to be plural", "They/we/you van con ARE", "are", 15, 45, ""),
                
                ("Plural de 'man'", "men", "Men es el plural irregular de man", "intermedio", "gramatica", "ingles",
                 "Plural irregular", "No termina en -s", "man → men", 15, 60, ""),
                
                ("Pasado de 'eat'", "ate", "Ate es el pasado irregular de eat (comer)", "intermedio", "gramatica", "ingles",
                 "Verbo irregular", "No termina en -ed", "eat → ate", 15, 60, ""),
                
                ("Completa: 'We ___ happy' (estar)", "are", "We are happy - ARE con we", "intermedio", "gramatica", "ingles",
                 "Verbo to be con 'we'", "We/they/you van con ARE", "are", 15, 45, ""),
                
                ("Plural de 'tooth'", "teeth", "Teeth es el plural irregular de tooth", "intermedio", "gramatica", "ingles",
                 "Plural irregular", "Cambia vowel", "tooth → teeth", 15, 60, ""),
                
                ("Pasado de 'see'", "saw", "Saw es el pasado irregular de see (ver)", "intermedio", "gramatica", "ingles",
                 "Verbo irregular", "No termina en -ed", "see → saw", 15, 60, ""),
                
                # INGLÉS - AVANZADO
                ("Traduce: 'Yo quiero aprender ingles'", "i want to learn english", "I want to learn English - estructura: sujeto + verbo + infinitivo", "avanzado", "traduccion", "ingles",
                 "Estructura: I want to + verbo", "want to = querer", "I want to learn English", 20, 90, "i want learn english"),
                
                ("Completa: 'If I ___ rich, I would travel' (conditional)", "were", "If I were rich... - se usa WERE en condicionales irreales", "avanzado", "gramatica", "ingles",
                 "Segunda condicional usa WERE", "If I were...", "Condicional irreal: were", 20, 120, "was"),
                
                ("Traduce: 'Ella esta estudiando ahora'", "she is studying now", "She is studying now - presente continuo", "avanzado", "traduccion", "ingles",
                 "Presente continuo: is/am/are + -ing", "is studying", "She is studying now", 20, 90, "she's studying now"),
                
                ("Completa: 'I have ___ there' (ir en participio)", "been", "I have been there - participio de 'be'", "avanzado", "gramatica", "ingles",
                 "Presente perfecto", "have/has + participio", "been", 20, 90, ""),
                
                ("Traduce: 'Yo he vivido aqui por 5 anos'", "i have lived here for 5 years", "I have lived here for 5 years - presente perfecto", "avanzado", "traduccion", "ingles",
                 "Presente perfecto: have + participio", "have lived", "I have lived here for 5 years", 20, 120, "i've lived here for 5 years"),
                
                # PROGRAMACIÓN - BÁSICO
                ("Que hace la funcion print() en Python?", "muestra texto", "print() muestra o imprime texto en la pantalla", "basico", "conceptos", "programacion",
                 "Es para mostrar algo", "Se usa para ver resultados", "print('Hola Mundo')", 10, 45, "imprime texto|imprime|mostrar|imprimir|muestra en pantalla|imprime en pantalla"),
                
                ("Como se declara una variable en Python?", "nombre = valor", "En Python: nombre_variable = valor (ej: edad = 25)", "basico", "conceptos", "programacion",
                 "Usa el signo igual", "No necesitas declarar tipo", "edad = 25, nombre = 'Juan'", 10, 60, "variable = valor|nombre=valor|variable=valor"),
                
                ("Que simbolo se usa para comentarios en Python?", "#", "El simbolo # se usa para comentarios de una linea en Python", "basico", "sintaxis", "programacion",
                 "Es para agregar notas al codigo", "Se ignora al ejecutar", "# Esto es un comentario", 10, 30, "numeral|hashtag|gato"),
                
                ("Como se llama el tipo de dato para texto en Python?", "string", "String (str) es el tipo de dato para texto en Python", "basico", "conceptos", "programacion",
                 "Se escribe entre comillas", "Puede ser 'texto' o texto", "nombre = 'Juan' es un string", 10, 45, "str|cadena|texto|cadena de texto"),
                
                ("Que operador se usa para sumar en Python?", "+", "El operador + se usa para suma y concatenacion", "basico", "operadores", "programacion",
                 "Es el simbolo mas comun", "5 + 3 = 8", "a + b", 10, 30, "mas|suma|plus"),
                
                ("Como se llama el tipo de dato para numeros enteros?", "int", "int es el tipo de dato para enteros (integer)", "basico", "conceptos", "programacion",
                 "integer = entero", "edad = 25 es int", "int", 10, 45, "integer|entero|numero entero"),
                
                ("Que funcion se usa para convertir a entero?", "int()", "int() convierte a numero entero", "basico", "funciones", "programacion",
                 "Conversion de tipo", "int('5') = 5", "int()", 10, 45, "int"),
                
                ("Como se escribe un string en Python?", "entre comillas", "Los strings van entre comillas simples ('') o dobles ()", "basico", "sintaxis", "programacion",
                 "Usa ' ' o  ", "nombre = 'Juan' o nombre = Juan", "Entre comillas", 10, 45, "comillas|' '| |con comillas"),
                
                ("Que hace la funcion len()?", "da la longitud", "len() devuelve la longitud de un string o lista", "basico", "funciones", "programacion",
                 "Cuenta elementos", "len('hola') = 4", "Devuelve longitud", 10, 45, "longitud|tamano|contar|cuenta|largo"),
                
                ("Como se llama el tipo de dato True/False?", "bool", "bool o boolean es el tipo de dato logico (True/False)", "basico", "conceptos", "programacion",
                 "True o False", "Valores logicos", "bool o boolean", 10, 45, "boolean|booleano|logico"),
                
                # PROGRAMACIÓN - INTERMEDIO
                ("Que estructura se usa para repetir codigo en Python?", "for", "for o while son bucles para repetir codigo", "intermedio", "estructuras", "programacion",
                 "Los bucles repiten acciones", "for o while", "for i in range(10): print(i)", 15, 60, "while|bucle|loop|ciclo"),
                
                ("Que palabra se usa para decisiones en Python?", "if", "if se usa para tomar decisiones condicionales", "intermedio", "estructuras", "programacion",
                 "Permite tomar decisiones", "Si... entonces...", "if edad > 18: print('Adulto')", 15, 60, "condicional|condicion"),
                
                ("Como se define una funcion en Python?", "def", "def nombre_funcion(): define una funcion", "intermedio", "funciones", "programacion",
                 "Usa la palabra clave def", "def nombre():", "def saludar(): print('Hola')", 15, 90, "definir|define"),
                
                ("Que metodo agrega un elemento a una lista?", "append", "lista.append(elemento) agrega al final de la lista", "intermedio", "listas", "programacion",
                 "Agrega al final de la lista", "lista.append()", "numeros.append(5)", 15, 60, "agregar|anadir|add"),
                
                ("Como se crea una lista vacia en Python?", "[
    ]
