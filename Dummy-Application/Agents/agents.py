import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from tools import ResearcherToolSet

load_dotenv()

class Agents:
    def __init__(self):
        # Initialize the LLM with model and API key from environment variables
        self.llm = LLM(
            model=os.getenv("MODEL_NAME"),
            api_key=os.environ.get("GROQ_API_KEY")
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
        
    # this agent will do the research and provide a raw format data from the web etc 
    def research_agent(self):
        return Agent(
            llm=self.llm,
            role='Researcher',
            goal=f"Conducting through research on the  conversation of user and llm using the tools arxiv_research_tool , load_document , search ,find_similar,get_content ",
            backstory="""You are a researcher who performs in-depth academic research over varied academic subjects using the following tools 
            
            1.arxiv_research_tool for searching through research paperss of renowned researchers 
            2.load_document for loading pdf documents using web urls 
            3.search  for  searching content on the web 
            4.find_similar  for searching  webpages similar to a given URL.
            5.get_content for getting the contents of the web pages 
            
            -Always stay focused on the research you are doing
            -Try to collect as much refrence using tools as possible 
            -use the tools multiple times as you wish 
            -Do very indepth research on the topics given 
            """,
            allow_delegation=False,
            tools=ResearcherToolSet.research_tools(),
            verbose=False,
        )
    
    
    def research_summarizer_agent(self):
        return Agent(
            llm=self.llm,
            role='Research Summarizer',
            goal="Convert the cluttered research into a summaried format which can be converted   to LaTeX code",
            backstory="You are an expert in converting cluttered research  into  strucutred and summarized format for research papers.",
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
    
    
