""" 
Author: Aniekan
"""

SYSTEM_PROMT = """You are an assistant to the recruiter.
You need to be very truthful since this information will be used in recruiting a person.
Return to me in json format, "position", "years_of_experience", "CTC", "notice_period", "educational_requirement" if available in the description, "years_of_experience", "CTC" should only show the lower and upper limit like (lower-upper).
If not mark it as none. Also, summarize the technical skills needed in the "technical_summary" field for the recruiter to be clear. Provide this technical summary as a list of points.
Summarize other needed skills like soft skills needed in the "soft_skills_summary" field as a list of points.
Also, add "must_have_skills" - these are the most important requirements from the job description, clearly mentioned as must have skills.
"location" is the place where the person will be posted. The output must be in JSON. I will use json.loads to convert it to a dictionary.
"""
REQUIREMENT_DESCRIPTION = """Position name: {job_title}, description of the job and requirements: {job_description}, Name of the client: {company},
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
            ('system', SYSTEM_PROMT),
            ('user', REQUIREMENT_DESCRIPTION)
        ]
        
        prompt_template = ChatPromptTemplate.from_messages(messages=messages)

        output_parser = StrOutputParser()
        chain = prompt_template | self.__llm | output_parser

        return chain.invoke(values)
    

if __name__ == '__main__':
    pass