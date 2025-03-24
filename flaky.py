import argparse
import json
from s3_client import S3Client
from step_result_transformer import get_mapped_result_url, get_transformed_step_results_for_success

def construct_flaky_input(input_json):
    s3_client = S3Client()
    failure_data_url = get_mapped_result_url(input_json.get("FAILURE"))
    failure_mapped_data = s3_client.get_file(failure_data_url)
    success_step_results = s3_client.get_all_step_results(input_json.get("success_steps_base_url"))
    success_step_result_context_details, success_context = get_transformed_step_results_for_success(success_step_results, success_step_results, success_step_results, failure_mapped_data.get("failed_result_context_details")[0].get("step_id"))
    success_mapped_data = {
        "success_result_context_details": success_step_result_context_details,
        "success_context": success_context
    }
    flaky_input = {
        "FAILURE": failure_mapped_data,
        "SUCCESS": success_mapped_data
    }
    print(flaky_input)

def process_json_input(json_string):
    """
    Process a JSON input string
    Args:
        json_string (str): JSON formatted string
    """
    try:
        input_data = json.loads(json_string)
        construct_flaky_input(input_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Process JSON input from command line')
    parser.add_argument('json_input', help='JSON string to process')
    args = parser.parse_args()
    
    result = process_json_input(args.json_input)
    print(result)

if __name__ == '__main__':
    main()
