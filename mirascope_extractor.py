from mirascope.openai import OpenAIExtractor
from mirascope.gemini import GeminiExtractor
from mirascope.groq import GroqExtractor

from pydantic import FilePath, BaseModel
from typing import List, Type


class TaskDetails(BaseModel):
    seller_company_name: str
    receiver_company: str
    description: List[str]
    invoice_date: str
    invoice_number: str
    net_amount : float
    vat_amount : float
    vat_rate: str
    total_amount : float

class TaskExtractor(OpenAIExtractor[TaskDetails]):
    extract_schema: Type[TaskDetails] = TaskDetails
    prompt_template = """
    Extract the invoice details from the following invoice:
    {invoice}
    """
    invoice: str

def extractor(text):
    task_details = TaskExtractor(invoice=text).extract()
    assert isinstance(task_details, TaskDetails)
    return task_details

