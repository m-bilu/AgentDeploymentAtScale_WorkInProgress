'''
This file contains all tools for edit_resume node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere import ChatCohere
from langchain.schema.runnable import RunnableSequence

def get_resume_edit_chain(llm: BaseChatModel | None = None) -> RunnableSequence:
    """
    Returns an LLMChain that edits a LaTeX resume using structured suggestions and a job description.
    
    Args:
        llm: Optional custom LLM instance (default: ChatCohere with temp=0)
    
    Returns:
        LLMChain
    """
    if llm == None:
        llm = ChatCohere(model="command-r-plus", temperature=0)

    prompt="""
        You are a LaTeX resume editing assistant.

        Given:
        1. A LaTeX resume document (as a string),
        2. A plain English job description,
        3. A list of structured improvement suggestions,

        Apply edits to the LaTeX string:
        - Reword or replace bullets as specified
        - Insert new bullet points under correct roles/sections
        - Add missing keywords subtly if possible
        - Preserve LaTeX formatting and syntax
        - Do NOT hallucinate new job roles or companies

        Return only the **edited LaTeX document** as a string (no markdown, no explanation).

        """

    resume_edit_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human",  "\n\nRESUME (LaTeX):{resume_latex}\n\nJOB DESCRIPTION:{jd_text}\n\nEDIT SUGGESTIONS:{suggestions_json}")
    ])
         
         

    chain = resume_edit_prompt | llm

    return chain
