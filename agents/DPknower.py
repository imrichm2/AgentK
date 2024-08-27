## 1. Imports:
##   ```python

from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
import config


## 2. System Prompt:
##   ```python	

system_prompt = """You are [agent_name], a ReAct agent that [description of agent's purpose].

   You have the following tools at your disposal:
   [List of tools and their brief descriptions]
   """


## 3. Tool Imports and List:
##   ```python
  
from tools.tool_1 import tool_1
from tools.tool_2 import tool_2
tools = [tool_1, tool_2]


## 4. Reasoning Function:
##   ```python
def reasoning(state: MessagesState):
       messages = state['messages']
       tooled_up_model = config.default_langchain_model.bind_tools(tools)
       response = tooled_up_model.invoke(messages)
       return {"messages": [response]}


## 5. Check for Tool Calls Function:
##   ```python

def check_for_tool_calls(state: MessagesState) -> Literal["tools", END]:
       messages = state['messages']
       last_message = messages[-1]
       if last_message.tool_calls:
           return "tools"
       return END
   

## 6. ToolNode and StateGraph:
##   ```python

acting = ToolNode(tools)
workflow = StateGraph(MessagesState)
workflow.add_node("reasoning", reasoning)
workflow.add_node("tools", acting)
workflow.set_entry_point("reasoning")
workflow.add_conditional_edges("reasoning", check_for_tool_calls)
workflow.add_edge("tools", 'reasoning')
graph = workflow.compile()
   

## 7. Main Agent Function:
##   ```python

def agent_name(task: str) -> str:
       """The agent has a RAGed understanding of Data Platforms and can provide information on the topic."""
       return graph.invoke(
           {"messages": [SystemMessage(system_prompt), HumanMessage(task)]}
       )
