import random
import json

def create_character(level = 1, echo_level_ups = False, game="nd20"):

    # Comprobamos qué fichero JSON vamos a cargar.
    if game == "nd20_cifi":
        ocupaciones_file = 'ocupaciones_cifi'
    else:
        ocupaciones_file = 'ocupaciones'
    
    # Lo mismo para las especies.
    if game == "nd20_cifi":
        especies_file = 'especies_cifi'
    else:
        especies_file = 'especies'

    # Cargar el archivo JSON de Ocupaciones
    with open('data/' + ocupaciones_file + '.json', 'r', encoding='utf-8') as file:
        ocupaciones = json.load(file)

    # Cargar el archivo JSON de Especies
    with open('data/' + especies_file + '.json', 'r', encoding='utf-8') as file:
        especies = json.load(file)

    def calcular_dado_salud_base(dado_base, modificacion):
        # Escala de dados de Salud posibles
        dados_salud = ["d4", "d6", "d8", "d10", "d12", "d20"]
        # Validar el dado de Salud base
        if dado_base not in dados_salud:
            raise ValueError("Dado de Salud base no válido")
        # Calcular el índice del dado base en la lista
        indice_base = dados_salud.index(dado_base)
        # Aplicar la modificación
        nuevo_indice = indice_base + modificacion
        # Asegurarse de que el nuevo índice esté dentro de los límites
        nuevo_indice = max(0, min(nuevo_indice, len(dados_salud) - 1))
        # Obtener el nuevo dado de Salud
        nuevo_dado = dados_salud[nuevo_indice]
        # Devolver el dado ya calculado
        return nuevo_dado

    def calcular_salud(dado, nivel):
        salud_final = 0
        dado_salud_entero = int(dado[1:])
        if nivel == 1:
            salud_final = dado_salud_entero
        else:
            salud_final = dado_salud_entero
            salud_final += (dado_salud_entero/2) * (nivel - 1)
        return int(salud_final)

    # Función para generar atributos aleatorios
    def generar_atributos():
        lista_atributos = ["Fuerza", "Agilidad", "Resistencia", "Mente", "Intuición", "Presencia"]
        atributos = {}
        for atributo in lista_atributos:
            atributos[atributo] = random.randint(4, 9)
        return atributos

    def mejorar_atributos(nivel, atributos, atributo_favorito, echo_msg = False):
        if echo_msg:
            print("=======================")
        mejoras_disponibles = nivel - 1
        mejoras_disponibles *= 2
        if mejoras_disponibles <= 0:
            return atributos  # No hay mejoras disponibles, devolver los atributos sin cambios
        
        while mejoras_disponibles > 0:
            # Crear la lista de atributos a elegir, incluyendo el favorito dos veces
            atributos_a_elegir = list(atributos.keys())
            atributos_a_elegir.extend([atributo_favorito, atributo_favorito])

            atributo_1 = random.choice(atributos_a_elegir)
            #atributos_a_elegir.remove(atributo_1)
            atributos_a_elegir = [a for a in atributos_a_elegir if a != atributo_1]
            atributo_2 = random.choice(atributos_a_elegir)
            
            # Elegir dos atributos al azar de la lista
            #atributos_elegidos = random.sample(atributos_a_elegir, 2)
            atributos_elegidos = [atributo_1, atributo_2]
            if echo_msg:
                print("  — Atributos en el Nivel", int(mejoras_disponibles / 2) + 1, atributos_elegidos)
            for atributo in atributos_elegidos:
                # Si el atributo es el favorito, lanzar dos dados de 20 y quedarse con el mejor resultado
                if atributo == atributo_favorito:
                    tirada_1 = random.randint(1, 20)
                    tirada_2 = random.randint(1, 20)
                    mejor_tirada = max(tirada_1, tirada_2)
                else:
                    tirada = random.randint(1, 20)
                    mejor_tirada = tirada
                
                # Si el resultado es mayor que el valor actual del atributo, mejora en 1 punto
                if mejor_tirada > atributos[atributo]:
                    if echo_msg:
                        print("   ‡ Mejorando", atributo, "— Actual", atributos[atributo])
                    atributos[atributo] += 1
                    if echo_msg:
                        print("   ‡ Atributo", atributo, "mejorado a", atributos[atributo])
                else:
                    if echo_msg:
                        print("   † No se ha mejorado", atributo)
                mejoras_disponibles -= 1
                
                # Si no quedan mejoras disponibles, salir del bucle
                if mejoras_disponibles <= 0:
                    break
        if echo_msg:
            print("=======================")
        return atributos

    # Función para elegir especie aleatoriamente con requisitos de atributos
    def elegir_especie(atributos):
        especie = random.choice(list(especies.keys()))
        atributo_requisito = especies[especie].get("atributo_requisito")
        atributo_valor = especies[especie].get("atributo_valor", 0)
        dado_salud = especies[especie].get("salud")
        mov = especies[especie].get("movimiento")

        if atributo_requisito and atributos.get(atributo_requisito, 0) >= atributo_valor:
            return especie, dado_salud, mov
        else:
            return None, None, None

    # Función para elegir ocupación aleatoriamente
    def elegir_ocupacion():
        ocupacion = random.choice(list(ocupaciones.keys()))
        atributo_favorito = random.choice(ocupaciones[ocupacion].get("atributo_favorito", []))
        mod_salud = ocupaciones[ocupacion].get("salud")
        energia = ocupaciones[ocupacion].get("esfuerzo")
        # Aumentar en 1 el valor del Atributo Favorito
        atributos[atributo_favorito] += 1
        return ocupacion, atributo_favorito, mod_salud, energia

    # Función para elegir talentos aleatoriamente
    def elegir_talentos(especie, ocupacion):
        talentos_ocupacion = ocupaciones[ocupacion].get("talentos", [])
        talentos_especie = especies.get(especie, {}).get("talentos", [])
        return talentos_ocupacion + talentos_especie

    # Función para generar riqueza inicial
    def generar_riqueza_inicial(nivel = 1):
        return (random.randint(4, 40) * 10) + (nivel * 100)

    def elegir_equipo(ocupacion, especie):
        # Lista de armas disponibles basadas en la ocupación y especie
        armas_disponibles = ocupaciones[ocupacion]["armas"]
        armaduras_disponibles = ocupaciones[ocupacion]["armaduras"]
        lista_objeto_emocional = especies[especie]["objetos_emocionales"]

        if len(lista_objeto_emocional) == 0:
            lista_objeto_emocional = [
                "Collar con un símbolo de la luz",
                "Anillo de la familia",
                "Libro de cuentos de la infancia",
                "Amuleto de protección",
                "Reliquia familiar"
            ]
        # Elegir aleatoriamente un arma, armadura y objeto emocional de las listas disponibles
        arma = random.choice(armas_disponibles)
        armadura = random.choice(armaduras_disponibles)
        objeto_emocional = random.choice(lista_objeto_emocional)
        return arma, armadura, objeto_emocional

    # Función para elegir un nombre aleatorio
    def elegir_nombre(especie = None):
        # Diccionario de nombres por Especie
        nombres_por_especie = especies[especie]["nombres"]
        # Lista de nombres aleatorios de todas partes del mundo
        nombres_genericos = [
            "Alethea", "Yusuf", "Sofia", "Chen Wei", 
            "Isabella", "Muhammad", "Mia", "Sakura", 
            "Liam", "Olivia", "Ahmed", "Ava", 
            "Carlos", "Zara", "Elena", "Hiroshi", 
            "Emma", "Amina", "Lucas", "Luna", 
            "Abdullah", "Santiago", "Aria", "Shan", 
            "Sophia", "Ananya", "Rafael", "Nina", 
            "Surya", "Eva", "Hikari", "Noah", 
            "Hana", "Ella", "Hassan", "Zahara", 
            "Adriana", "Nadia", "Lina", "Ibrahim", 
            "Naoki", "Leila", "Eduardo", "Gangorion"
        ]
        if len(nombres_por_especie) > 0:
            return random.choice(nombres_por_especie)
        else:
            # Si la Especie no está en el diccionario, se elige un nombre genérico
            return random.choice(nombres_genericos)
    # ------------------------------------------------------------------
    # Función para generar un concepto aleatorio
    def generar_concepto(ocupacion, especie):
        conceptos_ocupacion = ocupaciones.get(ocupacion, {}).get("conceptos", [])
        conceptos_especie = especies.get(especie, {}).get("conceptos", [])
        
        concepto = random.choice(conceptos_ocupacion + conceptos_especie)
        return concepto
    # ------------------------------------------------------------------
    # Generar el personaje
    # ------------------------------------------------------------------
    # Creamos los Atributos del personaje.
    # ------------------------------------------------------------------
    atributos = generar_atributos()
    # ------------------------------------------------------------------
    # Loop para asegurarse de que el personaje tiene una especie válida.
    # ------------------------------------------------------------------
    especie = None
    while especie is None:
        especie, dado_salud, movimiento = elegir_especie(atributos)
    # ------------------------------------------------------------------
    ocupacion, atributo_favorito, mod_salud, energia = elegir_ocupacion()
    # ------------------------------------------------------------------
    if especie:
       # concepto = generar_concepto(ocupacion, especie["nombre"])
       concepto = generar_concepto(ocupacion, especie)
    else: 
        concepto = generar_concepto(ocupacion, None)
    # ------------------------------------------------------------------
    talentos = elegir_talentos(especie, ocupacion)
    riqueza_inicial = generar_riqueza_inicial(level)
    arma, armadura, objeto_emocional = elegir_equipo(ocupacion, especie)
    # ------------------------------------------------------------------
    modificacion = mod_salud  # Modificación (+1 para subir un rango, -1 para bajar)
    nuevo_dado_salud = calcular_dado_salud_base(dado_salud, modificacion)
    valor_salud = calcular_salud(nuevo_dado_salud, level)
    # ------------------------------------------------------------------
    if level >= 12:
        energia += 1
    # ------------------------------------------------------------------
    atributos_nuevos = mejorar_atributos(level, atributos, atributo_favorito, echo_level_ups)
    # ------------------------------------------------------------------
    nombre = elegir_nombre(especie)  
    # ------------------------------------------------------------------
    # Imprimir el personaje generado en el formato deseado
    # ------------------------------------------------------------------
    personaje = {
        "Nombre": nombre,
        "Concepto": concepto,
        "Especie": especie if especie is not None else "Humano común",
        "Ocupacion": ocupacion if ocupacion is not None else "Aventurero",
        "Nivel": level,
        "Atributos": atributos_nuevos,
        "AtributoF": atributo_favorito,
        "Salud": f"{valor_salud} [{nuevo_dado_salud}]",
        "Esfuerzo": energia,
        "Movimiento": movimiento,
        "Talentos": talentos,
        "Riqueza": riqueza_inicial,
        "Arma": arma,
        "Armadura": armadura,
        "Objeto": objeto_emocional
    }
    # ------------------------------------------------------------------
    return personaje
