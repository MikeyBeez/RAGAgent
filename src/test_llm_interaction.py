from unittest.mock import MagicMock, patch
from modules import console_utils
from modules.llm_interaction import stream_llm_response

def test_stream_llm_response():
    mock_llm = MagicMock()
    mock_llm.stream.return_value = ["Hello", " world", "!"]
    mock_prompt_template = MagicMock()
    mock_console = MagicMock()
    mock_tts_queue = MagicMock()
    
    with patch('modules.console_utils.print_wrapped_text') as mock_print_wrapped_text:
        response = stream_llm_response(
            mock_llm, mock_prompt_template, "Hi", [], mock_console, mock_tts_queue, True
        )
        assert response == "Hello world!"
        assert mock_print_wrapped_text.call_count == 1
