from crewai import  Task
from typing import Dict, Any
from pydantic import BaseModel
from typing import Dict, Any

# Create a Pydantic model to represent the output structure
class OutputModel(BaseModel):
    conversation:Dict[str, str]
class Tasks:
        
    def task_question(self, agent):
        return Task(
            description="Use process_interaction tool to gather initial research information",
            expected_output="A structured dictionary with key: 'conversation'",
            agent=agent,
            output_json=OutputModel
        )
        
    
    def task_research(self, agent, conversation_data: Dict[str,str]) -> Task:
        
        research_template = """
        COMPREHENSIVE RESEARCH PROTOCOL:

        RESEARCH CONTEXT:
        {conversation}

        DETAILED RESEARCH REQUIREMENTS:
        1. Systematic Literature Review
        - Minimum 10-15 peer-reviewed sources
        - Cover publications from last 5 years
        - Include seminal works in the field
        - Use ArXiv and other academic databases

        2. Research Analysis Framework:
        a) Background and Current State
        - Historical context
        - Evolution of research topic
        - Current technological/scientific landscape

        b) Methodology Deep Dive
        - Comparative analysis of research approaches
        - Strengths and limitations of existing methodologies
        - Innovative techniques and emerging trends

        c) Empirical Evidence
        - Quantitative and qualitative data analysis
        - Statistical significance
        - Reproducibility of findings

        3. Critical Analysis
        - Identify research gaps
        - Propose potential future research directions
        - Discuss potential real-world applications

        4. Comprehensive Documentation
        - Structured academic report
        - Detailed references (APA/IEEE format)
        - In-text citations
        - Potential follow-up research questions

        OUTPUT REQUIREMENTS:
        - Structured academic report
        - Include full bibliography
        - Cite at least 15 sources
        """
        
        # Format conversation data into a string
        conversation = "\n".join([f"{k}: {v}" for k, v in conversation_data.items()]) if conversation_data else "No conversation context provided."
        
        return Task(
            description=research_template.format(conversation=conversation),
            expected_output="A structured dictionary with comprehensive research report of abstract, literature review, methodology, results, conclusion, and full references",
            agent=agent,
            async_execution=True,  # Allow parallel processing
        )
            
    def format_research(self, agent, research_outcomes: Dict[str, Any]) -> Task:
        
        return Task(
            description=f"""Format the research findings into a LaTeX-compatible academic paper structure:
            RESEARCH CONTENT:
            {research_outcomes['conversation']}
            
            REQUIREMENTS:
            1. Structure should include:
               - Abstract
               - Introduction
               - Literature Review
               - Methodology
               - Results/Findings
               - Discussion
               - Future Work
               - Conclusion
            2. Minimum length: 4 pages
            3. Follow academic writing style
            4. Include proper citations
            5. Generate appropriate paper title""",
            expected_output="Formatted academic paper structure in a dict format with the keys: 'title, abstract, introduction, literature_review, methodology, results, discussion, future_work, conclusion, references'",
            agent=agent
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
            agent=agent
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