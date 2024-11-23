import urllib.request as libreq
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import PyPDF2
import io
from crewai_tools import tool
import json
from typing import Optional,Dict
from pydantic import BaseModel,ValidationError, Field
from typing import Type
from crewai_tools import BaseTool


class ArxivResearchInput(BaseModel):
    """Input schema for arxiv tool"""
    argument: str = Field(
        description='JSON string containing search parameters',
        example='{"author": "Alan Turing", "title": "Computing Machinery", "category": "cs.AI", "max_results": 4, "sort_by": "relevance", "sort_order": "descending", "extract_text": true}'
    )

class ArxivResearchTool(BaseTool):
    name: str = 'arxiv_research_tool'
    description: str = """Useful to search the arxiv academic database and return relevant research papers.
    The argument must be a JSON string with the following structure:
    {
        "author": "string",
        "title": "string",
        "category": "string",
        "max_results": number,
        "sort_by": "string",
        "sort_order": "string",
        "extract_text": boolean
    }
    """
    args_schema: Type[BaseModel] = ArxivResearchInput

    def _run(self, argument: str) -> Dict:
        try:
            # Parse the JSON string into a dictionary
            params = json.loads(argument)
            
            # Validate required fields
            required_fields = ['author', 'title', 'category', 'max_results', 'sort_by', 'sort_order', 'extract_text']
            for field in required_fields:
                if field not in params:
                    raise ValueError(f"Missing required field: {field}")
            
            # Call the actual research implementation
            return ResearchTool.arxiv_research_tool(argument)
            
        except json.JSONDecodeError:
            return {"error": "Invalid JSON string provided"}
        except Exception as e:
            return {"error": str(e)}


class ResearchTool:
    def __init__(self):
        pass
    
        
    @staticmethod
    @tool("load_document")
    def load_document(file_path_url: str) -> str:
        """Load and extract text from PDF documents."""
        try:
            response = requests.get(file_path_url)
            response.raise_for_status()
            
            pdf_file_obj = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            
            text = ""
            num_pages = min(4, len(pdf_reader.pages))
            
            for page_num in range(num_pages):
                text += pdf_reader.pages[page_num].extract_text()

            return text
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
 
    @staticmethod
    def arxiv_research_tool(
        payload
    ) -> Dict:
        """Useful to search the arxiv academic data base  and return relevant research papaers 
        :param payload: str, a string representation of dictionary containing the following keys:

        author: str,the author to search for ,
        title: str,the title of the research paper ,
        category: str,the category of the subject of research,
        max_results: int ,number of papers ,
        sort_by: str, select from "relevance", "lastUpdatedDate", "submittedDate",
        sort_order: str, "ascending" or "descending",
        extract_text: bool,  "True"
        
        example payload:
        {
            "author" : "Geoffry Hinton",
            "title": "Attention is all you need",
            "category":"cs.AI",
            "max_results":  1,
            "sort_by":"relevance",
            "sort_order":"ascending",
            "extract_text":"True"
        }
        """
        """Search and extract research papers from ArXiv."""
        try:
            author = json.loads(payload)['author']
            title = json.loads(payload)['title']
            category=json.loads(payload)['category']
            max_results=json.loads(payload)['max_results']
            sort_by=json.loads(payload)['sort_by']
            sort_order=json.loads(payload)['sort_order']
            extract_text=json.loads(payload)['extract_text']
            # Input validation
            if not author and not title and not category:
                 category = "cs.AI"
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
                    text = ResearchTool.extract_text(paper_info['pdf_link'])
                    results["extracted_texts"].append(text)

            return results

        except Exception as e:
            return {"error": str(e), "papers": [], "extracted_texts": []}

    
    @staticmethod
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