from pydantic import BaseModel
from typing import Dict, Any,List


class ConversationOutPutModel(BaseModel):
    conversation:Dict[str,str]
    
    
    
class ResearchPaperModel(BaseModel):
    PAPER:Dict[str,Any]
    
    
    
class ResearchOutComeModel(BaseModel):
    abstract:str
    literature_review:str
    analysis:str
    conclusion:str
    references:List[str]
    
    
class ResearchFormatModel(BaseModel):
    title:str
    abstract:str
    introduction:str
    literature_review:str 
    methodology:str
    results:str
    discussion:str 
    future_work:str 
    conclusion:str 
    references:List[str] 
    

class LatexCodeModel(BaseModel):
    tex_file_path:str 
    research_name:str 
    
class LatexCompiledPathModel(BaseModel):
    pdf_file_path:str 