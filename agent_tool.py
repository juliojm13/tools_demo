import os
import requests

from dotenv import load_dotenv
from typing import Optional, Type

from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


class SearchInput(BaseModel):
    """
    City input for event search tool
    """
    city: str = Field(description="the name of the user's city")


class EventSearchTool(BaseTool):
    """
    Tool for searching events in the city
    """
    name = "event_search"
    description = "useful when user asks about some events in the city"
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self,
            city: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> list:
        """
        :param city: the name of the city
        :param run_manager: the manager for tool run
        :return: list of events
        """
        events_api = ('https://api.seatgeek.com/2/events?venue.city='
                      f'{city}'
                      f'&client_id={os.getenv("CLIENT_ID")}'
                      f'&client_secret={os.getenv("CLIENT_SECRET")}')
        events_list = []
        response = requests.get(events_api)
        for event in response.json()['events']:
            event_dict = {
                'date': event['datetime_utc'],
                'event_name': event['short_title']
            }
            events_list.append(event_dict)
        return events_list


class MessageInput(BaseModel):
    """
    Message input for telegram message tool
    """
    message: str = Field(description="the message for telegram user")


class SendTelegramMessageTool(BaseTool):
    """
    Tool for sending message to telegram chat
    """
    name = "send_telegram"
    description = "useful when user asks to send information to telegram chat"
    args_schema: Type[BaseModel] = MessageInput

    def _run(
            self,
            message: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        :param message: the message for telegram user
        :param run_manager: the manager for tool run
        :return: the message for telegram user
        """
        token = os.getenv('BOT_TOKEN')
        chat_id = os.getenv('CHAT_ID')
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        requests.post(
            url=url,
            json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
            }
        )
        return message


# Create a list of tools
tools = [EventSearchTool(), SendTelegramMessageTool()]
# Create an agent executor
llm = ChatOpenAI(
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model="gpt-3.5-turbo-0125",
    temperature=0
)
# Prompt that will be used in agent
prompt = hub.pull("hwchase17/openai-functions-agent")
# Creating the agent
agent = create_tool_calling_agent(llm, tools, prompt)
# Creating the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoking the agent
# agent_executor.invoke({"input": "Send me to telegram what events are there in London?"})
agent_executor.invoke({"input": input("Ask something to the LLM: ")})
