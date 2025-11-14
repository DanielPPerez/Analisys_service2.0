# Este diccionario sería el núcleo de tu archivo src/ml_core/feedback_generator.py
import random
from typing import Dict, Any

CONSEJOS_POR_CODIGO = {
    # =====================================================================
    # == CÓDIGOS DE PROPORCIÓN (proportion_analyzer.py)
    # =====================================================================
    "proporcion_optima": {
        "tipo": "fortaleza",
        "consejos": [
            "¡Las proporciones de tu letra son excelentes! Muy bien equilibrada.",
            "La relación entre el alto y el ancho de tu letra es perfecta.",
            "Tu letra tiene una forma muy armónica y bien proporcionada."
        ]
    },
    "demasiado_estrecha": {
        "tipo": "mejora",
        "consejos": [
            "Tu letra parece un poco delgada. Intenta darle un poco más de espacio a lo ancho para que respire.",
            "Prueba a hacer el trazo un poco más expansivo. Tu letra está un poco comprimida.",
            "Para mejorar la legibilidad, intenta ensanchar un poco la letra. ¡Vas por buen camino!"
        ]
    },
    "demasiado_ancha": {
        "tipo": "mejora",
        "consejos": [
            "¡Buen trazo! Para la próxima, prueba a hacer la letra un poco más esbelta, no tan ancha.",
            "Tu letra es muy clara, pero un poco ancha. Intenta hacerla un poco más alta que ancha.",
            "Estás ocupando mucho espacio horizontal. Trata de compactar la letra un poco."
        ]
    },
    "demasiado_alta": { # Podrías añadir esta lógica a tu analizador
        "tipo": "mejora",
        "consejos": [
            "Tu letra es muy estilizada. Intenta hacerla un poco más baja para que coincida con la altura de las otras letras.",
            "¡Casi perfecto! La letra es un poco alta. Prueba a reducir su altura un poco.",
            "Para un estilo más consistente, intenta que la altura de esta letra sea similar a la de sus vecinas."
        ]
    },
    "demasiado_baja": { # Podrías añadir esta lógica a tu analizador
        "tipo": "mejora",
        "consejos": [
            "Tu letra está un poco corta. Anímate a estirar un poco más el trazo hacia arriba.",
            "¡Buen intento! A esta letra le falta un poco de altura para estar perfecta.",
            "Dale un poco más de altura a tu letra para que se vea más clara y definida."
        ]
    },

    # =====================================================================
    # == CÓDIGOS DE INCLINACIÓN (inclination_analyzer.py)
    # =====================================================================
    "inclinacion_optima": {
        "tipo": "fortaleza",
        "consejos": [
            "¡Tu postura al escribir es genial! La letra está perfectamente vertical.",
            "La inclinación de tu letra es impecable. ¡Sigue así!",
            "Excelente control; tu letra está muy bien alineada verticalmente."
        ]
    },
    "inclinacion_excesiva_derecha": {
        "tipo": "mejora",
        "consejos": [
            "Tu letra está un poco inclinada hacia la derecha. Intenta mantener tu muñeca y el papel más rectos.",
            "Parece que estás escribiendo un poco rápido. Tómate un segundo para enderezar la letra.",
            "Para mejorar, intenta que el trazo principal de la letra sea más perpendicular a la línea base."
        ]
    },
    "inclinacion_excesiva_izquierda": {
        "tipo": "mejora",
        "consejos": [
            "Tu letra se inclina un poco hacia la izquierda. Asegúrate de que tu mano esté en una posición cómoda y relajada.",
            "Un pequeño ajuste en la postura puede ayudar. Intenta enderezar un poco la letra.",
            "¡Casi perfecto! Prueba a que la letra quede más vertical en lugar de inclinada hacia atrás."
        ]
    },

    # =====================================================================
    # == CÓDIGOS DE CONSISTENCIA DEL TRAZO (stroke_consistency_analyzer.py)
    # =====================================================================
    "consistencia_optima": {
        "tipo": "fortaleza",
        "consejos": [
            "¡Tu trazo es muy firme y consistente! La presión que aplicas es muy uniforme.",
            "Excelente control del lápiz. El grosor de tu letra es muy regular.",
            "La consistencia de tu trazo es de libro. ¡Muy buen trabajo!"
        ]
    },
    "trazo_inconsistente": {
        "tipo": "mejora",
        "consejos": [
            "Intenta mantener una presión más constante al escribir. Algunas partes del trazo son más gruesas que otras.",
            "Tu trazo varía un poco. Concéntrate en hacer un movimiento fluido y con la misma presión.",
            "Para un acabado más limpio, prueba a que el grosor de la línea no cambie tanto de principio a fin."
        ]
    },

    # =====================================================================
    # == CÓDIGOS DE ESPACIADO INTERNO (internal_spacing_analyzer.py)
    # =====================================================================
    "espaciado_interno_optimo": {
        "tipo": "fortaleza",
        "consejos": [
            "¡El espacio dentro de tu letra está perfectamente definido! Muy legible.",
            "Los bucles y círculos de tu letra tienen un tamaño ideal. ¡Excelente!",
            "Muy buen trabajo al definir los espacios internos de la letra."
        ]
    },
    "circulo_casi_cerrado": {
        "tipo": "mejora",
        "consejos": [
            "Casi lo tienes. El círculo de tu letra está un poco aplastado. Dale más aire para que respire.",
            "¡A un paso de la perfección! Intenta abrir un poco más el espacio interior de la letra.",
            "Para que sea más fácil de leer, asegúrate de que los bucles internos no se cierren por completo."
        ]
    },
    "circulo_demasiado_abierto": {
        "tipo": "mejora",
        "consejos": [
            "¡Buen trabajo! Para la próxima, intenta cerrar un poco más el círculo o el bucle de la letra.",
            "Tu letra es clara, pero el espacio interior es muy grande. Prueba a hacerlo un poco más pequeño.",
            "El trazo está bien, pero no termines de cerrar la forma. Intenta que los extremos se unan un poco más."
        ]
    },
    "wrong_hole_count": {
        "tipo": "mejora",
        "consejos": [
            "Parece que la forma básica de la letra no es correcta. Por ejemplo, una 'o' se convirtió en una 'u'.",
            "Revisa bien la estructura de la letra. El número de espacios cerrados no coincide con la plantilla.",
            "¡Ojo! Una letra como la 'B' debe tener dos espacios cerrados, y una 'P' solo uno. ¡Revisa tu trazo!"
        ]
    },
    "no_holes_expected": {
        "tipo": "mejora",
        "consejos": [
            "Tu trazo ha creado un círculo donde no debería haberlo. Por ejemplo, una 'u' que parece una 'o'.",
            "Asegúrate de no cerrar completamente la letra si no es necesario.",
            "Esta letra no debería tener espacios internos cerrados. Revisa el modelo y tu trazo."
        ]
    },

    # =====================================================================
    # == CÓDIGOS GENÉRICOS DE ERROR
    # =====================================================================
    "no_contour_found": {
        "tipo": "error",
        "consejos": [
            "No pudimos detectar una letra en la imagen. Asegúrate de escribir dentro del área designada.",
            "La imagen parece estar en blanco o el trazo es demasiado tenue. Intenta escribir con más claridad.",
        ]
    },
    "not_enough_data": {
        "tipo": "error",
        "consejos": [
            "El trazo que hiciste es muy pequeño o corto para poder analizarlo en detalle. Intenta hacerlo un poco más grande.",
            "Necesitamos un trazo un poco más largo para poder darte un buen consejo sobre este punto."
        ]
    }
}

