import json
from map_logs_to_step import map_logs_to_steps
from step_result_transformer import get_transformed_step_results
from text_summarizer import summarize_text
from utils import getFile, save_mapped_results
import argparse


def main(console_log_url, network_log_url, selenium_log_url, execution_log_url, step_urls):
    
    mapped_results_file_path = "mapped_results.json"
    steps_map = get_transformed_step_results(step_urls)

    network_logs = getFile(network_log_url , 'utf-8')['log']['entries']
    execution_logs = getFile(execution_log_url , 'windows-1252')
    selinium_logs = getFile(selenium_log_url , 'windows-1252')
    console_logs = getFile(console_log_url, 'windows-1252')
    

    mapped_results = map_logs_to_steps(steps_map, network_logs, execution_logs, selinium_logs, console_logs)
    
    # # Save results
    save_mapped_results(mapped_results, mapped_results_file_path)

    summarized_results = summarize_text(json.dumps(mapped_results))

    save_mapped_results(summarized_results, 'summarized_mapped_results.json')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process log URLs.")

    parser.add_argument("--console_log_url", required=True, help="Console log URL")
    parser.add_argument("--network_log_url", required=True, help="Network log URL")
    parser.add_argument("--selenium_log_url", required=True, help="Selenium log URL")
    parser.add_argument("--execution_log_url", required=True, help="Execution log URL")
    parser.add_argument("--step_urls", nargs='+', required=True, help="List of step result URLs")

    args = parser.parse_args()

    main(args.console_log_url, args.network_log_url, args.selenium_log_url, args.execution_log_url, args.step_urls)

