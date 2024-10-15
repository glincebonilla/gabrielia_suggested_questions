from domain.use_cases.suggested_questions_use_case import SuggestedQuestionsUseCase
from infraestructure.driven_adapters.langchain_suggested_questions_adapter import LangchainSuggestedQuestionsAdapter
from fastapi import FastAPI , Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import sys
sys.path.append('./')

from pydantic import BaseModel

app = FastAPI()

app = FastAPI()

origins = ["*"]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

class SuggestedQuestionsRequest(BaseModel):
    """Request model for the suggested questions endpoint."""
    question_count: int
    conversation: List[str]
    
class SuggestedQuestionController:
    def __init__(self):
        self.suggested_questions_use_case = SuggestedQuestionsUseCase(LangchainSuggestedQuestionsAdapter())

    def get_suggested_questions(self,conversation:list[str],question_count:int)->list[dict]:      
            return  self.suggested_questions_use_case.get_suggested_questions(conversation, question_count)
    
@app.get("/")
async def read_root():
    return {"test_conection": "conection success"}

@app.post("/suggested_questions")
async def get_suggested_questions(request: SuggestedQuestionsRequest, suggestion_controller: SuggestedQuestionController = Depends()):
    """Get suggested questions based"""
    try:
        return suggestion_controller.get_suggested_questions(request.conversation, request.question_count)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

        