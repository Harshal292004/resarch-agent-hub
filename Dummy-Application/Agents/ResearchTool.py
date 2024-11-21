import urllib.request as libreq
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import PyPDF2
import io
from crewai_tools import tool
class ResearchTool:
    def __init__(self):
        pass
    @staticmethod
    def load_document(file_path_url):
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
            
            num_pages=min(2,len(pdf_reader.pages))
            
            for page_num in range(num_pages):
                text+=pdf_reader.pages[page_num].extract_text()

            return text
        except requests.RequestException as e:
            print(f"Error occured:{e}")
            return None
        except Exception as e:
            print(f"Error occured in processing of pdf:{e}")
            return None 

        
        
    @staticmethod
    def arxiv_research_tool(author=None,title=None,category=None, sortBy="relevance", maxResults=1, sortOrder="ascending",extract_text=True, ) -> dict:
        """
        Advanced tool for searching and extracting research papers from ArXiv.

        Comprehensive search and extraction capabilities for academic research papers:
        - Flexible search across multiple parameters
        - Configurable search and extraction options

        Args:
            author (str, optional): Author name to search for. 
                Example: "Geoffrey Hinton"
            title (str, optional): Paper title or keywords. 
                Example: "Attention Is All You Need"
            category (str, optional): ArXiv research category. 
                Examples: "cs.AI", "math.ST", "physics.comp-ph"
            sortBy (str, optional): Sorting method for search results. 
                Choices: 
                - "relevance" (default)
                - "lastUpdatedDate"
                - "submittedDate"
            maxResults (int, optional): Maximum number of papers to retrieve. 
                Range: 1-4, Default: 1
            sortOrder (str, optional): Order of sorting. 
                Choices: 
                - "ascending" (default)
                - "descending"
            extract_text (bool, optional): Whether to extract full text from PDF. 
                Default: True

        Returns:
            dict: A dictionary containing:
            - 'papers': List of paper details
            - 'extracted_texts': List of extracted paper texts (if extract_text is True)

        Example:
            >>> result = ArxivResearchTool.arxiv_research_tool(
            ...     author="Yann LeCun", 
            ...     category="cs.AI", 
            ...     maxResults=2
            ... )
        """
        # Input validation
        if not any([author, title, category]):
            raise ValueError("At least one search parameter must be provided")

        # Validate and prepare search parameters
        search_parts = []
        if author:
            search_parts.append(f"au:{quote(author)}")
        if title:
            search_parts.append(f"ti:{quote(title)}")
        if category:
            search_parts.append(f"cat:{quote(category)}")

        search_query = "+AND+".join(search_parts)

        # Sanitize and validate inputs
        maxResults = min(max(1, maxResults), 4)
        sortOrder = sortOrder.lower() if sortOrder.lower() in ["ascending", "descending"] else "ascending"
        sortBy = sortBy if sortBy in ["relevance", "lastUpdatedDate", "submittedDate"] else "relevance"

        # Prepare result dictionary
        result = {
            "papers": [],
            "extracted_texts": []
        }

        try:
            # Construct ArXiv API URL
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": search_query,
                "max_results": maxResults,
                "sortBy": sortBy,
                "sortOrder": sortOrder,
            }
            url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            # Fetch XML data
            with libreq.urlopen(url, timeout=10) as response:
                xml_data = response.read().decode("utf-8")

            # Parse XML
            soup = BeautifulSoup(xml_data, "xml")
            entries = soup.find_all("entry")

            for entry in entries:
                paper_info = {
                    "title": entry.find("title").text.strip() if entry.find("title") else "No Title",
                    "authors": [a.text for a in entry.find_all("author")],
                    "summary": entry.find("summary").text.strip() if entry.find("summary") else "No Summary",
                    "pdf_link": entry.find("link", title="pdf")["href"] if entry.find("link", title="pdf") else None,
                }
                result["papers"].append(paper_info)

                # Text extraction if enabled
                if extract_text and paper_info['pdf_link']:
                    try:
                        text = ResearchTool.load_document(paper_info['pdf_link'])
                        result["extracted_texts"].append(text)
                    except Exception as extract_error:
                        print(f"Text extraction error for {paper_info['title']}: {str(extract_error)}")

        except Exception as e:
            print(f"Search Error :{e}")

        return result
    
    
    
    
        
# Additional dependencies to install:
# pip install requests beautifulsoup4 PyPDF2


result = ResearchTool.arxiv_research_tool(
    author="Yann LeCun", 
    category="cs.AI", 
    maxResults=2,
    extract_text=True
)


print("Title"+"-"*20+"Title")
# Access results
for paper in result['papers']:
    print(paper['title'])

print("Text"+"-"*20+"Text")
# Access extracted texts
for text in result['extracted_texts']:
    print(text[:500])  # First 500 characters

# Check for any errors
if result['errors']:
    print("Errors:", result['errors'])