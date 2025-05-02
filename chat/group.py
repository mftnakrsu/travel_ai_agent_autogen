# chat/group.py

from autogen import GroupChat
from agents.destination_expert import get_agent as get_destination_expert
from agents.itinerary_creator import get_agent as get_itinerary_creator
from agents.budget_analyst import get_agent as get_budget_analyst
from agents.report_writer import get_agent as get_report_writer
from agents.user_proxy import get_agent as get_user_proxy
from config.llm_config import llm_config

from tools.tavily_search import tool as tavily_tool

# Agents
user_proxy = get_user_proxy(llm_config)
destination_expert = get_destination_expert(llm_config)
itinerary_creator = get_itinerary_creator(llm_config)
budget_analyst = get_budget_analyst(llm_config)
report_writer = get_report_writer(llm_config)

# Tool registration
#for agent in [user_proxy, destination_expert, itinerary_creator, budget_analyst]:
#    tavily_tool.register_tool(agent)


allowed_transitions = {
    user_proxy: [destination_expert, user_proxy],
    destination_expert: [itinerary_creator, user_proxy],
    itinerary_creator: [budget_analyst, user_proxy],
    budget_analyst: [report_writer, user_proxy],  # BUNUN OLDUĞUNDAN EMİN OL
    report_writer: [user_proxy],
}


# GroupChat object
group_chat = GroupChat(
    agents=[
        user_proxy,
        destination_expert,
        itinerary_creator,
        budget_analyst,
        report_writer,
    ],  
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    messages=[],
    max_round=5
)


