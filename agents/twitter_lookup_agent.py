import os
from dotenv import load_dotenv

from tools.tools import get_profile_url_travily_twitter

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub


def lookup(name: str) -> str:
    """
    Lookup information about a person on LinkedIn.
    """
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo"
    )
    template = """
    Act as an expert Internet researcher. Given the name {name_of_person}, I want you to find a link to their twitter profile page and extract the username from it.
    Your final answer must contain only the person's twitter username.
    """

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template=template
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 twitter profile page",
            func=get_profile_url_travily_twitter,
            description="Useful when you need to get the Twitter page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )
    # Orchestrator for agent execution.
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

    # return "https://www.linkedin.com/in/ashutosh1995/"


if __name__ == "__main__":
    linkedin_url = lookup(name="Ashutosh Maheshwari awscloudengineer Nutanix")
    print(linkedin_url)
