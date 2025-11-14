# src/adapters/llm_adapter.py

import os
import json
from openai import OpenAI
from typing import Dict, Any, List

class LLMFeedbackGenerator:
    """
    Se comunica con un Modelo de Lenguaje Grande (LLM) para generar
    feedback de caligrafía personalizado y empático.
    """
    def __init__(self, api_key: str = None):
        """
        Inicializa el cliente de OpenAI.
        
        Args:
            api_key: Tu clave de API de OpenAI. Si es None, intentará
                     leerla de la variable de entorno OPENAI_API_KEY.
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró la clave de API de OpenAI. "
                             "Por favor, configúrala en la variable de entorno OPENAI_API_KEY.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o" # Puedes cambiar a "gpt-3.5-turbo" si prefieres

    def _build_prompt(self, character: str, metrics: Dict[str, Any]) -> str:
        """
        Construye el prompt detallado para el LLM a partir de las métricas de análisis.
        """
        # 1. Identificar la fortaleza principal y el área de mejora principal
        # Se asume que las métricas contienen un 'score' entre 0 y 100.
        all_metrics = list(metrics.items())
        
        # Filtra las métricas que tienen un código de desviación útil
        valid_metrics = [m for m in all_metrics if "deviation_code" in m[1] and m[1]["deviation_code"] != "optima"]
        
        # El área de mejora es la métrica válida con la puntuación más baja
        main_improvement_area = min(valid_metrics, key=lambda item: item[1]["score"], default=None)

        # La fortaleza es la métrica con la puntuación más alta
        main_strength = max(all_metrics, key=lambda item: item[1]["score"], default=None)

        # 2. Formatear los datos para el prompt en un JSON limpio
        prompt_data = {
            "puntuacion_general": metrics.get("similarity_score", {}).get("score", "N/A"),
            "metricas_principales": []
        }

        if main_improvement_area:
            metric_name, details = main_improvement_area
            prompt_data["metricas_principales"].append({
                "metrica": metric_name,
                "codigo": details.get("deviation_code", "N/A"),
                "puntuacion": details.get("score", "N/A")
            })
            
        # 3. Construir el prompt final usando una plantilla
        
        # El rol y la personalidad del tutor de IA
        role_definition = (
            "Actúa como un tutor de caligrafía experto, amable, motivador y muy conciso. "
            "Tu objetivo es ayudar a un adulto analfabeta a mejorar su escritura a mano."
        )
        
        # El contexto y los datos del análisis
        context = (
            f"El usuario acaba de practicar la letra '{character}'. "
            "A continuación te proporciono un análisis técnico de su trazo en formato JSON:"
        )
        
        # La tarea específica que debe realizar el LLM
        task = (
            "Basado SOLAMENTE en estos datos, genera un consejo. "
            "1. Empieza con un comentario positivo y de ánimo general. "
            "2. Luego, enfócate en el área de mejora más importante (la métrica con la puntuación más baja). "
            "Explícalo de forma simple y da un consejo práctico y accionable para mejorar. "
            "3. Sé breve y directo. Evita usar los nombres técnicos de las métricas o los códigos de error. "
            "4. Tu respuesta DEBE ser un objeto JSON válido con dos claves: 'fortalezas' (el comentario positivo) "
            "y 'areas_mejora' (el consejo práctico). No incluyas nada más en tu respuesta."
        )

        prompt = f"""
        {role_definition}

        {context}
        ```json
        {json.dumps(prompt_data, indent=2)}
        ```

        {task}
        """
        
        return prompt.strip()

    def generate_feedback(self, character: str, metrics: Dict[str, Any]) -> Dict[str, str]:
        """
        Llama a la API del LLM para generar feedback y parsea la respuesta.

        Args:
            character: La letra que fue analizada.
            metrics: El diccionario completo de métricas de los analizadores geométricos.

        Returns:
            Un diccionario con las claves "fortalezas" y "areas_mejora".
        """
        prompt = self._build_prompt(character, metrics)
        
        try:
            print("\n--- Generando feedback con LLM ---")
            print(f"Prompt enviado a {self.model}:")
            print(prompt)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente servicial que solo responde en formato JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, # Un poco de creatividad, pero no demasiada
                response_format={"type": "json_object"} # Forzar la salida JSON
            )
            
            content = response.choices[0].message.content
            print(f"Respuesta recibida del LLM: {content}")
            
            # Parsear la respuesta JSON del LLM
            feedback = json.loads(content)
            
            # Asegurarse de que las claves esperadas existan
            if "fortalezas" not in feedback or "areas_mejora" not in feedback:
                raise KeyError("La respuesta del LLM no contiene las claves esperadas.")
                
            return feedback

        except Exception as e:
            print(f"Error al comunicarse con la API de OpenAI: {e}")
            # Devolver un feedback genérico en caso de error
            return {
                "fortalezas": "¡Sigue practicando! La constancia es la clave para mejorar.",
                "areas_mejora": "Hubo un problema al generar el consejo. Por favor, inténtalo de nuevo."
            }