import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from tools import ResearcherToolSet
from langchain_openai import ChatOpenAI
load_dotenv()

class Agents:
    def __init__(self):
        # Initialize the LLM with model and API key from environment variables
        """ self.llm = LLM(
            model="huggingface/Qwen/Qwen2.5-Coder-3B-Instruct",  # You can change the model
            api_base="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-3B-Instruct",
        )
        """
        self.llm=LLM(
            model="groq/llama3-8b-8192",
            api_key=os.getenv("GROQ_API_KEY")    
        )
    # this agent will question  the user and take his her queries 
    def questioning_agent(self):
        return Agent(
            llm=self.llm,
            role='Questioner',
            goal="Consistently capture user research requirements using process_interaction tool",
            backstory="""You are a systematic data capture agent. 
            - Always use the process_interaction tool 
            - Ensure consistent output structure
            - Preserve exact conversation flow
            - Do not deviate from the original interaction""",
            allow_delegation=False,  # Prevent deviation
            tools=ResearcherToolSet.questioning_tools(),
            verbose=False,
            max_iter=1
        ) 
  
    def research_agent(self):
        return Agent(
            role='Researcher',
            goal="Conduct comprehensive academic research following a structured methodology",
            backstory="""You are an expert research analyst with deep expertise in systematic literature review 
            and academic research synthesis.
            
            VERY IMPORTANT - When using tools, you MUST use this exact format:
            
            Thought: [your reasoning]
            Action: arxiv_research_tool
            Action Input: {"author": "string", "title": "string", "category": "cs.AI", "max_results": 4, "sort_by": "lastUpdatedDate", "sort_order": "descending", "extract_text": true}
            
            After getting the Observation, you can either:
            1. Use another tool with the same format
            2. Provide your Final Answer
            
            Remember:
            - Always include "Thought:", "Action:", and "Action Input:" prefixes
            - The Action Input must be a valid JSON object without escaped quotes
            - Only use one tool at a time
            - Wait for each tool's response before using another tool
            - Don't mix tool usage with final answers
            
            Available tools:
            - arxiv_research_tool: Search academic papers
            - load_document: Extract text from PDFs
            - search: Web search
            - find_similar: Find similar web pages
            - get_contents: Get webpage contents""",
            tools=ResearcherToolSet.research_tools(),
            verbose=True,
            allow_delegation=False
        )
        
    def research_summarizer_agent(self):
        return Agent(
            llm=self.llm,
            role='Research Summarizer',
            goal="Organize research content into a clean, structured format ready for LaTeX conversion",
            backstory="""You are an expert research organizer who excels at:
            1. Converting cluttered research into clear, structured content
            2. Organizing information logically and coherently
            3. Ensuring consistency in formatting and citations
            4. Preparing content that's ready for LaTeX conversion
            
            Your job is to take research findings and organize them into a clean format 
            that another agent can easily convert to LaTeX.""",
            allow_delegation=True,
            verbose=False
        )
    # this agent will  convert the unstructured research of the research agent to a latex format and convert to pdf 
    def latex_converter_agent(self):
        return Agent(
            llm=self.llm,
            role='LaTeX Converter ',
            goal="Convert the given formated research to latex code and then save it to latex file",
            backstory="You are an expert in converting format research  into LaTeX code for research papers.",
            allow_delegation=True,
            verbose=False,
            tools=ResearcherToolSet.latex_conver_tools()
        )
    
    def latex_to_pdf_agent(self):
        return Agent(
            llm=self.llm,
            role="Latex to Pdf saver",
            goal='Given a latex file find it and convert it to a pdf using the tools provided',
            backstory='You are skilled in conveerting given latex file to a pdf file',
            allow_delegation=True,
            tools=ResearcherToolSet.latex_conver_tools()
        )
        
       
    

    
    # todo: add a agent that can store the final pdf docs to a faiss data base for a particular user so that we can add memeory to general caht bot 
    
    
