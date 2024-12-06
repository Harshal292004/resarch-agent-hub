from crewai import Task
from typing import Dict, Any, List
import json
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
    def unroll_results(self,results):
        # Extract and format papers
        formatted_papers = []
        for idx, paper in enumerate(results["papers"], start=1):
            paper_details = f"""
            Paper {idx}:
            Title: {paper["title"]}
            Authors: {", ".join(filter(None, paper["authors"]))}
            Summary: {paper["summary"]}
            PDF Link: {paper["pdf_link"]}
            """
            formatted_papers.append(paper_details.strip())

        # Extract extracted texts
        extracted_texts = "\n".join(
            [f"Extracted Text {idx+1}: {text}" for idx, text in enumerate(results["extracted_texts"])]
        )

        return "\n\n".join(formatted_papers) + "\n\n" + extracted_texts
            
        
    def task_question(self, agent) -> Task:
        return Task(
            description=(
                """Use process_interaction tool to gather initial research information
                These keywords must never be translated and transformed:
                - Action:
                - Thought:
                - Action Input:
                because they are part of the thinking process instead of the output.
                """
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
        
        
        These keywords must never be translated and transformed:
        - Action:
        - Thought:
        - Action Input:
        because they are part of the thinking process instead of the output.
        """
        params = {
            "author": "Asish Vaswani",
            "title": "Attention is all you need",
            "category": "cs.AI",
            "max_results": 10,
            "sort_by": "lastUpdatedDate",
            "sort_order": "descending",
            "extract_text": True,
        }

        return Task(
            description=extraction_template.format(
                conversation_text=self.format_input_dict(conversation)
            ),
            expected_output="A structured dictionary with key: 'PAPER'",
            agent=agent,
            async_execution=True,
            config=params,  # Pass dictionary directly
        )

    
    def task_research(self, agent, conversation: Dict[str, str],research_papers:Dict[str,Any]) -> Task:
        research_template = """
        RESEARCH PROTOCOL:
        
        CONTEXT:
        {conversation_text}
        {research_papers}

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
           
        These keywords must never be translated and transformed:
        - Action:
        - Thought:
        - Action Input:
        because they are part of the thinking process instead of the output.
        """
        research_papers_unrolled=self.unroll_results(research_papers)
        return Task(
            description=research_template.format(
                conversation_text=self.format_input_dict(conversation),
                research_papers=research_papers_unrolled
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
        
        These keywords must never be translated and transformed:
        - Action:
        - Thought:
        - Action Input:
        because they are part of the thinking process instead of the output.
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

        These keywords must never be translated and transformed:
        - Action:
        - Thought:
        - Action Input:
        because they are part of the thinking process instead of the output.
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
            These keywords must never be translated and transformed:
            - Action:
            - Thought:
            - Action Input:
            because they are part of the thinking process instead of the output.
            """,
            expected_output="Dictionary with key: 'pdf_file_path'",
            output_file=f"{latex_file_path}.pdf",
            agent=agent,
            output_json=LatexCompiledPathModel
        )