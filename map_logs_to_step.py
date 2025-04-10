from network_log_transformer import create_network_log_map
from utils import get_ms_from_time, get_time_in_milliseconds, parse_log_entry
def map_logs_to_steps(step_results_map, har_entries, execution_logs, selenium_logs, console_logs, context_results, test_case_message):

    buffer_time = 500  # 0.5 second buffer
    string_max_len = 1000
    
    # Create time-based mapping for HAR entries
    har_log_data = create_network_log_map(har_entries['log']['entries']) if har_entries else {}

    
    # Process each step in the map
    for uuid, step_data in step_results_map.items():
        start_time = step_data['startTime']
        end_time = step_data['endTime']
        start_time_ms = get_time_in_milliseconds(start_time) - buffer_time
        end_time_ms = get_time_in_milliseconds(end_time) + buffer_time
        
        # Map network logs based on time range
        populate_network_logs(buffer_time, har_log_data, step_data, start_time, end_time)

        # Map execution logs by UUID
        populate_execution_logs(execution_logs, uuid, step_data)
        
        # Map selinium logs based on time range
        populate_selenium_logs(selenium_logs, string_max_len, step_data, start_time_ms, end_time_ms)
        
        # Map console logs based on time range
        populate_console_logs(console_logs, buffer_time, step_data, start_time, end_time)

    return generate_results_with_context(step_results_map, context_results, test_case_message)



# Helper:

def generate_results_with_context(step_results_map, context_results, test_case_message):

    # Prepare the final response structure
    results_with_context = {
        "failed_result_context_details": list(step_results_map.values()),
        "step_results_context": context_results,
        "test_case_message" : test_case_message
    }

    return results_with_context

def populate_console_logs(console_logs, buffer_time, step_data, start_time, end_time):
    if console_logs and not any(line.startswith('//') for line in console_logs):  # Check if there are actual logs
        for log_line in console_logs:
            try:
                time_str = log_line.split(':')[0]
                total_ms = int(time_str)
                if total_ms >= end_time + buffer_time:
                    break
                    # Check if log time falls within the given time range
                if start_time - buffer_time <= total_ms <= end_time + buffer_time:
                    step_data['console_logs'].append(log_line.strip())
            except ValueError:
                pass

def populate_selenium_logs(selenium_logs, string_max_len, step_data, start_time_ms, end_time_ms):
    if selenium_logs:
        for log_line in selenium_logs:
            try:
                total_ms = get_ms_from_time(log_line.split(' ')[0], "Etc/GMT+4")
                if total_ms >= end_time_ms:
                    break
                    # Check if log time falls within the given time range
                if log_line.split(' ')[1] == 'ERROR' and start_time_ms <= total_ms <= end_time_ms:
                    step_data['selenium_logs'].append(log_line.strip()[:string_max_len])
            except ValueError:
                pass

def populate_execution_logs(execution_logs, uuid, step_data):
    execution_log_populated = False
    if execution_logs:
        for log_line in execution_logs:
            log_entry = parse_log_entry(log_line)
            if execution_log_populated and log_entry and log_entry['uuid'] != uuid:
                break
            if log_entry and log_entry['uuid'] == uuid:
                execution_log_populated = True
                step_data['execution_logs'].append(log_entry['message'])

def populate_network_logs(buffer_time, har_log_data, step_data, start_time, end_time):
    if har_log_data:
        for (start, end), log_entry in har_log_data.items():
            if start >= end_time + buffer_time:
                break
            if(start >= start_time - buffer_time and end <= end_time + buffer_time):
                step_data['network_logs'].append(log_entry)

