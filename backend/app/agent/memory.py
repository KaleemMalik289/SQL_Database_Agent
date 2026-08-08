from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# In a production distributed environment, we would use RedisChatMessageHistory.
# For this scalable MVP, we will use an in-memory dictionary to map session IDs to their histories.
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates a ChatMessageHistory for a given session ID.
    This acts as the memory state store for RunnableWithMessageHistory.
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
