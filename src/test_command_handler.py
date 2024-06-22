# tests/test_command_handler.py
import pytest
import pyperclip
from unittest.mock import patch
from modules.command_handler import is_command, handle_command

def test_is_command():
    assert is_command("/talk") == True
    assert is_command("Hello") == False

def test_handle_command_quit():
    assert handle_command("/quit", [], False) == "QUIT"

def test_handle_command_talk():
    result = handle_command("/talk", [], False)
    assert result["tts_enabled"] == True
    assert "enabled" in result["message"]

def test_handle_command_notalk():
    result = handle_command("/notalk", [], True)
    assert result["tts_enabled"] == False
    assert "disabled" in result["message"]

def test_handle_command_copy():
    with patch('pyperclip.copy') as mock_copy:
        history = [type('obj', (object,), {'content': 'Hello'}), 
                   type('obj', (object,), {'content': 'Hi there!'})]
        result = handle_command("/copy", history, False)
        assert "Copied" in result["message"]
        mock_copy.assert_called_once()

def test_handle_unknown_command():
    result = handle_command("/unknown", [], False)
    assert "Unknown command" in result["message"]
