import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from tools import ResearcherToolSet
from ResearchTool import ArxivResearchTool

load_dotenv()


class Agents:
    def __init__(self):
        self.llm = LLM(model="groq/llama3-8b-8192", api_key=os.getenv("GROQ_API_KEY"))

    def questioning_agent(self):
        return Agent(
            llm=self.llm,
            role="Questioner",
            goal="Consistently capture user research requirements using process_interaction tool",
            backstory="""You are a systematic data capture agent. 
            - Always use the process_interaction tool 
            - Ensure consistent output structure
            - Preserve exact conversation flow
            - Do not deviate from the original interaction""",
            allow_delegation=False,
            tools=ResearcherToolSet.questioning_tools(),
            verbose=False,
            max_iter=1,
        )

    def research_paper_agent(self):
        return Agent(
            llm=self.llm,
            role="Academic Research Explorer",
            goal="""
            Identify and analyze relevant research papers by:
            1. Understanding the core research requirements
            2. Finding papers that closely match the research criteria
            3. Ensuring comprehensive coverage of the topic
            4. Maintaining academic rigor in paper selection
            """,
            backstory="""You are an expert Academic Research Explorer specialized in discovering relevant scholarly work.

            Key Responsibilities:
            - Systematically search academic papers using arXiv
            - Evaluate paper relevance and impact
            - Maintain consistent research methodology
            - Follow exact research parameters
            
            Tool Usage Protocol:
            1. Analyze the research requirement
            2. Formulate precise search criteria
            3. Execute search using exact tool format below
            
            Required Tool Format:
            Thought: [Explain your search strategy]
            Action: arxiv_research_tool
            Action Input: {
                "author": "string",
                "title": "string",
                "category": "cs.AI",
                "max_results": 4,
                "sort_by": "lastUpdatedDate",
                "sort_order": "descending",
                "extract_text": true
            }
            
            Search Guidelines:
            - Always use arxiv_research_tool
            - Maintain consistent input structure
            - Follow the research scope strictly
            - Document search reasoning clearly
            """,
            allow_delegation=False,
            tools=[ArxivResearchTool()],
            verbose=True,
            max_iter=3,
        )

    def research_agent(self):
        return Agent(
            llm=self.llm,  # Add llm parameter
            role="Researcher",
            goal="Conduct comprehensive academic research following a structured methodology",
            backstory="""You are an expert research analyst with deep expertise in systematic literature review 
            and academic research synthesis.
          
            Remember:
            - Wait for each tool's response before using another tool
            - Don't mix tool usage with final answers
            
            Available tools:
            - load_document: Extract text from PDFs
            - search: Web search
            - find_similar: Find similar web pages
            - get_contents: Get webpage contents""",
            tools=ResearcherToolSet.research_tools(),
            verbose=True,
            allow_delegation=False,
        )

    def research_summarizer_agent(self):
        return Agent(
            llm=self.llm,
            role="Research Summarizer",
            goal="Organize research content into a clean, structured format ready for LaTeX conversion",
            backstory="""You are an expert research organizer who excels at:
            1. Converting cluttered research into clear, structured content
            2. Organizing information logically and coherently
            3. Ensuring consistency in formatting and citations
            4. Preparing content that's ready for LaTeX conversion
            
            Your job is to take research findings and organize them into a clean format 
            that another agent can easily convert to LaTeX.""",
            allow_delegation=False,
            verbose=False,
        )

    def latex_converter_agent(self):
        return Agent(
            llm=self.llm,
            role="LaTeX Code Specialist",
            goal="""
            Transform formatted research into professional LaTeX code by:
            1. Converting structured content into proper LaTeX syntax
            2. Implementing academic paper formatting standards
            3. Ensuring correct handling of mathematical notations
            4. Managing citations and references appropriately
            
            And save it to a tex file using the `latex_saver_tool`
            """,
            backstory="""You are an expert LaTeX Code Specialist with extensive experience in academic Code writing.

            Key Responsibilities:
            - Convert structured research into LaTeX format
            - Apply academic paper templates and styles
            - Handle complex mathematical notations
            - Manage citations and references
            - Generate clean, error-free LaTeX code
            - Also name the research paper yourself 
            
            Document Structure Protocol:
            1. Analyze input format
            2. Apply appropriate LaTeX template
            3. Convert content sections systematically
            4. Implement proper citations
            
            Formatting Guidelines:
            - Use appropriate document class
            - Maintain consistent styling
            - Follow academic formatting standards
            - Ensure proper package inclusion
            - Validate mathematical expressions
            
            Quality Checks:
            - Verify syntax correctness
            - Check mathematical notation
            - Ensure proper section hierarchy
            """,
            allow_delegation=False,
            tools=ResearcherToolSet.latex_saver_tools(),
            verbose=True,
            max_iter=2,
        )

    def latex_to_pdf_agent(self):
        return Agent(
            llm=self.llm,
            role="LaTeX PDF Compiler Specialist",
            goal="""
            Transform LaTeX (.tex) files into professional PDF documents by:
            1. Executing proper LaTeX compilation process using the `compile_latex_to_pdf` tool
            2. Ensuring high-quality PDF output generation
            """,
            backstory="""You are an expert LaTeX PDF Generation Specialist with extensive experience in document compilation.

            Key Responsibilities:
            Use the `compile_latex_to_pdf` 
            
            Tool Usage Requirements:
            - Use provided `compile_latex_to_pdf` with a file_path of the .tex file to be compiled 
            """,
            allow_delegation=False,
            tools=ResearcherToolSet.latex_saver_tools(),
            verbose=True,
            max_iter=3,
        )
