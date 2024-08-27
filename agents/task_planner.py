from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph, MessagesState

import config

system_prompt = """You are task_planner, a ReAct agent that breaks down complex tasks into smaller, manageable subtasks.

Your role is to analyze a given task, understand its complexity, and create a structured plan with subtasks that can be easily executed.
"""

def reasoning(state: MessagesState):
    print("task_planner is thinking...")
    messages = state['messages']
    response = config.default_langchain_model.invoke(messages)
    return {"messages": [response]}

def check_for_completion(state: MessagesState) -> Literal["reasoning", END]:
    messages = state['messages']
    last_message = messages[-1]
    
    if "TASK BREAKDOWN COMPLETE" in last_message.content:
        return END
    
    return "reasoning"

workflow = StateGraph(MessagesState)
workflow.add_node("reasoning", reasoning)
workflow.set_entry_point("reasoning")
workflow.add_conditional_edges(
    "reasoning",
    check_for_completion,
)

graph = workflow.compile()

def task_planner(task: str) -> str:
    """Breaks down a complex task into smaller subtasks."""
    result = graph.invoke(
        {"messages": [
            SystemMessage(system_prompt),
            HumanMessage(f"""
            Please break down the following task into smaller, manageable subtasks:
            
            {task}
            
            Provide a numbered list of subtasks, with brief explanations if necessary.
            When you're finished, end your response with 'TASK BREAKDOWN COMPLETE'.
            """)
        ]}
    )
    return result['messages'][-1].content