""" 
Author: Aniekan
"""

JD_SYSTEM_PROMT = """You are an assistant to the recruiter.
You need to be very truthful since this information will be used in recruiting a person.
Return to me in json format, "position", "years_of_experience", "CTC", "notice_period", "educational_requirement" if available in the description, "years_of_experience", "CTC" should only show the lower and upper limit like (lower-upper).
If not mark it as none. Also, summarize the technical skills needed in the "technical_summary" field for the recruiter to be clear. Provide this technical summary as a list of points.
Summarize other needed skills like soft skills needed in the "soft_skills_summary" field as a list of points.
Also, add "must_have_skills" - these are the most important requirements from the job description, clearly mentioned as must have skills.
"location" is the place where the person will be posted. The output must be in JSON. I will use json.loads to convert it to a dictionary.
"""
JD_REQUIREMENT_DESCRIPTION = """Position name: {job_title}, description of the job and requirements: {job_description}, Name of the client: {company},
Minimum experience required: {min_experience}, Maximum experience required: {max_experience}, Minimum budget for the salart p.a: {salary_min}, Maximum budget for the salart p.a: {salary_max},
Location of the job: {location}, Notice period: {notice_period}, Mandatory or Must have skills required for this job: {mandatory_skills}.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class JobRequirementProcessor:

    TEMPERATURE = 1
    MAX_TOKENS = 2000
    MODEL = 'gpt-3.5-turbo-16k'

    def __init__(self) -> None:
        self.__llm = ChatOpenAI(model=self.MODEL, temperature=self.TEMPERATURE, max_tokens=self.MAX_TOKENS)

    def process_reqirement(self, values):
        """
        Generates a response based on requirement description and system prompt using the OpenAI API.

        Returns:
        - str: The generated text based on the `REQUIREMENT_DESCRIPTION`.
        """

        messages = [
            ('system', JD_SYSTEM_PROMT),
            ('user', JD_REQUIREMENT_DESCRIPTION)
        ]
        
        prompt_template = ChatPromptTemplate.from_messages(messages=messages)

        output_parser = StrOutputParser()
        chain = prompt_template | self.__llm | output_parser

        return chain.invoke(values)


RS_SYSTEM_PROMT = """Read the given resume and extract information corresponding to the keys:
 "name_of_candidate" which stores the candidate name,
 "mobile_number" contains the mobile number,
 "email_id" records the email id of the candidate,
 total years of experience is stored in "years_of_experience",
 "education" refers to the candidate's most recent or highest academic degree,
 last university/school/college attended by the candidate is given by "university",
 "linkedin_profile" contains the linkedin profile,
 record all the technical skills in "technical_skills",
 "years_of_jobs" showcases the years spent in different jobs,
 years spent in the current organization is given by "year_in_current_position",
 "Present_Organization" denotes name of the present organization and "summay".
 For "technical_skills", provide a summary of the programming languages, libraries, and frameworks the candidate has experience with as a list,
 "years_of_jobs" is a list of job durations, e.g., ["2012-current","2010-2012", (June 22, 2022 - Present)].
 "year_in_current_position" indicates the duration in their current job role integer. Present year is 2023.
 "years_of_experience" is the sum of years spent in all jobs including the current one.
 Round off the year to the upper ceiling. So, if it is 3 months, round it off to 1 year.
 Summarize the resume in approximately 100 words for the "summary" field.
 The final output must be in JSON
"""


import os
import shutil
import tiktoken
import textract
from docx import Document
from  PyPDF2 import PdfReader
from langchain_core.messages import SystemMessage, HumanMessage

class ResumeProcessor:

    __UPLOAD_DIR = 'docs'

    def get_resume_summary(self, resume_data:str):
        messages = [
            SystemMessage(content=RS_SYSTEM_PROMT),
            HumanMessage(content=resume_data)
        ]

        llm = ChatOpenAI(model='gpt-3.5-turbo-16k', max_tokens=12000)
        response = llm.invoke(messages)

        return response.content

    def load_file_and_save(self, file_path:str):
        filename = os.path.basename(file_path)
        resume_path = os.path.join(self.__UPLOAD_DIR, filename)
        shutil.copyfile(file_path, resume_path)         

        return resume_path

    def read_document(self, file_path:str):
        _, ext = os.path.splitext(file_path)
        
        match ext:
            case '.pdf':
                return extract_text_from_pdf(file_path)
            case '.docx':
                return extract_text_from_docx(file_path)
            case '.doc': 
                return extract_text_from_doc(file_path)
            case _: 
                raise ValueError(f'Unsupported file type: {ext}')
            
    def check_and_trim(self, resume_text, max_tokens=1500):
        encoding = tiktoken.get_encoding('cl100k_base')
        tokens = encoding.encode(resume_text)
        old_len = len(tokens)

        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
            resume_text = encoding.decode(tokens)

        return resume_text, old_len, len(tokens)


def extract_text_from_pdf(pdf_path:str):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    return text  

def extract_text_from_doc(doc_path:str):
    text = textract.process(doc_path).decode()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    
    return text


if __name__ == '__main__':
    processor = ResumeProcessor()

    data = processor.read_document()
    data, _, _ = processor.check_and_trim(data)
    print(processor.get_resume_summary(data))
    pass
    