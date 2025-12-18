"""
Validador Inteligente con ML para PiLearn
"""

import re
from config.constants import THRESHOLDS

try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_DISPONIBLE = True
except ImportError:
    RAPIDFUZZ_DISPONIBLE = False
    print("⚠ RapidFuzz no disponible - funcionalidad reducida")


class ValidadorInteligente:
    """Validador Semántico Inteligente con Fuzzy + Sinónimos"""
    
    def __init__(self):
        self.listo = False
        self._inicializar_sinonimos()
        self.listo = True
        print(f"🤖 Validador cargado: {len(self.mapa_sinonimos)} palabras")
    
    def _inicializar_sinonimos(self):
        """Inicializar grupos de sinónimos"""
        grupos = [
            # Acciones
            ['print', 'imprimir', 'mostrar', 'escribir', 'display', 'sacar'],
            ['crear', 'construir', 'definir', 'hacer', 'generar'],
            # Tipos
            ['string', 'str', 'cadena', 'texto', 'mensaje'],
            ['int', 'integer', 'entero', 'numero', 'número'],
            ['float', 'decimal', 'flotante', 'real'],
            ['bool', 'boolean', 'booleano', 'logico', 'lógico'],
            # Estructuras
            ['lista', 'list', 'arreglo', 'array', '[]'],
            ['diccionario', 'dict', 'mapa', 'hash', '{}'],
            ['tupla', 'tuple', 'par', '()'],
            # I/O
            ['input', 'entrada', 'leer', 'pedir', 'capturar'],
            ['output', 'salida', 'pantalla', 'consola'],
            # Comentarios
            ['comentario', 'nota', '#', '//'],
            ['comillas', '"', "'", '""', "''"],
            # Operadores
            ['suma', 'sumar', '+', 'mas', 'más'],
            ['resta', 'restar', '-', 'menos'],
            ['multiplicacion', 'multiplicar', '*', 'por'],
            ['division', 'dividir', '/', 'entre'],
            # Comparadores
            ['igual', '=='], ['diferente', '!='],
            ['mayor', '>'], ['menor', '<'],
            # Métodos comunes
            ['longitud', 'length', 'len', 'tamaño', 'largo'],
            ['tipo', 'type', 'clase', 'class'],
        ]
        
        self.mapa_sinonimos = {}
        for grupo in grupos:
            grupo_set = set(p.lower() for p in grupo)
            for palabra in grupo:
                self.mapa_sinonimos[palabra.lower()] = grupo_set
    
    def son_sinonimos(self, palabra1, palabra2):
        """Verificar si dos palabras son sinónimos"""
        p1 = palabra1.lower().strip()
        p2 = palabra2.lower().strip()
        
        if p1 == p2:
            return True
        
        simbolos_map = {
            '[]': 'lista', '{}': 'diccionario', '()': 'tupla',
            '"': 'comillas', "'": 'comillas',
            '#': 'comentario', '//': 'comentario',
            '+': 'suma', '-': 'resta', '*': 'multiplicacion', '/': 'division',
            '==': 'igual', '!=': 'diferente', '>': 'mayor', '<': 'menor',
        }
        
        p1_norm = simbolos_map.get(p1, p1)
        p2_norm = simbolos_map.get(p2, p2)
        
        if p1_norm == p2_norm:
            return True
        
        if p1_norm in self.mapa_sinonimos and p2_norm in self.mapa_sinonimos:
            return len(self.mapa_sinonimos[p1_norm] & self.mapa_sinonimos[p2_norm]) > 0
        
        return False
    
    def similitud_semantica(self, texto1, texto2):
        """Calcular similitud semántica entre dos textos"""
        texto1_exp = self._expandir_texto(texto1.lower())
        texto2_exp = self._expandir_texto(texto2.lower())
        
        if self._es_codigo(texto1) or self._es_codigo(texto2):
            return self._comparar_codigo(texto1, texto2)
        
        palabras1 = self._tokenizar(texto1_exp)
        palabras2 = self._tokenizar(texto2_exp)
        
        if not palabras1 or not palabras2:
            return 0.0
        
        usadas = set()
        coincidencias = 0
        
        for p1 in palabras1:
            for j, p2 in enumerate(palabras2):
                if j not in usadas and self.son_sinonimos(p1, p2):
                    coincidencias += 1
                    usadas.add(j)
                    break
        
        similitud = (2.0 * coincidencias) / (len(palabras1) + len(palabras2))
        return min(similitud, 1.0)
    
    def _expandir_texto(self, texto):
        """Expandir funciones y símbolos de Python"""
        expansiones = {
            'int()': ' numero entero integer ',
            'str()': ' texto string cadena ',
            'print()': ' imprimir mostrar ',
            'len()': ' longitud tamaño ',
            '[]': ' lista array ',
            '{}': ' diccionario hash ',
            '()': ' tupla par ',
        }
        
        resultado = texto
        for patron, expansion in expansiones.items():
            resultado = resultado.replace(patron, expansion)
        
        return resultado
    
    def _es_codigo(self, texto):
        """Detectar si es código Python"""
        return bool(re.search(r"\w\s*=\s*\w|\bdef\b|\bclass\b|\breturn\b", texto))
    
    def _comparar_codigo(self, codigo1, codigo2):
        """Comparar fragmentos de código normalizados"""
        if not RAPIDFUZZ_DISPONIBLE:
            return 0.0
        
        n1 = self._normalizar_codigo(codigo1)
        n2 = self._normalizar_codigo(codigo2)
        
        if n1 == n2:
            return 1.0
        
        return fuzz.ratio(n1, n2) / 100.0
    
    def _normalizar_codigo(self, codigo):
        """Normalizar código para comparación"""
        s = codigo.strip()
        s = re.sub(r"\s+", " ", s)
        s = re.sub(r"\".*?\"|\'.*?\'", "STR", s)
        s = re.sub(r"\b\d+(?:\.\d+)?\b", "NUM", s)
        s = re.sub(r"\s*([=+\-*/%<>:,()\[\]{}])\s*", r"\1", s)
        return s.lower()
    
    def _tokenizar(self, texto):
        """Tokenizar texto"""
        txt = re.sub(r"[^\w\s]", ' ', texto.lower())
        return [p for p in txt.split() if len(p) >= 1]
    
    def validar_respuesta(self, respuesta_usuario, respuesta_correcta, materia=""):
        """
        Validar respuesta con IA semántica
        
        Returns:
            tuple: (es_correcta: bool, confianza: float, mensaje: str)
        """
        if not RAPIDFUZZ_DISPONIBLE:
            return self._validar_exacta(respuesta_usuario, respuesta_correcta)
        
        resp_user = str(respuesta_usuario).strip().lower()
        resp_correct = str(respuesta_correcta).strip().lower()
        
        if resp_user == resp_correct:
            return True, 1.0, "✓ Respuesta exacta"
        
        similitud_fuzzy = fuzz.ratio(resp_user, resp_correct) / 100.0
        if similitud_fuzzy >= THRESHOLDS['fuzzy_high']:
            return True, similitud_fuzzy, "✓ Correcto (typo mínimo)"
        
        if self._es_termino_tecnico(resp_correct, materia):
            if similitud_fuzzy >= THRESHOLDS['fuzzy_good']:
                return True, similitud_fuzzy, "✓ Correcto (término técnico)"
            return False, similitud_fuzzy, "Incorrecto"
        
        if not self.listo:
            return False, 0.0, "Validador no disponible"
        
        similitud_sem = self.similitud_semantica(respuesta_usuario, respuesta_correcta)
        
        es_corta = len(resp_correct) <= 3
        umbral_alto = THRESHOLDS['semantic_high_short'] if es_corta else THRESHOLDS['semantic_high_long']
        umbral_bajo = THRESHOLDS['semantic_low_short'] if es_corta else THRESHOLDS['semantic_low_long']
        
        if similitud_sem >= umbral_alto:
            return True, similitud_sem, "🤖 Correcto (semántica)"
        
        if similitud_sem >= umbral_bajo:
            similitud_comb = (similitud_sem * 0.75) + (similitud_fuzzy * 0.25)
            umbral_comb = THRESHOLDS['combined_high_short'] if es_corta else THRESHOLDS['combined_high_long']
            
            if similitud_comb >= umbral_comb:
                return True, similitud_comb, "🤖 Correcto (híbrido)"
        
        return False, similitud_sem, f"Incorrecto ({int(similitud_sem*100)}% similar)"
    
    def _validar_exacta(self, resp_user, resp_correct):
        """Validación exacta cuando no hay librerías ML"""
        if str(resp_user).strip().lower() == str(resp_correct).strip().lower():
            return True, 1.0, "✓ Correcto"
        return False, 0.0, "Incorrecto"
    
    def _es_termino_tecnico(self, texto, materia):
        """Detectar si es un término técnico"""
        if materia != "programacion":
            return False
        
        terminos = {'bool', 'int', 'float', 'str', 'list', 'dict', 'tuple', 
                   'def', 'class', 'if', 'else', 'for', 'while', 'print', 'input',
                   '#', '//', 'and', 'or', 'not'}
        
        palabras = texto.replace(' o ', ' ').split()
        return any(p in terminos for p in palabras)
    
    def esta_listo(self):
        """Verificar si el validador está listo"""
        return self.listo
