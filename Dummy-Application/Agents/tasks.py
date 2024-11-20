from crewai import  Task


class Tasks:
    def task_question(self, agent):
        return Task(
            description=
            """Engage with the user to understand their research topic by:
                1. Using the conversation processing tool to gather initial information
            """,
            expected_output="Conversation history and initial research requirements as a structured dictionary",
            agent=agent
        )
    def task_research(self, agent, history):
        """Comprehensive research task based on conversation insights"""
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
        
        Using the tools provided:
        1. For Web Research: search, find_similar, get_contents
        2. For Academic Paper review: arxiv_research_tool
        3. For loading documents from web: load_document
        """
        conversation = "\n".join([f"{k}: {v}" for k, v in history.items()]) if history else "No conversation context provided."
        
        return Task(
            description=research_template.format(conversation=conversation),
            expected_output="A structured dictionary with 'abstract, literature review, methodology, results/findings, conclusion' (Note the dictionary should have the exact same keys)",
            agent=agent,
            context=[self.task_question],  # Fixed invocation
        )


    def format_research(self, agent, research_outcomes) :
        """Format research findings into LaTeX-compatible structure"""
        return Task(
            description=f"""Format the research findings into a LaTeX-compatible academic paper structure:
            RESEARCH CONTENT:
            {'\n'.join([f"{k}: {v}" for k, v in research_outcomes.items()])}
            
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
            expected_output="Formatted academic paper structure in a dict format with the keys: 'title, abstract,introduction,literatureReview,methodology,results/findings, references ,conclusion'",
            agent=agent,
            context=[self.task_research]
        )
        
    def task_convert_latex(self, agent, formatted_research, research_name) :
        """Convert formatted research into complete LaTeX document"""
        return Task(
            description=f"""Generate complete LaTeX code for the research paper:
            CONTENT:
            {formatted_research}
            
            REQUIREMENTS:
            1. Use appropriate document class (e.g., 'article', 'paper')
            2. Implement proper sectioning
            3. Follow academic paper formatting guidelines
        
            
            Save as: {research_name}.tex
            Using the  tools provided :
            1.latex_writer_tool 
            """,
            agent=agent,
            expected_output="LaTeX file path containing the formatted research paper",              
            output_file=f"output/{research_name}.tex",
            context=[self.format_research],
        )
    
    def task_convert_latex_to_pdf(self, agent, latex_file_name):
        """Convert LaTeX file to PDF"""
        return Task(
            description=f"""Compile LaTeX file to PDF:
            
            FILE: {latex_file_name}
            
            REQUIREMENTS:
            1. Verify LaTeX syntax
            2. Generate PDF with proper formatting
            """,
            agent=agent,
            expected_output="PDF file path",
            output_file=f"output/{latex_file_name}.pdf",
            context=[self.task_convert_latex],
        )
        
    # todo : add task to store papers in faiss