from crewai import Task
from typing import Dict, Any, List
from PydanticBaseModels import (
    ConversationOutPutModel,
    ResearchPaperModel,
    ResearchOutComeModel,
    ResearchFormatModel,
    LatexCodeModel,
    LatexCompiledPathModel
)

class Tasks:
    def format_input_dict(self, input_dict: Dict[str, str]) -> str:
        return "\n".join([f"{k}: {v}" for k, v in input_dict.items()])

    def task_question(self, agent) -> Task:
        return Task(
            description=(
                "Use process_interaction tool to gather initial research information"
            ),
            expected_output=(
                "A structured dictionary with key: 'conversation'"
            ),
            agent=agent,
            output_json=ConversationOutPutModel
        )
    
    def task_extract_paper(self, agent, conversation: Dict[str, str]) -> Task:
        extraction_template = """
        EXTRACTION PROTOCOL:
        
        CONTEXT:
        {conversation_text}
        
        INSTRUCTIONS:
        1. Use arxiv_research_tool to gather relevant papers
        2. Focus on renowned authors and seminal work
        3. Store extracted content under 'PAPER' key
        """
        
        return Task(
            description=extraction_template.format(
                conversation_text=self.format_input_dict(conversation)
            ),
            expected_output="A structured dictionary with key: 'PAPER'",
            agent=agent,
            output_json=ResearchPaperModel
        )
    
    def task_research(self, agent, conversation: Dict[str, str]) -> Task:
        research_template = """
        RESEARCH PROTOCOL:
        
        CONTEXT:
        {conversation_text}

        REQUIRED STEPS:
        1. Research Analysis:
           - Extract key findings
           - Document methodology
           - Record empirical results
           - Note implementation details
        
        2. Content Organization:
           - Background/Current State
           - Methodology Analysis
           - Empirical Evidence
        
        3. Content Extraction:
           - Use load_document for PDFs
        
        4. Final Synthesis:
           - Abstract
           - Literature Review
           - Methodology Comparison
           - Results Analysis
           - Conclusions
           - References
        """
        
        return Task(
            description=research_template.format(
                conversation_text=self.format_input_dict(conversation)
            ),
            expected_output="A structured dictionary with keys: 'abstract', 'literature_review', 'analysis', 'conclusion', 'references'",
            agent=agent,
            async_execution=True,
            output_json=ResearchOutComeModel
        )
            
    def format_research(self, agent, research_outcomes: Dict[str, str]) -> Task:
        research_format_template = """
        FORMAT RESEARCH TASK:
        
        INPUT RESEARCH:
        {research_text}

        REQUIREMENTS:
        1. Clean, organized content structure
        2. Complete, self-contained sections
        3. Proper paragraph breaks
        4. Standardized citations (Author, Year)
        5. Minimal formatting
        6. Consistent citation style
        """
        
        return Task(
            description=research_format_template.format(
                research_text=self.format_input_dict(research_outcomes)
            ),
            expected_output="""
            Return dictionary with following structure:
            {
                "title": str,
                "abstract": str,
                "introduction": str,
                "literature_review": str,
                "methodology": str,
                "results": str,
                "discussion": str,
                "future_work": str,
                "conclusion": str,
                "references": List[str]
            }
            """,
            agent=agent,
            async_execution=True,
            output_json=ResearchFormatModel
        )
        
    def task_convert_latex(self, agent, formatted_research: Dict[str, Any], research_name: str) -> Task:
        formatted_content = '\n'.join(
            f"{k}: {v}" if k != 'references' else 
            f"references: {' '.join(ref for ref in v)}" 
            for k, v in formatted_research.items()
        )
        
        conversion_template = """
        LATEX CONVERSION TASK:
        
        CONTENT:
        {formatted_content}
        
        REQUIREMENTS:
        1. Use appropriate document class
        2. Implement proper sectioning
        3. Follow academic formatting
        
        OUTPUT FILE: {research_name}.tex
        """
        
        return Task(
            description=conversion_template.format(
                formatted_content=formatted_content,
                research_name=research_name
            ),
            expected_output="Dictionary with keys: 'tex_file_path', 'research_name'",
            output_file=f"output/{research_name}.tex",
            agent=agent,
            async_execution=True,
            output_json=LatexCodeModel
        )
    
    def task_convert_latex_to_pdf(self, agent, latex_file_path: str) -> Task:
        return Task(
            description=f"""
            PDF COMPILATION TASK:
            
            INPUT FILE: {latex_file_path}
            
            REQUIREMENTS:
            1. Verify LaTeX syntax
            2. Generate formatted PDF
            """,
            expected_output="Dictionary with key: 'pdf_file_path'",
            output_file=f"{latex_file_path}.pdf",
            agent=agent,
            output_json=LatexCompiledPathModel
        )