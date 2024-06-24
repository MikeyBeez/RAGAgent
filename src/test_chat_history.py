import pytest
import json
import os
from modules.chat_history import add_to_history, save_interaction, get_memories, populate_chat_history, initialize_chat_history
from langchain_core.messages import HumanMessage, AIMessage

def test_add_to_history():
    chat_history = []
    user_input = "Test input"
    ai_response = "Test response"
    add_to_history(chat_history, user_input, ai_response)
    assert len(chat_history) == 2
    assert isinstance(chat_history[0], HumanMessage)
    assert isinstance(chat_history[1], AIMessage)
    assert chat_history[0].content == user_input
    assert chat_history[1].content == ai_response

def test_save_interaction():
    user_name = "TestUser"
    user_input = "Test input"
    ai_response = "Test response"
    save_interaction(user_name, user_input, ai_response)
    # We're just testing that the function runs without errors
    assert True

def test_get_memories():
    memories = get_memories('memories')
    assert isinstance(memories, list)
    assert len(memories) > 0
    assert 'user' in memories[0]
    assert 'agent' in memories[0]

def test_populate_chat_history():
    chat_history = []
    memories = [
        {"user": "Test input 1", "agent": "Test response 1"},
        {"user": "Test input 2", "agent": "Test response 2"}
    ]
    populate_chat_history(chat_history, memories)
    assert len(chat_history) == 4
    assert isinstance(chat_history[0], HumanMessage)
    assert isinstance(chat_history[1], AIMessage)
    assert chat_history[0].content == "Test input 1"
    assert chat_history[1].content == "Test response 1"

def test_initialize_chat_history():
    chat_history = initialize_chat_history('memories')
    assert isinstance(chat_history, list)
    assert len(chat_history) > 0
    assert isinstance(chat_history[0], HumanMessage)
    assert isinstance(chat_history[1], AIMessage)
