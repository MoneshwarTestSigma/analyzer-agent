
import json


def get_element_input():
        with open("input.json", 'r') as f:
            input_json = json.load(f)
            with open("mapped_results.json", 'r') as f:
                results =  json.load(f)
                input_data = {
                    "lab_type" : input_json.get("lab_type"),
                    "platform": input_json.get("platform"),
                    "resolution": input_json.get("resolution"),
                    "browser": input_json.get("browser"),
                    "browser_version": input_json.get("browser_version"),
                    "os_version": input_json.get("os_version"),
                    "test_case_error_message": input_json.get("message"),
                    "test_step_error_message" : results.get("failed_result_context_details",{})[0].get("message"),
                    "test_step_action" :  results.get("failed_result_context_details",{})[0].get("action"),
                    "screenshots":results.get("failed_result_context_details",{})[0].get("screenshots"),
                    "element_screenshots" : results.get("failed_result_context_details",{})[0].get("element_screenshots"),
                }
                return input_data;