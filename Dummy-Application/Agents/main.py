from crewai import Crew
from agents import Agents
from tasks import Tasks
from tools import ResearcherToolSet
from dotenv import load_dotenv
import os 
def main():
    load_dotenv()
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    print("## Welcome to the Research Paper Generator")
    print('-'*50)
    
    # Initialize managers
    tasks_manager = Tasks()
    agents_manager = Agents()
    
    # Create agents
    questioning_agent = agents_manager.questioning_agent()
    research_agent = agents_manager.research_agent()
    research_summarizer_agent = agents_manager.research_summarizer_agent()
    latex_converter_agent = agents_manager.latex_converter_agent()
    latex_to_pdf_agent = agents_manager.latex_to_pdf_agent()
    
    # Execute tasks sequentially and store results
    print("\nStep 1: Initial Questioning")
    task1 = tasks_manager.task_question(questioning_agent)
    crew1 = Crew(
        agents=[questioning_agent],
        tasks=[task1],
        verbose=True
    )
    conversation_result = crew1.kickoff()
    print(f"Conversation Result: {conversation_result}")
    
    task2= tasks_manager.task_research(Tasks)
    """ # Create tasks
    task1 = tasks_manager.task_question(questioning_agent)
    task2 = tasks_manager.task_research(research_agent)
    task3 = tasks_manager.format_research(research_summarizer_agent)
    task4 = tasks_manager.task_convert_latex(latex_converter_agent)
    task5 = tasks_manager.task_convert_latex_to_pdf(latex_to_pdf_agent)
    
    # Create crew with sequential tasks
    crew = Crew(
        agents=[
            questioning_agent,
            research_agent,
            research_summarizer_agent,
            latex_converter_agent,
            latex_to_pdf_agent
        ],
        tasks=[task1, task2, task3, task4, task5],
        process="sequential",
        verbose=True
    )
    
    # Execute the workflow
    result = crew.kickoff()
    
    print("\nResearch Paper Generation Complete!")
    print(f"Result: {result}")
    """
if __name__ == "__main__":
    main()
    