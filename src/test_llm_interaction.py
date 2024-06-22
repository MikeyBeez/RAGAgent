# tests/test_llm_interaction.py
import pytest
from unittest.mock import MagicMock
from modules.llm_interaction import setup_prompt_template, stream_llm_response

def test_setup_prompt_template():
    template = setup_prompt_template()
    assert template is not None

def test_stream_llm_response():
    mock_llm = MagicMock()
    mock_llm.stream.return_value = ["Hello", " world", "!"]
    
    mock_prompt_template = MagicMock()
    mock_console = MagicMock()
    mock_tts_queue = MagicMock()
    
    response = stream_llm_response(
        mock_llm, mock_prompt_template, "Hi", [], mock_console, mock_tts_queue, True
    )
    
    assert response == "Hello world!"
    assert mock_console.print_wrapped_text.call_count == 1
    assert mock_tts_queue.put.call_count == 1

