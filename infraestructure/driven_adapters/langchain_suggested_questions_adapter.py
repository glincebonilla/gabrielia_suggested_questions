from domain.models.gateways.suggested_questions_gateway import SuggestedQuestionsGateway
from domain.models.suggested_questions_model import SuggestedQuestion

import re
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List

from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.schema.runnable import RunnableConfig
from langchain.callbacks.tracers.langchain import wait_for_all_tracers

from dotenv import load_dotenv, find_dotenv

from external_services.general_parameters import GeneralParametersController

general_parameters = GeneralParametersController()

# Cargar las variables de entorno
load_dotenv(find_dotenv())

class LangchainSuggestedQuestionsAdapter(SuggestedQuestionsGateway):

    def get_parameters(self):
        parameters = general_parameters.get_general_parameters()
        return {
            "suggested_questions_prompt":[item["value"] for item in parameters if any(valor == "suggested_questions_prompt" for valor in item.values())][0],
            "suggested_questions_model": [item["value"] for item in parameters if any(valor == "suggested_questions_model" for valor in item.values())][0]
        }
    

    def get_suggested_questions(self, context:object) -> List[SuggestedQuestion]:
        parameters = self.get_parameters()
        # Inicializar el modelo con tu clave de API y especificar el modelo
        llm = ChatOpenAI(model=parameters.get("suggested_questions_model"))
        prompt_template = PromptTemplate(
            input_variables=["text_context","question_count"],
            template = parameters.get("suggested_questions_prompt")
        )
        dllm_chain = LLMChain(llm=llm, prompt=prompt_template)
        
         # Configurar RunCollectorCallbackHandler
        callback_handler = RunCollectorCallbackHandler()
        config = RunnableConfig(
            callbacks=[callback_handler],
            tags=[context.login, context.name , context.job, context.region, context.sale_point, context.entry_date, context.immediate_boss],
            metadata={"session_id": context.conversation_id}
        )

        text_context = " ".join(context.conversation)
        respuesta = dllm_chain.invoke(input={"text_context": text_context, "question_count": context.question_count}, config=config)
                                   
        # Usar una expresión regular para extraer la parte de la respuesta entre corchetes
        match = re.search(r'\[.*?\]', respuesta["text"], re.DOTALL)
        if match:
            json_str = match.group(0)
            # Parsear la respuesta JSON para obtener la lista de preguntas
            preguntas = json.loads(json_str)

            run = callback_handler.traced_runs[0]
            callback_handler.traced_runs = []
            wait_for_all_tracers()

            return preguntas
        else:
            print("No se encontró una lista JSON en la respuesta.")
            return []