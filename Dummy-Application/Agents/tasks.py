from crewai import  Task
from typing import Dict, Any
from pydantic import BaseModel
from typing import Dict, Any

# Create a Pydantic model to represent the output structure

class Tasks:
        
    def task_question(self, agent):
        return Task(
            description="Use process_interaction tool to gather initial research information",
            expected_output="A structured dictionary with keys: 'conversation' and 'initial_research_requirements'",
            agent=agent,
        )
        
    
    def task_research(self, agent, conversation_data: Dict[str, Any]) -> Task:
        research_template = """
        Conduct thorough academic research based on the provided conversation:
        
        CONVERSATION CONTEXT:
        {conversation}
        
        RESEARCH REQUIREMENTS:
        1. Analyze key topics and research questions identified
        2. Conduct literature review covering:
        - Recent academic papers (last 5 years)
        - Seminal works in the field
        - Current state-of-the-art
        3. Identify and document:
        - Methodologies used
        - Key findings
        - Research gaps
        - Future directions
        """
        
        # Format conversation data into a string
        conversation = "\n".join([f"{k}: {v}" for k, v in conversation_data.items()]) if conversation_data else "No conversation context provided."
    
        return Task(
            description=research_template.format(conversation=conversation),
            expected_output="A structured dictionary with 'abstract, literature_review, methodology, results, conclusion'",
            agent=agent
        )
        
    def format_research(self, agent, research_outcomes: Dict[str, Any]) -> Task:
        return Task(
            description=f"""Format the research findings into a LaTeX-compatible academic paper structure:
            RESEARCH CONTENT:
            {research_outcomes}
            
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