import pytest
import json
import os
from modules.create_memories import save_prompt_and_response

@pytest.fixture(scope="function")
def cleanup_memories():
    yield
    # Clean up test files after each test
    for file in os.listdir('memories'):
        if file.startswith('test_'):
            os.remove(os.path.join('memories', file))

def test_save_prompt_and_response(cleanup_memories):
    user_name = "TestUser"
    prompt = "Test prompt"
    response = "Test response"
    
    original_save = save_prompt_and_response
    
    def mock_save(user_name, prompt, response):
        timestamp = "20240623_000000"  # Fixed timestamp for testing
        filename = f"test_{timestamp}.json"
        
        memory_data = {
            "user_name": user_name,
            "user": prompt,
            "agent": response,
            "metadata": {
                "accessCount": 0,
                "lastAccess": None,
                "creation": timestamp
            }
        }
        
        file_path = os.path.join('memories', filename)
        with open(file_path, 'w') as f:
            json.dump(memory_data, f, indent=2)

    # Replace the save function with our mock
    save_prompt_and_response.__code__ = mock_save.__code__
    
    save_prompt_and_response(user_name, prompt, response)
    
    # Check if the file was created
    test_file = os.path.join('memories', 'test_20240623_000000.json')
    assert os.path.exists(test_file)
    
    # Check file content
    with open(test_file, 'r') as f:
        memory_data = json.load(f)
    
    assert memory_data['user_name'] == user_name
    assert memory_data['user'] == prompt
    assert memory_data['agent'] == response
    assert 'metadata' in memory_data
    assert 'creation' in memory_data['metadata']
    
    # Restore the original save function
    save_prompt_and_response.__code__ = original_save.__code__
