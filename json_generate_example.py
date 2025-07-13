import json

def run_json_generate_example():
    """
    Converts COBOL-like record structure to JSON and displays output,
    mimicking the COBOL JSON GENERATE command.
    Returns the generated JSON string and its character count.
    """
    # COBOL equivalent of working-storage section
    # 01 ws-json-output                       pic x(256).
    # 01 ws-json-char-count                   pic 9(4).
    # 01 ws-record.
    #    05 ws-record-name                  pic x(10).
    #    05 ws-record-value                 pic x(10).
    #    05 ws-record-blank                 pic x(10).
    #    05 ws-record-flag                  pic x(5) value "false".
    #        88 ws-record-flag-enabled      value "true".
    #        88 ws-record-flag-disabled     value "false".

    # Initialize ws-record equivalent as a dictionary
    # COBOL PIC X fields are typically space-padded to their length.
    # For ws-record-blank, it's implicitly initialized to spaces.
    ws_record = {
        "ws-record-name": "          ", # pic x(10) - 10 spaces
        "ws-record-value": "          ", # pic x(10) - 10 spaces
        "ws-record-blank": "          ", # pic x(10) - 10 spaces
        "ws-record-flag": "false"      # pic x(5) - "false" + 0 spaces
    }

    # COBOL: move "Test Name" to ws-record-name
    # COBOL: move "Test Value" to ws-record-value
    # COBOL: set ws-record-flag-enabled to true
    # Note: COBOL moves are left-justified and padded with spaces if source is shorter.
    # If source is longer, it's truncated. Here, "Test Name" is 9 chars, so 1 space pad.
    # "Test Value" is 10 chars, no pad. "true" is 4 chars, so 1 space pad.
    ws_record["ws-record-name"] = "Test Name "
    ws_record["ws-record-value"] = "Test Value"
    ws_record["ws-record-flag"] = "true "

    # Prepare data for JSON generation, applying 'name of' renames
    # and stripping COBOL-style padding.
    # The .strip() ensures that the values in the JSON are not padded.
    json_input_data = {
        "name": ws_record["ws-record-name"].strip(),
        "value": ws_record["ws-record-value"].strip(),
        "enabled": ws_record["ws-record-flag"].strip()
    }

    ws_json_output = ""
    ws_json_char_count = 0
    
    try:
        # COBOL: json generate ws-json-output from ws-record ...
        # Python's json.dumps handles the serialization.
        # We use separators=(',', ':') to match COBOL's compact output
        # (no extra spaces after colon or comma).
        generated_json = json.dumps(json_input_data, separators=(',', ':'))
        ws_json_output = generated_json

        # COBOL: count in ws-json-char-count
        ws_json_char_count = len(ws_json_output)

        # COBOL: not on exception display "JSON document successfully generated."
        print("JSON document successfully generated.")

    except Exception as e:
        # COBOL: on exception display "Error generating JSON error " JSON-CODE
        print(f"Error generating JSON error: {e}")
        # In a real script, this would typically involve sys.exit(1).
        # For a function designed to be tested, we return an error state.
        return None, 0 # Indicate failure

    # COBOL: display "Generated JSON for record: " ws-record
    # Note: The COBOL display of ws-record would show its raw, padded content.
    # For Python, we'll show the dictionary representation.
    print(f"Generated JSON for record: {ws_record}")
    print("----------------------------")
    # COBOL: display function trim(ws-json-output)
    print(ws_json_output.strip()) # In Python, json.dumps doesn't add leading/trailing spaces
    print("----------------------------")
    # COBOL: display "JSON output character count: " ws-json-char-count
    print(f"JSON output character count: {ws_json_char_count}")
    print("Done.")

    return ws_json_output, ws_json_char_count

if __name__ == "__main__":
    # When run as a script, just execute the function.
    # The return values are not used here, but the prints will occur.
    run_json_generate_example()