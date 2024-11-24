import os
import io
import re
import PyPDF2
import subprocess
import requests
import urllib.request as libreq
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
from crewai_tools import tool

""" 
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS 
"""
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq

from dotenv import load_dotenv
from QuestioningTool import QuestioningTool
from tasks import OutputModel
from ResearchTool import ResearchTool
from ExaSearchToolset import ExaSearchToolset

from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from ResearchTool import ArxivResearchTool
load_dotenv()


class ResearcherToolSet:
    
    @tool
    def process_interaction():
        """Process the user interaction with improved context management and flow"""
        
        print("Research Assistant: Hello! I'm here to help with your research project. What would you like to explore?")
        question_tool=QuestioningTool()
        chain = question_tool.create_research_agent()
        conversation_active = True
        
        while conversation_active:
            # Get user input
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'exit':
                conversation_active = False
                continue

            # Generate response
            try:
                response = chain.predict(input=user_input)
                print("\nResearch Assistant:", response)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Please try again or type 'exit' to end the conversation.")
        # Format the conversation directly as a dictionary
        conversation_dict = question_tool.format_conversation(chain.memory.chat_memory.messages)
        
        # Create an OutputModel instance with the dictionary
        output = OutputModel(
            conversation=conversation_dict
        )
        return output

    
     # for latex writer
    @tool
    def latex_writer_tool( research_latex_code, file_name: str):
        """
        Processes and writes LaTeX content to a .tex file.

        Args:
            research_latex (str): The LaTeX content to write into the file.
            file_name (str): The name of the research document.

        Returns:
            str: Success or error message.
        """
        # clean the name
        file_name = re.sub(r"[^\w\s]", "", file_name)
        file_name = file_name.lower().replace(" ", "_") + ".tex"

        try:
            with open(file_name, "w") as file:
                file.write(research_latex_code)
        except Exception as e:
            return f"Error while creating the file: {str(e)}"


    # for latex  to pdf
    @tool('compile_latex_to_pdf')
    def compile_latex_to_pdf(self, latex_file_name,output_directory="Your Researchers"):
        """returns a pdf file with latex written

        Args:
            latex_file_name (_type_): _description_
        """
        if not os.path.exists(latex_file_name):
            print(f"Error: File '{latex_file_name}' not found .")
            return None
        
        
        try:
            pdflatex_path= subprocess.check_output(['where','pdflatex'],
                                                   stderr=subprocess.STDOUT,
                                                   text=True
                                                   )
            print(f"Found pdflatex at: {pdflatex_path}")
        except subprocess.CalledProcessError:
            print("Error : Could not find pdflatex in PATH")
            print("\nCurrent PATH environment:")
            print(os.environ.get('PATH','').replace(';','\n'))
            return None
        #non stop mode stops from any manual input given between the compilation 
        if  output_directory:
            os.makedirs(output_directory,exist_ok=True)
            command=[
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory',
                output_directory,
                latex_file_name
            ]
        else:
            command=[
                'pdflatex',
                '-interaction=nonstopmode',
                latex_file_name
            ]
        
        try:
            print(f"Attempting to run command: {' '.join(command)}")
             
            result= subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False)
            
            if result.stderr:
                print("\nError Output :")
                print(result.stderr)
                
            
            if result.returncode==0:
                print("PDF compiled successfully!")
                pdf_file=os.path.splitext(os.path.basename(latex_file_name))[0]+".pdf"
                return os.path.join(output_directory or ".",pdf_file)
            else:
                print("Compilation failed")
                print(result.stderr)
        except FileNotFoundError:
            print( "File not found")
            return NotImplemented

    def latex_compiler_tools(): 
        return[
            ResearcherToolSet.compile_latex_to_pdf
        ]   
        
    def latex_saver_tools():
        return [
            ResearcherToolSet.latex_writer_tool
        ]
    
    def research_tools():
        web_search_tools = ExaSearchToolset.tools()
        return [
            ResearchTool.load_document,
            *web_search_tools  # Spread the tools from web_search_tools into the list
        ]

        
    def questioning_tools():
        return[
            ResearcherToolSet.process_interaction
        ]
        
    """ def storage_tools():
        return[
            ResearcherToolSet.load_document_to_vector_db
        ] """
        
        
    """ @tool
    def load_document_to_vector_db(self, vector_db: FAISS, research_paper_path):
        _summary_

        Args:
            vector_db (FAISS): _description_
            research_paper_path (_type_): _description_

        Returns:
            _type_: _description_
       
        try:
            # Create loader
            loader = PyPDFLoader(research_paper_path)
            
            # Load documents
            documents = loader.load()
            
            # Create embeddings
            embeddings = HuggingFaceBgeEmbeddings()
            
            # Create text splitter
            text_splitter = CharacterTextSplitter(
                separator='\n',
                chunk_size=500,
                chunk_overlap=200
            )
            
            # Split documents
            doc_chunks = text_splitter.split_documents(documents)
            
            # Add to vector db
            vector_db.add_documents(doc_chunks, embeddings)
            
            return documents
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    
     """