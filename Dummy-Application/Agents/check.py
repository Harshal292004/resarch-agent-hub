from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

def process_interaction():
    """Process the user interaction with a predefined prompt template and return full conversation"""
    
    # Get initial user input 
    user_question = input("Hola: ")
    
    # Define a template with placeholders for dynamic insertion 
    prompt_template = """ 
    You are a helpful assistant. Here are some instructions: 
    1. You are here to take more insights on the user's question. 
    2. Ask some intriguing questions so that you can understand what the user knows about the topic. 
    3. Don't get into much depth; ask what the user is trying to research for. 

    Current conversation: {history}
    User's Question: {user_question}
    """
    
    # Initialize the ChatGroq model
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Memory to keep track of the conversation
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="history"
    )

    # Create a PromptTemplate with the defined instructions 
    template = PromptTemplate(
        input_variables=["history", "user_question"], 
        template=prompt_template
    )

    # Create the ConversationChain
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=template,
        verbose=True
    )

    # Initialize user response
    user_response = ""

    # Conversation loop
    while user_response.lower() != "sufficient":
        # Use the chain to generate a response based on the user's question
        response = chain.predict(user_question=user_question)
        print(response)

        # Get new input from the user
        user_response = input("Your response (type 'sufficient' to end): ")
        
        # Update user_question for next iteration
        user_question = user_response

    # Return the entire conversation memory
    return memory.chat_memory.messages

# Call the function and print the conversation
conversation = process_interaction()
print("\nFull Conversation:")
for message in conversation:
    print(f"{message.type}: {message.content}")