# Definición del Menú con precios
MENU = {
    "empanadas colombianas": 12.34, "aros de cebolla": 12.34, 
    "rollos de carne": 12.34, "carimañolas": 12.34, "gallina": 12.34,
    "carnes mixtas": 12.34, "gallina y cerdo": 12.34, "full carnes": 12.34,
    "churrasco": 12.34, "costillitas bbq": 12.34, 
    "combo hamburguesa": 12.34, "bandeja paisa": 12.34, 
    "agua": 12.34, "gaseosa tamaño personal": 12.34, 
    "cerveza": 12.34, "coctel de la casa": 12.34
}

# Mapeo de categorías (para referencia, no para la lógica de búsqueda)
CATEGORIAS = {
    "empanadas colombianas": "ENTRADAS", "aros de cebolla": "ENTRADAS", 
    "gallina": "PICADAS", "carnes mixtas": "PICADAS", 
    "churrasco": "ESPECIALES", "combo hamburguesa": "ESPECIALES",
    "agua": "BEBIDAS", "cerveza": "BEBIDAS"
    # ... otras categorías
}

HORARIO = "Abrimos de jueves a lunes, de 5 PM a 11 PM."

def mostrar_menu():
    """Formatea y muestra el menú completo."""
    # (Mantenemos esta función simple para la demostración)
    menu_str = "\n--- 🍽️ MENÚ TERRAZA ---\n"
    
    # Reconstruimos el menú por categorías para mostrarlo ordenado
    categorias_ordenadas = {
        "ENTRADAS": [], "PICADAS": [], "ESPECIALES": [], "BEBIDAS": []
    }
    for item, cat in CATEGORIAS.items():
        categorias_ordenadas[cat].append(f"  - {item.capitalize()}: ${MENU[item]:.2f}")
        
    for cat, items in categorias_ordenadas.items():
        if items:
            menu_str += f"\n👉 {cat}:\n" + "\n".join(items)
            
    menu_str += f"\n--- ⏰ HORARIO ---\n{HORARIO}"
    return menu_str

def encontrar_items_y_cantidad(mensaje):
    """
    Busca coincidencias de productos del menú y extrae cantidades de un mensaje complejo.
    Implementa PLN básico (tokenización, mapeo y reconocimiento de números).
    """
    mensaje_tokens = mensaje.lower().split()
    items_encontrados = []
    
    # Mapeo simple de números escritos a dígitos (para PLN básico)
    mapa_numeros = {'un': 1, 'una': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6}

    cantidad_predeterminada = 1 # Cantidad si no se especifica
    i = 0
    while i < len(mensaje_tokens):
        token = mensaje_tokens[i]
        cantidad_actual = 1
        
        # 1. Intentar reconocer la cantidad primero (ej. 'dos')
        if token in mapa_numeros:
            cantidad_actual = mapa_numeros[token]
            i += 1
            if i >= len(mensaje_tokens): break # Evitar IndexError

        # Si el token es un dígito (ej. '2')
        elif token.isdigit():
             cantidad_actual = int(token)
             i += 1
             if i >= len(mensaje_tokens): break

        # 2. Intentar reconocer el producto (buscando palabras clave o frases de 2-3 palabras)
        
        # Buscamos frases de 3 palabras (ej. 'coctel de la casa')
        posible_item = " ".join(mensaje_tokens[i:i+3])
        if posible_item in MENU:
            items_encontrados.append((posible_item, cantidad_actual))
            i += 3
            continue

        # Buscamos frases de 2 palabras (ej. 'aros de cebolla' -> 'aros de')
        posible_item = " ".join(mensaje_tokens[i:i+2])
        if posible_item in MENU:
            items_encontrados.append((posible_item, cantidad_actual))
            i += 2
            continue
            
        # Buscamos 1 palabra (ej. 'agua')
        posible_item = mensaje_tokens[i]
        if posible_item in MENU:
            items_encontrados.append((posible_item, cantidad_actual))
            i += 1
            continue
            
        i += 1 # Si no encontramos nada, pasamos al siguiente token

    return items_encontrados

def iniciar_chatbot():
    """Función principal que ejecuta la lógica del chatbot."""
    print("------------------------------------------")
    print("¡Hola! Soy el chatbot de TERRAZA. 👋 ¡Bienvenido!")
    print("------------------------------------------")

    # 1. Solicitar Nombre
    nombre_cliente = input("Chatbot: Antes de tomar tu orden, ¿me podrías decir cuál es tu nombre? \nTú: ")
    nombre_cliente = nombre_cliente.strip().capitalize()
    
    print(f"\nChatbot: ¡Gracias, {nombre_cliente}!")
    print(mostrar_menu())
    print("\nChatbot: Estamos listos para tomar tu orden. Puedes pedir varios artículos a la vez.")
    print("         (Ej: 'Quiero 2 carnes mixtas y un churrasco')")
    
    pedido = {}
    total = 0.0
    
    while True:
        entrada = input("\nTú: ")
        entrada_limpia = entrada.lower().strip()
        
        # Comandos de salida
        if entrada_limpia in ["salir", "no", "seria todo", "no, seria todo", "fin"]:
            break

        # Procesar el mensaje complejo
        items_detectados = encontrar_items_y_cantidad(entrada_limpia)
        
        if items_detectados:
            items_agregados = []
            
            for item, cantidad in items_detectados:
                precio_unitario = MENU[item]
                costo_item = cantidad * precio_unitario
                
                if item not in pedido:
                    pedido[item] = 0
                
                pedido[item] += cantidad
                total += costo_item
                items_agregados.append(f"{cantidad} {item.capitalize()}")
            
            print(f"Chatbot: Entendido. Añadí: {', '.join(items_agregados)} a tu pedido.")
            print(f"Chatbot: Subtotal actual: ${total:.2f}")
            print("\nChatbot: ¿Deseas añadir algo más? (o escribe 'seria todo' para finalizar)")

        elif "menu" in entrada_limpia or "ver menu" in entrada_limpia or "horario" in entrada_limpia:
            print(mostrar_menu())
            print("\nChatbot: ¿Qué te gustaría ordenar?")
        
        else:
            print("Chatbot: Lo siento, no pude identificar ningún artículo del menú en esa frase. Intenta nombrarlos claramente.")

    # 4. Resumen y Finalización
    if total > 0:
        print("\n------------------------------------------")
        print(f"Chatbot: ¡Pedido final confirmado, {nombre_cliente}!")
        print("Detalle de tu orden:")
        
        for item, cant in pedido.items():
            print(f"- {cant}x {item.capitalize()}")

        print(f"\nEl costo TOTAL es: ${total:.2f}")
        print("Tu pedido está siendo procesado. ¡Gracias por ordenar en Terraza! 🥳")
    else:
        print("\nChatbot: Entendido. Esperamos verte pronto.")
    
    print("------------------------------------------")

if __name__ == "__main__":
    iniciar_chatbot()