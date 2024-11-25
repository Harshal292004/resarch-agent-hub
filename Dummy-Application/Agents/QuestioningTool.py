from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq

from dotenv import load_dotenv

class QuestioningTool():
    def __init__(self):
        load_dotenv()
        pass
    def create_research_agent(self):
            """Create and configure the research-focused chat agent"""
            
            llm = ChatGroq(
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

            # Enhanced prompt template with corrected input variables
            prompt_template = """You are an intelligent research assistant focused on helping users develop academic projects and research.

            Key Objectives:
            1. Understand the core research topic or project goal
            2. Identify knowledge gaps and technical requirements
            3. Provide relevant suggestions and insights
            4. Maintain context throughout the conversation
            
            Conversation Guidelines:
            - Ask focused, relevant follow-up questions (max 2 per response)
            - Build upon previous responses
            - Provide specific examples or suggestions when possible
            - Guide the conversation towards practical next steps
            
            Previous Conversation: {history}
            Human: {input}
            
            Assistant:"""

            # Corrected memory configuration
            memory = ConversationBufferMemory()

            # Create prompt template with correct input variables
            template = PromptTemplate(
                input_variables=["history", "input"],
                template=prompt_template
            )

            return ConversationChain(
                llm=llm,
                prompt=template,
                memory=memory,
                verbose=True
            )
        
        
        
    def format_conversation(self,messages):
        """Format the conversation history in a readable way"""
        formated_conversation_dict={}
        print("\n=== Conversation Summary ===")
        for i, message in enumerate(messages, 1):
            role = "Human" if message.type == "human" else "Assistant"
            formated_conversation_dict[f"{i}. {role}:"]=message.content
            
        return formated_conversation_dict
                
        
    def process_interaction(self):
        """Process the user interaction with improved context management and flow"""
        
        print("Research Assistant: Hello! I'm here to help with your research project. What would you like to explore?")
        
        chain = self.create_research_agent()
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

        return self.format_conversation(chain.memory.chat_memory.messages)