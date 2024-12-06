import urllib.request as libreq
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import PyPDF2
import io
from crewai_tools import tool
import json
from typing import Optional,Dict,List
from pydantic import BaseModel,ValidationError, Field
from typing import Type
from crewai_tools import BaseTool
import logging
from typing import ClassVar
logging.basicConfig(level=logging.DEBUG)
    
class ArxivResearchInput(BaseModel):
    author: str = Field("", description="Author name")
    title: str = Field("", description="Paper title")
    category: str = Field("cs.AI", description="ArXiv category")
    max_results: int = Field(10, description="Maximum number of results")
    sort_by: str = Field("lastUpdatedDate", description="Sort by field")
    sort_order: str = Field("descending", description="Sort order")
    extract_text: bool = Field(True, description="Extract text from papers")


class ArxivResearchTool(BaseTool):
    name: str = "arxiv_research_tool"
    description: str = "Search ArXiv database for academic research."
    args_schema: Type[BaseModel] = ArxivResearchInput

    # Initialize logger at the class level
    logger: ClassVar = logging.getLogger(__name__)

    def _run(self, **params):
        self.logger.debug(f"Received params: {params}")
        try:
            result = ResearchTool.arxiv_research_tool(params)
            self.logger.debug(f"Result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
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
    def arxiv_research_tool(params: Dict) -> Dict:
        try:
            author = params.get('author', '')
            title = params.get('title', '')
            category = params.get('category', 'cs.AI')
            max_results = params.get('max_results', 10)
            sort_by = params.get('sort_by', 'relevance')
            sort_order = params.get('sort_order', 'ascending')
            extract_text = params.get('extract_text', True)
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
            
            url = f"{base_url}?{'&'.join(f'{quote(str(k))}={quote(str(v))}' for k, v in params.items())}"

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