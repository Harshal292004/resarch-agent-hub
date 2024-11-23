from crewai import  Task
from typing import Dict, Any,List
from pydantic import BaseModel
from typing import Dict, Any
    
class OutputModel(BaseModel):
    conversation:Dict[str,str]
class ResearchOutcomeModel(BaseModel):
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
class Tasks:
        
    def task_question(self, agent):
        return Task(
            description="Use process_interaction tool to gather initial research information",
            expected_output="A structured dictionary with key: 'conversation'",
            agent=agent,
            output_json=OutputModel
        )
    
    
    def task_research(self, agent, conversation: Dict[str, str]) -> Task:
        research_template = """
            RESEARCH PROTOCOL:
            
            CONTEXT:
            {conversation_text}


            REQUIRED STEPS:
            1. LITERATURE COLLECTION:
            Use arxiv_research_tool
            Requirements:
            - Extract 4 papers per search (maximum allowed)
            - Perform multiple searches with different keywords to get minimum 5 papers
            - Focus on last 5 years
            - Include seminal works
            - Target renowned researchers

            2. RESEARCH ANALYSIS:
            For each paper found:
            - Extract and document key findings
            - Analyze methodology
            - Note empirical results
            - Document implementation details
            
            Organize findings into:
            a) Background and Current State
            b) Methodology Analysis
            c) Empirical Evidence Review

            3. CONTENT EXTRACTION:
            Use load_document for each paper's PDF URL
            
            4. SYNTHESIS:
            Compile a structured report with:
            - Abstract
            - Literature Review
            - Methodology Comparison
            - Results Analysis
            - Conclusions
            - Full References
        """
        
        # Convert conversation dictionary to text
        conversation_text = "\n".join([f"{k}: {v}" for k, v in conversation.items()])
        
        return Task(
            description=research_template.format(conversation_text=conversation_text),
            expected_output="structured dictionary with key: 'abstract','literature_review','analysis','conclusion','references'",
            agent=agent,
            async_execution=True,
            output_json=ResearchOutcomeModel
        )
            
    def format_research(self, agent, research_outcomes: Dict[str, Any]) -> Task:
        research_format_template="""
            TASK: Organize the research findings into a clean, structured format that can be easily converted to LaTeX.

            INPUT RESEARCH:
            {research_text}

            REQUIREMENTS:
            1. Content should be clean and well-organized
            2. Each section should be complete and self-contained
            3. Use proper paragraph breaks
            4. Include in-text citations (Author, Year)
            5. Keep formatting minimal - no special characters or markup
            6. Maintain consistent citation format throughout
            """
        research_text= "\n".join([f"{k}:{v}" for k,v in research_outcomes.items()])
        
        return Task(
            description=research_format_template.format(research_text=research_text),
            expected_output="""Clean, structured dictionary with all required sections ready for LaTeX conversion
            Return a dictionary with these exact keys, where each value contains properly formatted text content:
            {
                "title": "Clear, descriptive title of the paper",
                "abstract": "Concise summary of the research",
                "introduction": "Background and context of the research",
                "literature_review": "Organized review of relevant literature",
                "methodology": "Research approach and methods used",
                "results": "Key findings and outcomes",
                "discussion": "Analysis and interpretation of results",
                "future_work": "Potential future research directions",
                "conclusion": "Summary of key findings and implications",
                "references": [
                    "Author1, Title1, Year1",
                    "Author2, Title2, Year2"
                ]
            }

            """,
            agent=agent,
            async_execution=True,
            output_json=ResearchFormatModel
        )
        
    def task_convert_latex(self, agent, formatted_research: Dict[str, Any], research_name: str) -> Task:
        return Task(
            description=f"""Generate complete LaTeX code for the research paper:
            CONTENT:
            {formatted_research}
            
            REQUIREMENTS:
            1. Use appropriate document class (e.g., 'article', 'paper')
            2. Implement proper sectioning
            3. Follow academic paper formatting guidelines
            
            Save as: {research_name}.tex""",
            expected_output="LaTeX file path containing the formatted research paper",              
            output_file=f"output/{research_name}.tex",
            agent=agent,
            async_execution=True
        )
    
    def task_convert_latex_to_pdf(self, agent, latex_file_path: str) -> Task:
        return Task(
            description=f"""Compile LaTeX file to PDF:
            
            FILE: {latex_file_path}
            
            REQUIREMENTS:
            1. Verify LaTeX syntax
            2. Generate PDF with proper formatting
            """,
            expected_output="PDF file path",
            output_file=f"{latex_file_path}.pdf",
            agent=agent
        )
        
    # todo : add task to store papers in faiss