import os
from autogen.agentchat.contrib.web_surfer import WebSurferAgent
import streamlit as st
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen.tools import Tool
from autogen import register_function, ConversableAgent
from typing import Annotated
from pydantic import BaseModel, Field
from tavily import TavilyClient
from autogen import register_function
from typing import List
import tempfile
import re
import matplotlib.pyplot as plt



load_dotenv()

def tavily_search(
    query: Annotated[str, "The search query string"],
    max_results: Annotated[int, "Maximum results"] = 3,
    search_depth: Annotated[str, "basic or advanced"] = "basic"
) -> List[dict]:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query=query, max_results=max_results, search_depth=search_depth)
    
    return [
        {
            "title": r["title"],
            "url": r["url"],
            "summary": r["content"][:200] + "..."
        }
        for r in response.get("results", [])
    ]

tavily_tool = Tool(
    name="tavily_search",
    description="Search the internet using Tavily API for up-to-date travel information.",
    func_or_tool=tavily_search  
    
)
  
st.set_page_config(page_title="Travel Planner AI", page_icon="🌍", layout="centered")

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]
}


user_proxy = ConversableAgent(
    name="User_Proxy_Agent",
    system_message="You are a user proxy agent.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

destination_expert = ConversableAgent(
    name="Destination_Expert_Agent",
    system_message="""
                    You are the Destination Expert, a specialist in global travel destinations. 

                Your responsibilities include:
                    1. Analyzing user preferences (e.g., climate, activities, culture) to suggest suitable destinations.
                    2. Providing detailed information about recommended locations, including attractions, best times to visit, and local customs.
                    3. Consider factors like seasonality, events, and travel advisories in your recommendations.
                    4. SELECT 1 destination that you think is the best choice
                    5. DO NOT GIVE AN ITINERARY
                    Base your suggestions on a wide range of global destinations and current travel trends.
                    Format your response with a clear "DESTINATION SUMMARY" header.
                    You are expected to read tool outputs and generate a natural language response using those results.

    """,
    llm_config=llm_config,
    human_input_mode="NEVER",
)

itinerary_creator = ConversableAgent(
    name="Itinerary_Creator_Agent",
    system_message="""
                    You are the Itinerary Creator, responsible for crafting detailed travel itineraries.

                    You may use the `tavily_search` tool to find up-to-date information about points of interest, opening hours, and local activities.
                    You are expected to read tool outputs and generate a natural language response using those results.

                    Your responsibilities include:
                    1. Creating day-by-day schedules.
                    2. Aligning the plan with the suggested destination and user's interests.
                    3. Using insights from the tool when selecting attractions or planning timing.
                    4. Avoid repetition and ensure logical travel pacing.

                    Format your response with a clear "ITINERARY" header.
                    You are expected to read tool outputs and generate a natural language response using those results.

                    """,
    llm_config=llm_config,
    human_input_mode="NEVER",
)

budget_analyst = ConversableAgent(
    name="Budget_Analyst_Agent",
    system_message="""
                    You are the Budget Analyst, an expert in travel budgeting.

                    You may use the `tavily_search` tool to retrieve accurate and recent price information (transportation, accommodation, activities).

                    Your responsibilities include:
                    1. Providing cost estimates for all aspects of the trip.
                    2. Suggesting ways to optimize spending.
                    3. Referencing tool results in cost justifications.
                    4. Breaking down the budget clearly.

                    Format your response with a clear "BUDGET" header.
                    You are expected to read tool outputs and generate a natural language response using those results.

                    """
,
    llm_config=llm_config,
    human_input_mode="NEVER",
)

report_writer = ConversableAgent(
    name="Report_Writer_Agent",
    system_message="""
                    You are the Report Compiler agent, tasked with creating a comprehensive travel report based on the outputs of the following agents:

                    Destination_Expert_Agent: Provides a recommended destination.
                    Itinerary_Creator_Agent: Creates a detailed itinerary for the chosen destination.
                    Budget_Analyst_Agent: Analyzes the budget and provides cost estimates for the trip.

                    Your Task:

                    Gather Information: Collect the outputs from each agent.
                    Structure the Report: Organize the information into a clear and concise report format.
                    Create a Summary: Provide a brief overview of the recommended destination, itinerary, and budget.
                    Highlight Key Points: Emphasize the most important aspects of the trip, such as unique experiences or cost-saving tips.

                    Report Structure:

                    Introduction: A brief welcome and overview of the trip.
                    Destination Summary: Details from the Destination_Expert_Agent, including the chosen destination and reasons for recommendation.
                    Cultural Tips: Information on local customs, etiquette, and cultural norms.
                    Itinerary: The detailed itinerary created by the Itinerary_Creator_Agent, including day-by-day activities and accommodations.
                    Transportation: A summary of transport modes found at the destination and their prices
                    Budget Breakdown: The cost estimates and financial advice from the Budget_Analyst_Agent.
                    Packing List: List of essential and optional items to pack for your trip.
                    Conclusion: A summary of the trip and any final recommendations or suggestions.
                    You are expected to read tool outputs and generate a natural language response using those results.


    """,
    llm_config=llm_config,
    human_input_mode="NEVER",
)



#TOOL USAGE - THERE IS A PROBLEM, if i use tool, just return raw tool data didnt mix with llm response
#tavily_tool.register_for_llm(user_proxy)
#tavily_tool.register_for_llm(report_writer)

#for agent in [destination_expert, itinerary_creator, budget_analyst]:
    #tavily_tool.register_for_llm(agent)
    #tavily_tool.register_for_execution(agent)

#for agent in [user_proxy, report_writer]:
 #   tavily_tool.register_for_llm(agent)
  #  tavily_tool.register_for_execution(agent)


allowed_transitions = {
    user_proxy: [destination_expert,user_proxy],
    destination_expert: [itinerary_creator,user_proxy],
    itinerary_creator: [budget_analyst,user_proxy],
    budget_analyst: [report_writer,user_proxy], 
    report_writer: [user_proxy],
}

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
    max_round=5,
)

