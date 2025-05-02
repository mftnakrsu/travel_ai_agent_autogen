# chat/manager.py

from autogen import GroupChatManager
from chat.group import group_chat
from config.llm_config import llm_config  # bunu da sonra yaparız

travel_planner_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)
