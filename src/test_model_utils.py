# tests/test_model_utils.py
import pytest
from unittest.mock import patch, MagicMock
from modules.model_utils import get_available_models, initialize_model

def test_get_available_models():
    mock_result = MagicMock()
    mock_result.stdout = "NAME      ID        SIZE   MODIFIED\nllama3  abcdef123  1.2GB  1 day ago\n"
    
    with patch('subprocess.run', return_value=mock_result):
        models = get_available_models()
        assert models == ['llama3']

def test_initialize_model():
    with patch('modules.model_utils.Ollama') as mock_ollama:
        model = initialize_model('llama3')
        mock_ollama.assert_called_once_with(model='llama3')
        assert model is not None

def test_initialize_model_error():
    with patch('modules.model_utils.Ollama', side_effect=Exception("Model error")):
        model = initialize_model('invalid_model')
        assert model is None
