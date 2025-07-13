import json

class WsRecord:
    def __init__(self):
        # Initialize with spaces to simulate COBOL PIC X fixed-length fields
        self._ws_record_name = "          "  # PIC X(10)
        self._ws_record_value = "          " # PIC X(10)
        self._ws_record_blank = "          " # PIC X(10)
        self._ws_record_flag = "false"       # PIC X(5) - initial value "false"

    @property
    def ws_record_name(self):
        return self._ws_record_name

    @ws_record_name.setter
    def ws_record_name(self, value):
        # COBOL PIC X(N) behavior: right-pad with spaces, truncate if too long
        self._ws_record_name = value.ljust(10)[:10]

    @property
    def ws_record_value(self):
        return self._ws_record_value

    @ws_record_value.setter
    def ws_record_value(self, value):
        # COBOL PIC X(N) behavior: right-pad with spaces, truncate if too long
        self._ws_record_value = value.ljust(10)[:10]

    @property
    def ws_record_blank(self):
        return self._ws_record_blank

    @ws_record_blank.setter
    def ws_record_blank(self, value):
        # COBOL PIC X(N) behavior: right-pad with spaces, truncate if too long
        self._ws_record_blank = value.ljust(10)[:10]

    @property
    def ws_record_flag(self):
        # Return the raw, padded string value
        return self._ws_record_flag

    @ws_record_flag.setter
    def ws_record_flag(self, value):
        # Simulate 88-level items: only "true" or "false" strings are valid
        if value in ["true", "false"]:
            # Ensure it's padded to 5 characters, as per PIC X(5)
            self._ws_record_flag = value.ljust(5)[:5]
        else:
            raise ValueError("ws_record_flag must be 'true' or 'false'")

    def set_ws_record_flag_enabled(self):
        # Simulates 88 ws-record-flag-enabled value "true"
        self._ws_record_flag = "true ".ljust(5)[:5] # "true" + 1 space = 5 chars

    def set_ws_record_flag_disabled(self):
        # Simulates 88 ws-record-flag-disabled value "false"
        self._ws_record_flag = "false".ljust(5)[:5] # "false" = 5 chars

def generate_json_from_record(record: WsRecord) -> str:
    """
    Generates a JSON string from a WsRecord instance, mapping COBOL field names
    to specified JSON keys and handling boolean conversion.
    """
    # COBOL's JSON GENERATE typically trims trailing spaces from PIC X fields.
    name = record.ws_record_name.strip()
    value = record.ws_record_value.strip()

    # Handle 88-level boolean flag conversion.
    # The internal _ws_record_flag stores the padded string ("true " or "false").
    # We strip it before checking for "true" to get the correct boolean.
    enabled = True if record._ws_record_flag.strip() == "true" else False

    json_data = {
        "name": name,
        "value": value,
        "enabled": enabled
    }

    # json.dumps by default adds spaces after colons and commas,
    # which results in 61 characters for the example output.
    return json.dumps(json_data)

# Main application logic (simulating COBOL PROCEDURE DIVISION)
# This block will be executed directly by the environment.

# Simulate COBOL working-storage section initialization
ws_record = WsRecord()

# Simulate COBOL procedure division assignments
ws_record.ws_record_name = "Test Name" # Will be padded to "Test Name " by setter
ws_record.ws_record_value = "Test Value" # Will be padded to "Test Value" by setter
ws_record.set_ws_record_flag_enabled() # Will set _ws_record_flag to "true "

# Generate JSON
json_output = generate_json_from_record(ws_record)
json_char_count = len(json_output)

# Display results, simulating COBOL DISPLAY statements
# Replicating `display "Generated JSON for record: " ws-record`
# ws-record is the concatenation of its raw, padded fields
full_ws_record_content = f"{ws_record._ws_record_name}{ws_record._ws_record_value}{ws_record._ws_record_blank}{ws_record._ws_record_flag}"
print(f"Generated JSON for record: {full_ws_record_content}")
print("----------------------------")
print(json_output)
print("----------------------------")
print(f"JSON output character count: {json_char_count}")
print("Done.")