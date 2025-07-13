import json

# Re-include the application code for testing purposes
class WsRecord:
    def __init__(self):
        self._ws_record_name = "          "
        self._ws_record_value = "          "
        self._ws_record_blank = "          "
        self._ws_record_flag = "false"

    @property
    def ws_record_name(self):
        return self._ws_record_name

    @ws_record_name.setter
    def ws_record_name(self, value):
        self._ws_record_name = value.ljust(10)[:10]

    @property
    def ws_record_value(self):
        return self._ws_record_value

    @ws_record_value.setter
    def ws_record_value(self, value):
        self._ws_record_value = value.ljust(10)[:10]

    @property
    def ws_record_blank(self):
        return self._ws_record_blank

    @ws_record_blank.setter
    def ws_record_blank(self, value):
        self._ws_record_blank = value.ljust(10)[:10]

    @property
    def ws_record_flag(self):
        return self._ws_record_flag

    @ws_record_flag.setter
    def ws_record_flag(self, value):
        if value in ["true", "false"]:
            self._ws_record_flag = value.ljust(5)[:5]
        else:
            raise ValueError("ws_record_flag must be 'true' or 'false'")

    def set_ws_record_flag_enabled(self):
        self._ws_record_flag = "true ".ljust(5)[:5]

    def set_ws_record_flag_disabled(self):
        self._ws_record_flag = "false".ljust(5)[:5]

def generate_json_from_record(record: WsRecord) -> str:
    name = record.ws_record_name.strip()
    value = record.ws_record_value.strip()
    enabled = True if record._ws_record_flag.strip() == "true" else False

    json_data = {
        "name": name,
        "value": value,
        "enabled": enabled
    }
    return json.dumps(json_data)

# --- Custom Unit Test Framework ---

def assert_equal(actual, expected, message=""):
    if actual != expected:
        raise AssertionError(f"Assertion failed: {actual!r} != {expected!r}. {message}")
    print(f"  PASS: {message or 'Values are equal'}")

def assert_true(condition, message=""):
    if not condition:
        raise AssertionError(f"Assertion failed: Expected True. {message}")
    print(f"  PASS: {message or 'Condition is True'}")

def assert_false(condition, message=""):
    if condition:
        raise AssertionError(f"Assertion failed: Expected False. {message}")
    print(f"  PASS: {message or 'Condition is False'}")

def assert_in(member, container, message=""):
    if member not in container:
        raise AssertionError(f"Assertion failed: {member!r} not in {container!r}. {message}")
    print(f"  PASS: {message or 'Member found in container'}")

# --- Test Cases ---

def test_cobol_example_values():
    print("\nRunning test_cobol_example_values...")
    ws_record = WsRecord()
    ws_record.ws_record_name = "Test Name"
    ws_record.ws_record_value = "Test Value"
    ws_record.set_ws_record_flag_enabled()

    generated_json = generate_json_from_record(ws_record)
    expected_json_dict = {"name": "Test Name", "value": "Test Value", "enabled": True}
    expected_json_string = json.dumps(expected_json_dict)

    assert_equal(json.loads(generated_json), expected_json_dict, "JSON content matches expected dictionary")
    assert_equal(len(generated_json), len(expected_json_string), "JSON string length matches expected")
    assert_equal(len(generated_json), 61, "JSON character count is 61")

def test_flag_true():
    print("\nRunning test_flag_true...")
    ws_record = WsRecord()
    ws_record.ws_record_name = "Name"
    ws_record.ws_record_value = "Val"
    ws_record.set_ws_record_flag_enabled()

    generated_json = generate_json_from_record(ws_record)
    parsed_json = json.loads(generated_json)

    assert_true(parsed_json["enabled"], "Boolean flag 'enabled' is True")

def test_flag_false():
    print("\nRunning test_flag_false...")
    ws_record = WsRecord()
    ws_record.ws_record_name = "Name"
    ws_record.ws_record_value = "Val"
    ws_record.set_ws_record_flag_disabled()

    generated_json = generate_json_from_record(ws_record)
    parsed_json = json.loads(generated_json)

    assert_false(parsed_json["enabled"], "Boolean flag 'enabled' is False")

