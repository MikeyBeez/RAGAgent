# tests/test_chat_history.py
import pytest
from unittest.mock import patch
from modules.chat_history import add_to_history, save_interaction

def test_add_to_history():
    history = []
    add_to_history(history, "Hello", "Hi there!")
    assert len(history) == 2
    assert history[0].content == "Hello"
    assert history[1].content == "Hi there!"

def test_save_interaction():
    with patch('modules.chat_history.save_prompt_and_response') as mock_save:
        save_interaction("Hello", "Hi there!")
        mock_save.assert_called_once_with("Hello", "Hi there!")
