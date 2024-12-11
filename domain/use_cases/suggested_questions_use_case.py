from domain.models.gateways.suggested_questions_gateway import SuggestedQuestionsGateway
from domain.models.suggested_questions_model import SuggestedQuestion
from typing import List

class SuggestedQuestionsUseCase:
    def __init__(self, suggested_questions_gateway: SuggestedQuestionsGateway):
        self.suggested_questions_gateway = suggested_questions_gateway

    def get_suggested_questions(self, context: object) -> List[SuggestedQuestion]:
        if not context:
            raise ValueError("Context cannot be empty.")
        return self.suggested_questions_gateway.get_suggested_questions(context)