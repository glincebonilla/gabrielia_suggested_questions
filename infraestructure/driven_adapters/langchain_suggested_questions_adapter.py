from domain.models.gateways.suggested_questions_gateway import SuggestedQuestionsGateway
from domain.models.suggested_questions_model import SuggestedQuestion

import re
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List
from dotenv import load_dotenv, find_dotenv

# Cargar las variables de entorno
load_dotenv(find_dotenv())

class LangchainSuggestedQuestionsAdapter(SuggestedQuestionsGateway):
    

    def get_suggested_questions(self, context: list[str], question_count: int) -> List[SuggestedQuestion]:
        # Inicializar el modelo con tu clave de API y especificar el modelo
        llm = ChatOpenAI(model='gpt-4o-mini')
        prompt_template = PromptTemplate(
            input_variables=["text_context","question_count"],
            template="Basado en la siguiente conversación:\n {text_context}\n sugiere {question_count} preguntas relevantes y cortas en formato de lista JSON. Cada objeto de la lista debe tener una clave 'question' con el texto de la pregunta."
        )
        dllm_chain = LLMChain(llm=llm, prompt=prompt_template)
        text_context = " ".join(context)
        respuesta = dllm_chain.run(text_context=text_context,question_count=question_count)
                                   
        # Usar una expresión regular para extraer la parte de la respuesta entre corchetes
        match = re.search(r'\[.*?\]', respuesta, re.DOTALL)
        if match:
            json_str = match.group(0)
            # Parsear la respuesta JSON para obtener la lista de preguntas
            preguntas = json.loads(json_str)
            return preguntas
        else:
            print("No se encontró una lista JSON en la respuesta.")
            return []