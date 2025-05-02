# main.py

import streamlit as st
from agents.user_proxy import get_agent as get_user_proxy
from chat.manager import travel_planner_manager
from config.llm_config import llm_config
import traceback



st.set_page_config(page_title="Travel Planner AI", page_icon="🌍", layout="centered")

user_proxy = get_user_proxy(llm_config=llm_config)

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
                report_msgs = [
                    msg["content"]
                    for msg in chat_result.chat_history
                    if msg.get("name") == "Report_Writer_Agent"
                ]

                if report_msgs:
                    st.success("Here is your final travel plan! 🌍")
                    st.info(report_msgs[-1])  # en sonuncuyu göster
                else:
                    st.error("⚠️ Report could not be generated. The final agent might not have responded.")

            except Exception as e:
                st.error("An error occurred while planning your trip.")
                st.code(traceback.format_exc())  # tüm traceback'i yaz

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Autogen + Streamlit")