def test_various_string_lengths():
    print("\nRunning test_various_string_lengths...")
    # Case 1: Shorter strings, no padding in input, but padded internally
    ws_record1 = WsRecord()
    ws_record1.ws_record_name = "Short"
    ws_record1.ws_record_value = "Data"
    ws_record1.set_ws_record_flag_disabled()
    json1 = json.loads(generate_json_from_record(ws_record1))
    assert_equal(json1["name"], "Short", "Short name trimmed correctly")
    assert_equal(json1["value"], "Data", "Short value trimmed correctly")

    # Case 2: Exactly 10 characters, no trimming needed for JSON output
    ws_record2 = WsRecord()
    ws_record2.ws_record_name = "TenChars  " # Input with spaces, will be truncated/padded to 10
    ws_record2.ws_record_value = "Full Value"
    ws_record2.set_ws_record_flag_enabled()
    json2 = json.loads(generate_json_from_record(ws_record2))
    assert_equal(json2["name"], "TenChars", "10-char name trimmed correctly")
    assert_equal(json2["value"], "Full Value", "10-char value trimmed correctly")

    # Case 3: Empty strings (COBOL empty string would be all spaces)
    ws_record3 = WsRecord()
    ws_record3.ws_record_name = "" # Will become "          " internally
    ws_record3.ws_record_value = "" # Will become "          " internally
    ws_record3.set_ws_record_flag_disabled()
    json3 = json.loads(generate_json_from_record(ws_record3))
    assert_equal(json3["name"], "", "Empty name trimmed correctly")
    assert_equal(json3["value"], "", "Empty value trimmed correctly")

def test_field_mapping():
    print("\nRunning test_field_mapping...")
    ws_record = WsRecord()
    ws_record.ws_record_name = "MyName"
    ws_record.ws_record_value = "MyValue"
    ws_record.set_ws_record_flag_enabled()

    generated_json = generate_json_from_record(ws_record)
    parsed_json = json.loads(generated_json)

    assert_in("name", parsed_json, "JSON contains 'name' key")
    assert_in("value", parsed_json, "JSON contains 'value' key")
    assert_in("enabled", parsed_json, "JSON contains 'enabled' key")
    assert_equal(parsed_json["name"], "MyName", "Name field mapped correctly")
    assert_equal(parsed_json["value"], "MyValue", "Value field mapped correctly")
    assert_true(parsed_json["enabled"], "Enabled field mapped correctly")

def test_ws_record_flag_setter_validation():
    print("\nRunning test_ws_record_flag_setter_validation...")
    ws_record = WsRecord()
    
    # Test rejection of invalid values
    try:
        ws_record.ws_record_flag = "invalid"
        raise AssertionError("Expected ValueError for 'invalid' but none was raised.")
    except ValueError:
        print("  PASS: Setter rejects 'invalid'")
    except Exception as e:
        print(f"  ERROR: An unexpected error occurred: {e}")
        raise AssertionError(f"Expected ValueError, but got {type(e).__name__} for 'invalid'.")

    try:
        ws_record.ws_record_flag = "TRUE" # Case-sensitive
        raise AssertionError("Expected ValueError for 'TRUE' but none was raised.")
    except ValueError:
        print("  PASS: Setter rejects 'TRUE' (case-sensitive)")
    except Exception as e:
        print(f"  ERROR: An unexpected error occurred: {e}")
        raise AssertionError(f"Expected ValueError, but got {type(e).__name__} for 'TRUE'.")

    try:
        ws_record.ws_record_flag = "FALSE" # Case-sensitive
        raise AssertionError("Expected ValueError for 'FALSE' but none was raised.")
    except ValueError:
        print("  PASS: Setter rejects 'FALSE' (case-sensitive)")
    except Exception as e:
        print(f"  ERROR: An unexpected error occurred: {e}")
        raise AssertionError(f"Expected ValueError, but got {type(e).__name__} for 'FALSE'.")

    # Test acceptance of valid values
    ws_record.ws_record_flag = "true"
    assert_equal(ws_record.ws_record_flag, "true ", "Setter accepts 'true' and pads")
    ws_record.ws_record_flag = "false"
    assert_equal(ws_record.ws_record_flag, "false", "Setter accepts 'false' and pads")

# --- Test Runner ---
# The run_all_tests function is defined but not called here.
# The manager can manually execute run_all_tests() in a compatible environment.
def run_all_tests():
    print("Starting all tests...")
    tests = [
        test_cobol_example_values,
        test_flag_true,
        test_flag_false,
        test_various_string_lengths,
        test_field_mapping,
        test_ws_record_flag_setter_validation,
    ]

    total_tests = len(tests)
    passed_tests = 0

    for test_func in tests:
        try:
            test_func()
            passed_tests += 1
        except AssertionError as e:
            print(f"  FAIL: {e}")
        except Exception as e:
            print(f"  ERROR: An unexpected error occurred in {test_func.__name__}: {e}")

    print(f"\n--- Test Summary ---")
    print(f"Total tests run: {total_tests}")
    print(f"Tests passed: {passed_tests}")
    print(f"Tests failed: {total_tests - passed_tests}")
    print(f"--------------------")