from abc import ABCMeta, abstractmethod
from typing import List
from domain.models.suggested_questions_model import SuggestedQuestion

class SuggestedQuestionsGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_suggested_questions(self, context: object) -> List[SuggestedQuestion]:
        "Get suggested questions based on the given context."

