# IMPORTANT NOTE: This test file uses the 'unittest' framework as requested.
# However, due to the strict import restrictions in the current execution environment
# (disallowing 'unittest', 'pytest', 'sys', 'io', 'contextlib'), this file
# CANNOT BE EXECUTED DIRECTLY within this environment.
# It is provided to fulfill the task requirement of generating a test file,
# assuming a standard Python environment where 'unittest' is available.

import unittest
import json
# Assuming json_generate_example.py is in the same directory or accessible via PYTHONPATH
from json_generate_example import run_json_generate_example

class TestJsonGenerateExample(unittest.TestCase):

    def test_successful_json_generation(self):
        """
        Tests that the run_json_generate_example function correctly generates
        the expected JSON string and character count.
        """
        expected_json_string = '{"name":"Test Name","value":"Test Value","enabled":"true"}'
        expected_char_count = len(expected_json_string)

        # Call the function that performs the COBOL-to-Python conversion logic
        # This function also prints to stdout, but we are primarily testing its return values.
        generated_json, char_count = run_json_generate_example()

        # Assert the returned values
        self.assertEqual(generated_json, expected_json_string, "Generated JSON string does not match expected.")
        self.assertEqual(char_count, expected_char_count, "Generated JSON character count does not match expected.")

    # Note on error handling tests:
    # For this simple example, it's not straightforward to make json.dumps fail
    # with valid dictionary input without introducing complex mocking (which might
    # involve disallowed imports or go beyond the scope of a direct COBOL conversion).
    # The `try-except` block is present in `run_json_generate_example`, and its
    # successful execution is implicitly tested by `test_successful_json_generation`.
    # If a scenario existed where invalid data could be passed to `json.dumps`
    # that would cause a JSON encoding error, a separate test case would be added
    # to verify the error path (e.g., by passing a non-serializable object).
    # In a standard unittest setup, one might use `unittest.mock.patch` to simulate
    # an exception from `json.dumps`, but `unittest.mock` is also not available here.

if __name__ == '__main__':
    # This block allows the test file to be run directly using `python -m unittest test_json_generate_example.py`
    # in a standard Python environment.
    unittest.main()