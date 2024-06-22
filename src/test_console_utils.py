# tests/test_console_utils.py
import pytest
from unittest.mock import patch, MagicMock
from modules.console_utils import setup_console, print_wrapped_text, get_user_name, get_model_choice, get_user_input, print_command_result, print_copy_instruction

def test_setup_console():
    console = setup_console()
    assert console is not None

def test_print_wrapped_text():
    mock_console = MagicMock()
    print_wrapped_text(mock_console, "Hello, world!")
    mock_console.print.assert_called_once()

def test_get_user_name():
    mock_console = MagicMock()
    mock_console.input.return_value = "Alice"
    assert get_user_name(mock_console) == "Alice"

def test_get_model_choice():
    mock_console = MagicMock()
    mock_console.input.return_value = "llama3"
    assert get_model_choice(mock_console, ["llama3", "gpt2"]) == "llama3"

def test_get_user_input():
    mock_console = MagicMock()
    mock_console.input.return_value = "Hello, AI!"
    assert get_user_input(mock_console, "User") == "Hello, AI!"

def test_print_command_result():
    mock_console = MagicMock()
    print_command_result(mock_console, {"message": "Command executed"})
    mock_console.print.assert_called_once()

def test_print_copy_instruction():
    mock_console = MagicMock()
    print_copy_instruction(mock_console)
    mock_console.print.assert_called_once()