travel_planner_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)

st.title("🌍 Travel Planner AI Assistant")
st.subheader("Plan your perfect trip with smart AI agents!")

user_input = st.text_input("Tell us about your dream trip:", placeholder="e.g., Europe, 7 days, love beaches and history")

if st.button("Plan My Trip ✈️"):
    if user_input.strip() == "":
        st.warning("Please enter your trip details.")
    else:
        with st.spinner("Planning your dream trip... 🏋️✨"):
            try:
                chat_result = user_proxy.initiate_chat(
                    travel_planner_manager,
                    message=user_input,
                    summary_method="last_msg",
                )

                # --- AGENT CHAT HISTORY ---
                st.subheader("💛 Agent Chat History")
                for idx, msg in enumerate(chat_result.chat_history):
                    role = msg.get("name", "Unknown Agent")
                    content = msg.get("content", "")

                    if role and content:
                        with st.expander(f"{idx+1}. {role}"):
                            st.markdown(content)

                # --- TOOL USAGE LOG ---
                st.subheader("🛠️ Agent Tool Usage")

                tool_calls = [
                    msg for msg in chat_result.chat_history
                    if msg.get("role") == "tool" or (
                        isinstance(msg.get("content"), str) and "Response from calling tool" in msg["content"]
                    )
                ]

                if not tool_calls:
                    st.info("No tools were used during this planning.")
                else:
                    for idx, msg in enumerate(tool_calls):
                        role = msg.get("name", "Unknown Agent")
                        content = msg.get("content", "")
                        st.markdown(f"**{idx+1}. `{role}` used `tavily_search`:**")
                        st.code(content if isinstance(content, str) else str(content))


                # --- FINAL REPORT ---
                report = next(
                    msg["content"]
                    for msg in chat_result.chat_history
                    if msg.get("name") == "Report_Writer_Agent"
                )

                st.success("Here is your final travel plan! 🌍")
                st.info(report)

                # Report içeriğini dosyaya yaz
                with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as f:
                    f.write(report)
                    tmp_path = f.name

                # İndirme butonu
                with open(tmp_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Itinerary as TXT",
                        data=f,
                        file_name="travel_plan.txt",
                        mime="text/plain",
                                    )

            except Exception as e:
                st.error(f"An error occurred while planning your trip: {str(e)}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Autogen + Streamlit")