class RuleBasedFeedbackGenerator:
    """
    Genera feedback para el usuario mapeando los códigos de diagnóstico
    a consejos predefinidos.
    """
    def generate_feedback(self, metrics: Dict[str, Any]) -> Dict[str, str]:
        """
        Analiza las métricas y genera un diccionario con fortalezas y áreas de mejora.
        """
        strengths = []
        improvements = []

        # Recorrer todas las métricas de diagnóstico
        for metric_name, details in metrics.items():
            if not isinstance(details, dict): continue
            
            code = details.get("deviation_code")
            score = details.get("score", 0)
            
            if code in CONSEJOS_POR_CODIGO:
                info = CONSEJOS_POR_CODIGO[code]
                consejo = random.choice(info["consejos"])
                
                if info["tipo"] == "fortaleza" or score > 90:
                    strengths.append(consejo)
                elif info["tipo"] == "mejora":
                    improvements.append(consejo)
        
        # Seleccionar la fortaleza y la mejora más importantes
        final_strength = random.choice(strengths) if strengths else "¡Sigue practicando, vas por muy buen camino!"
        
        # Dar prioridad a los consejos de mejora
        if improvements:
            final_improvement = random.choice(improvements)
        elif not strengths:
             final_improvement = "Parece que la imagen está en blanco o el trazo es muy tenue. ¡Inténtalo de nuevo!"
        else:
            final_improvement = "¡Tu letra es prácticamente perfecta! No tenemos ninguna sugerencia por ahora."

        return {
            "fortalezas": final_strength,
            "areas_mejora": final_improvement
        }