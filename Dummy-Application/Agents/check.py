from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

def arxiv_research_tool(
        author: Optional[str] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        max_results: int = 1,
        sort_by: str = "relevance",
        sort_order: str = "ascending",
        extract_text: bool = True
    ) -> Dict:
        """Search and extract research papers from ArXiv.
        Using tool: arxiv_research
        Tool Input:
        arxiv_research(
            author="Geoffrey Hinton",
            title="dropout layers",
            category="cs.LG",
            max_results=4,
            sort_by="date",
            sort_order="descending",
            extract_text=False
        )    
        """
        try:
            # Input validation
            if not any([author, title, category]):
                category = "cs.AI"

            # Prepare search query
            search_parts = []
            if author:
                search_parts.append(f"au:{quote(author)}")
            if title:
                search_parts.append(f"ti:{quote(title)}")
            if category:
                search_parts.append(f"cat:{quote(category)}")

            search_query = "+AND+".join(search_parts)

            # Prepare API request
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": search_query,
                "max_results": min(max(1, max_results), 4),
                "sortBy": sort_by if sort_by in ["relevance", "lastUpdatedDate", "submittedDate"] else "relevance",
                "sortOrder": sort_order.lower() if sort_order.lower() in ["ascending", "descending"] else "ascending",
            }
            
            url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            # Execute request
            with libreq.urlopen(url, timeout=10) as response:
                xml_data = response.read().decode("utf-8")

            # Parse results
            soup = BeautifulSoup(xml_data, "xml")
            entries = soup.find_all("entry")

            results = {
                "papers": [],
                "extracted_texts": []
            }

            for entry in entries:
                paper_info = {
                    "title": entry.find("title").text.strip() if entry.find("title") else "No Title",
                    "authors": [a.text for a in entry.find_all("author")],
                    "summary": entry.find("summary").text.strip() if entry.find("summary") else "No Summary",
                    "pdf_link": entry.find("link", title="pdf")["href"] if entry.find("link", title="pdf") else None,
                }
                results["papers"].append(paper_info)

                if extract_text and paper_info['pdf_link']:
                    text = extract_text(paper_info['pdf_link'])
                    results["extracted_texts"].append(text)

            return results

        except Exception as e:
            return {"error": str(e), "papers": [], "extracted_texts": []}

    
def extract_text(file_path_url):
    """This tool helps in loading documents and extracting text from them for research purpose 
    
    Args:
        file_path_url (str): its the url of the pdf of which the text is to extracted 

    Returns:
        str: returns the first 2 pages of research done 
    """
    try:
        response=requests.get(file_path_url)
        response.raise_for_status() # Raise an exception for bad status codes
        
        pdf_file_obj=io.BytesIO(response.content)
        
        pdf_reader=PyPDF2.PdfReader(pdf_file_obj)
        
        text=""
        
        num_pages=min(4,len(pdf_reader.pages))
        
        for page_num in range(num_pages):
            text+=pdf_reader.pages[page_num].extract_text()

        return text
    except requests.RequestException as e:
        print(f"Error occured:{e}")
        return None
    except Exception as e:
        print(f"Error occured in processing of pdf:{e}")
        return None 

def main():
    """Main function to run the research assistant"""
    try:
        conversation = process_interaction()
        format_conversation(conversation)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()