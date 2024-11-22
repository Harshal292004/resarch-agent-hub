from crewai import  Task
from typing import Dict, Any
from pydantic import BaseModel
from typing import Dict, Any
    
class OutputModel(BaseModel):
    conversation:Dict[str,str]

class Tasks:
        
    def task_question(self, agent):
        return Task(
            description="Use process_interaction tool to gather initial research information",
            expected_output="A structured dictionary with key: 'conversation'",
            agent=agent,
            output_json=OutputModel
        )
    
    
    def task_research(self, agent, conversation: Dict[str, str]) -> Task:
        print(f"Converstaion in:{conversation}")
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
            async_execution=True
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