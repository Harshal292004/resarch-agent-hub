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
    
    # Initialize tasks and agents
    tasks_manager = Tasks()
    agents_manager = Agents()
    
    # Create agents
    questioning_agent = agents_manager.questioning_agent()
    research_agent = agents_manager.research_agent()
    research_summarizer_agent = agents_manager.research_summarizer_agent()
    latex_converter_agent = agents_manager.latex_converter_agent()
    latex_to_pdf_agent = agents_manager.latex_to_pdf_agent()
    
    # Create task instances
    task1 = tasks_manager.task_question(
        agent=questioning_agent
    )
    
    task2 = tasks_manager.task_research(
        agent=research_agent,
        history={}  # This will be populated by task1's output
    )
    
    task3 = tasks_manager.format_research(
        agent=research_summarizer_agent,
        research_outcomes={}  # This will be populated by task2's output
    )
    
    task4 = tasks_manager.task_convert_latex(
        agent=latex_converter_agent,
        formatted_research={},  # This will be populated by task3's output
        research_name="research_paper"  # This will be updated based on the research topic
    )
    
    task5 = tasks_manager.task_convert_latex_to_pdf(
        agent=latex_to_pdf_agent,
        latex_file_name="research_paper"  # This will be updated based on task4's output
    )
    
    # Create crew with sequential tasks
    crew = Crew(
        agents=[
            questioning_agent,
            research_agent,
            research_summarizer_agent,
            latex_converter_agent,
            latex_to_pdf_agent
        ],
        tasks=[
            task1,
            task2,
            task3,
            task4,
            task5
        ],
        process="sequential",
        verbose=True
    )
      
    # Execute research paper generation workflow
    result = crew.kickoff()
    
    print("\nResearch Paper Generation Complete!")
    print(result)

if __name__ == "__main__":
    main()
    