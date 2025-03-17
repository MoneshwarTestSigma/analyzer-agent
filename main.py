import json
from map_logs_to_step import map_logs_to_steps
from step_result_transformer import get_transformed_step_results, get_mapped_result_url
from text_summarizer import summarize_text
from utils import save_mapped_results, should_skip_analysis
from s3_client import S3Client
import argparse



def main(input_json):

    should_skip, skip_message = should_skip_analysis(input_json)
    if (should_skip):
        print(skip_message)
        return

    steps_base_url = input_json.get('step_results_base_url')
    logs_base_url = input_json.get('logs_base_url')
    console_log_url = logs_base_url + "console.log"
    network_log_url = logs_base_url + "network.har"
    selenium_log_url = logs_base_url + "selenium.log"
    execution_log_url = input_json.get('execution_logs_url')
    screenshot_base_url = input_json.get('screenshot_base_url')
    failed_step_locator_base_url = input_json.get('failed_step_locator_base_url')
    element_screenshot_base_url = input_json.get('element_screenshot_base_url')
    
    mapped_results_file_path = "mapped_results.json"

    s3_client = S3Client()
    steps = s3_client.list_and_download_json_files(steps_base_url)
    step_results_map = get_transformed_step_results(steps , screenshot_base_url , element_screenshot_base_url)
    network_logs = s3_client.get_file(network_log_url , 'utf-8')
    execution_logs = s3_client.get_file(execution_log_url , 'windows-1252')
    selinium_logs = s3_client.get_file(selenium_log_url , 'windows-1252')
    console_logs = s3_client.get_file(console_log_url, 'windows-1252')
    

    mapped_results = map_logs_to_steps(step_results_map, network_logs, execution_logs, selinium_logs, console_logs)
    
    mapped_results_file_url = get_mapped_result_url(input_json)
    s3_client.upload_json(mapped_results, mapped_results_file_url)

    # # Save results
    save_mapped_results(mapped_results, mapped_results_file_path)

    summarized_results = summarize_text(json.dumps(mapped_results))

    save_mapped_results(summarized_results, 'summarized_mapped_results.txt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log URLs from JSON input.")
    parser.add_argument("--json_file", required=True, help="Path to JSON file containing URLs")

    args = parser.parse_args()
    
    try:
        with open(args.json_file, 'r') as f:
            input_json = json.load(f)
        main(input_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        raise Exception(f"Error parsing JSON file: {e}")
    except FileNotFoundError:
        print(f"JSON file not found: {args.json_file}")
        raise Exception(f"JSON file not found: {args.json_file}")

