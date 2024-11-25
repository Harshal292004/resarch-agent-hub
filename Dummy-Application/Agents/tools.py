import os
import io
import re
import json
import PyPDF2
import requests
import subprocess
from crewai_tools import tool
from dotenv import load_dotenv
from QuestioningTool import QuestioningTool
from ResearchTool import ResearchTool
from ExaSearchToolset import ExaSearchToolset
from PydanticBaseModels import ConversationOutPutModel,ResearchOutComeModel,ResearchFormatModel,ResearchPaperModel,LatexCodeModel,LatexCompiledPathModel
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
        output = ConversationOutPutModel(
            conversation=conversation_dict
        )
        return output

    
     # for latex writer
    @tool
    def latex_writer_tool( research_latex_code:str, file_name: str):
        """
        Processes and writes LaTeX content to a .tex file.

        Args:
            research_latex (str): The LaTeX content to write into the file.
            file_name (str): The name of the research document.

        Returns:
            LatexCodeModel: Success or error message.
        """
        # clean the name
        file_name = re.sub(r"[^\w\s]", "", file_name)
        file_name = file_name.lower().replace(" ", "_") + ".tex"

        try:
            with open(file_name, "w") as file:
                file.write(research_latex_code)
            return LatexCodeModel(tex_file_path=file_name,research_name=file_name )
        except Exception as e:
            return f"Error {e}"
        
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
                return LatexCompiledPathModel(pdf_file_path=os.path.join(output_directory or ".",pdf_file))
            else:
                print("Compilation failed")
                print(result.stderr)
                return f"Compilation failed "
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