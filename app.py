# --- app.py: Código Unificado y con CORS ---

# 1. Importaciones necesarias (incluyendo CORS)
from flask import Flask, request, jsonify, render_template
from menu_logic import MENU, mostrar_menu, encontrar_items_y_cantidad 
from flask_cors import CORS

app = Flask(__name__)
# 2. Inicialización de CORS: Vital para permitir la conexión desde GitHub Pages
CORS(app) 

# --- Simulación del Estado de la Conversación ---
PEDIDO_ACTUAL = {}
TOTAL_ACTUAL = 0.0

@app.route('/')
def index():
    """Muestra la interfaz HTML del chatbot (menu.html)."""
    # Flask buscará 'menu.html' dentro de la carpeta 'templates/'
    return render_template('menu.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    global PEDIDO_ACTUAL, TOTAL_ACTUAL
    
    # 1. Obtener el mensaje del usuario (JSON desde JavaScript)
    data = request.get_json()
    entrada = data.get('mensaje', '').lower().strip()
    respuesta = ""
    
    # Comandos de limpieza/reinicio para pruebas sencillas
    if entrada == "reiniciar":
        PEDIDO_ACTUAL = {}
        TOTAL_ACTUAL = 0.0
        return jsonify({'respuesta': "Pedido Reiniciado. ¿Cuál es tu nombre?", 'pedido_actual': PEDIDO_ACTUAL})

    # 2. Manejo de comandos especiales
    if entrada in ["menu", "ver menu", "horario"]:
        respuesta = mostrar_menu()
    
    elif entrada in ["salir", "seria todo", "fin"]:
        if TOTAL_ACTUAL > 0:
             # Generar resumen del pedido
             resumen = "\nPedido final confirmado:\n"
             for item, cant in PEDIDO_ACTUAL.items():
                 # Cálculo final del costo por ítem para el resumen
                 costo_item = cant * MENU[item]
                 resumen += f"- {cant}x {item.capitalize()} (${costo_item:.2f})\n"
             resumen += f"\nEl costo TOTAL es: ${TOTAL_ACTUAL:.2f}. Tu pedido está siendo procesado. ¡Gracias! 🥳"
             
             # Reiniciar estado (muy importante)
             PEDIDO_ACTUAL = {}
             TOTAL_ACTUAL = 0.0
             respuesta = resumen
        else:
             respuesta = "Entendido. Esperamos verte pronto."
    
    else:
        # 3. Procesar el mensaje de pedido usando la lógica de PLN
        items_detectados = encontrar_items_y_cantidad(entrada)
        
        if items_detectados:
            items_agregados = []
            
            for item, cantidad in items_detectados:
                precio_unitario = MENU[item]
                costo_item = cantidad * precio_unitario
                
                PEDIDO_ACTUAL[item] = PEDIDO_ACTUAL.get(item, 0) + cantidad
                TOTAL_ACTUAL += costo_item
                items_agregados.append(f"{cantidad} {item.capitalize()}")

            respuesta = f"Añadí: {', '.join(items_agregados)} a tu pedido. Subtotal actual: ${TOTAL_ACTUAL:.2f}. ¿Algo más?"
        else:
            respuesta = "Lo siento, no pude identificar ese artículo. Escribe 'menu' para ver las opciones."

    # 4. Devolver la respuesta al frontend en formato JSON
    return jsonify({'respuesta': respuesta, 'pedido_actual': PEDIDO_ACTUAL})

if __name__ == '__main__':
    # Asegúrate de crear una carpeta 'templates' en el mismo directorio.
    app.run(debug=True)