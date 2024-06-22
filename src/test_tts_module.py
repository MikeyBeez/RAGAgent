# tests/test_tts_module.py
import pytest
from unittest.mock import patch, MagicMock
from modules.tts_module import speak_text, tts_worker, setup_tts_queue, start_tts_thread, cleanup_tts

def test_speak_text():
    with patch('subprocess.run') as mock_run:
        speak_text("Hello, world!")
        mock_run.assert_called_once_with(['say', "Hello, world!"], check=True)

def test_tts_worker():
    mock_queue = MagicMock()
    mock_queue.get.side_effect = ["Hello", "World", None]
    
    with patch('modules.tts_module.speak_text') as mock_speak:
        tts_worker(mock_queue)
        assert mock_speak.call_count == 2
        mock_speak.assert_any_call("Hello")
        mock_speak.assert_any_call("World")

def test_setup_tts_queue():
    queue = setup_tts_queue()
    assert queue.empty()

def test_start_tts_thread():
    mock_queue = MagicMock()
    thread = start_tts_thread(mock_queue)
    assert thread.is_alive()
    cleanup_tts(mock_queue, thread)

def test_cleanup_tts():
    mock_queue = MagicMock()
    mock_thread = MagicMock()
    cleanup_tts(mock_queue, mock_thread)
    mock_queue.put.assert_called_once_with(None)
    mock_thread.join.assert_called_once()
