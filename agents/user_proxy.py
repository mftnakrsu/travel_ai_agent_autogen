from autogen import ConversableAgent

def get_agent(llm_config):
    return ConversableAgent(
        name="User_Proxy_Agent",
        system_message="You are a user proxy agent. You represent the human user in this multi-agent conversation.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
