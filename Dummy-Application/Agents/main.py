from crewai import Crew
from agents import Agents
from tasks import Tasks
from tools import ResearcherToolSet
from dotenv import load_dotenv

def main():
    load_dotenv()

    
    print("## Welcome to the resarch paper generator ")
    print('-'*20)
    
    tasks=Tasks()
    agents_=Agents()
    
    # Create agents
    questioning_agent = agents_.questioning_agent()
    research_agent = agents_.research_agent()
    research_summarizer_agent = agents_.resarch_sumarizer_agent()
    latex_converter_agent = agents_.latex_converter_agent()
    latex_to_pdf_agent = agents_.latex_to_pdf_agent()
    
    
    task_question=tasks.task_question(agent=questioning_agent,answer='')
    task_resarch=tasks.task_resarch(agent=research_agent,user_question='',llm_answers='')
    format_resarch=tasks.format_research(agent=research_summarizer_agent,resarch_outcomes='')
    task_convert_latex=tasks.task_convert_latex(agent=latex_converter_agent,resarch_name='')
    task_convert_latex_to_pdf=tasks.task_convert_latex_to_pdf(agent=latex_to_pdf_agent,latex_file_name='')
    
    
    crew=Crew(
        agents=[
            questioning_agent,
            research_agent,
            research_summarizer_agent,
            latex_converter_agent,
            latex_to_pdf_agent
        ],
        tasks=[
            lambda: tasks.task_question(
                agent=questioning_agent
            ),
            
            # Task 2: Research based on conversation history
            lambda conversation: tasks.task_resarch(
                agent=research_agent,
                history=conversation
            ),
            
            lambda research_data:tasks.format_research(
                agent=research_summarizer_agent,
                research_outcomes={
                    'literature_review': research_data.get('literature_review', {}),
                    'methodology_analysis': research_data.get('methodology_analysis', {}),
                    'key_findings': research_data.get('key_findings', []),
                    'research_gaps': research_data.get('research_gaps', []),
                    'future_directions': research_data.get('future_directions', [])
                }
            ),
            
            # Task 4: Convert to LaTeX
            lambda formatted_data: tasks.task_convert_latex(
                agent=latex_converter_agent,
                formatted_research={
                    'title': formatted_data.get('title', ''),
                    'formatted_content': formatted_data.get('formatted_content', {}),
                },
                research_name=formatted_data.get('title', 'research_paper').replace(" ", "_").lower()
            ),
            
            # Task 5: Convert LaTeX to PDF
            lambda latex_path: tasks.task_convert_latex_to_pdf(
                agent=latex_to_pdf_agent,
                latex_file_name=latex_path
            )
        ],
        process="sequential",
        
    ) 
        
    # Execute research paper generation workflow
    result = crew.kickoff()
    
    print("\nResearch Paper Generation Complete!")
    print(result)

if __name__ == "__main__":
    main()
    