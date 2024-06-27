# test_process_prompt.py

import unittest
from unittest.mock import patch, MagicMock
from modules.process_prompt import ProcessPrompt

class TestProcessPrompt(unittest.TestCase):
    def setUp(self):
        self.processor = ProcessPrompt()
        self.mock_chat_history = MagicMock()

    def test_process_input_command(self):
        result = self.processor.process_input("/help", self.mock_chat_history, False)
        self.assertEqual(result["type"], "command")
        self.assertIn("message", result["content"])
        self.assertTrue(result["content"]["is_panel"])

    def test_process_input_search(self):
        with patch('modules.ddg_search.run_search', return_value="Mock search results"):
            result = self.processor.process_input("/search test query", self.mock_chat_history, False)
            self.assertEqual(result["type"], "prompt")
            self.assertIn("Search results for 'test query'", result["content"])

    def test_process_input_memory(self):
        self.mock_chat_history.search_memories.return_value = "Mock memory results"
        result = self.processor.process_input("/memory test query", self.mock_chat_history, False)
        self.assertEqual(result["type"], "prompt")
        self.assertIn("Relevant memories: Mock memory results", result["content"])

    def test_process_input_normal_prompt(self):
        result = self.processor.process_input("Hello, Otto!", self.mock_chat_history, False)
        self.assertEqual(result, {"type": "prompt", "content": "Hello, Otto!"})

    def test_handle_command_quit(self):
        result = self.processor.handle_command("/quit", self.mock_chat_history, False)
        self.assertEqual(result, {"type": "command", "content": "QUIT"})

    def test_handle_command_talk(self):
        result = self.processor.handle_command("/talk", self.mock_chat_history, False)
        self.assertEqual(result["content"]["tts_enabled"], True)

    def test_handle_command_notalk(self):
        result = self.processor.handle_command("/notalk", self.mock_chat_history, False)
        self.assertEqual(result["content"]["tts_enabled"], False)

if __name__ == '__main__':
    unittest.main()
