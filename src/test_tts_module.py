# tests/test_tts_module.py
import pytest
from unittest.mock import patch, MagicMock
from modules.tts_module import speak_text, tts_worker, setup_tts_queue, start_tts_thread, cleanup_tts
import time

def test_speak_text():
    with patch('subprocess.run') as mock_run, patch('time.sleep') as mock_sleep:
        speak_text("Hello, world!")
        mock_sleep.assert_called_once_with(0.5)
        mock_run.assert_called_once_with(['say', "Hello, world!"], check=True)

def test_tts_worker():
    mock_queue = MagicMock()
    mock_queue.get.side_effect = ["Hello", "World", None]
    
    with patch('modules.tts_module.speak_text') as mock_speak:
        tts_worker(mock_queue)
        assert mock_speak.call_count == 2
        mock_speak.assert_any_call("Hello")
        mock_speak.assert_any_call("World")
        assert mock_queue.task_done.call_count == 2

def test_setup_tts_queue():
    queue = setup_tts_queue()
    assert queue.empty()

@patch('threading.Thread')
def test_start_tts_thread(mock_thread):
    mock_queue = MagicMock()
    mock_thread_instance = MagicMock()
    mock_thread.return_value = mock_thread_instance

    thread = start_tts_thread(mock_queue)

    mock_thread.assert_called_once_with(target=tts_worker, args=(mock_queue,))
    mock_thread_instance.start.assert_called_once()
    assert thread == mock_thread_instance

def test_cleanup_tts():
    mock_queue = MagicMock()
    mock_thread = MagicMock()
    cleanup_tts(mock_queue, mock_thread)
    mock_queue.put.assert_called_once_with(None)
    mock_thread.join.assert_called_once()
