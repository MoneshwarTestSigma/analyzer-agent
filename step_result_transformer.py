import gzip
import json
import urllib

def get_transformed_step_results(step_results_json, buffer=0):
        transformed_data = {}
        filtered_results = []
        for i, step in enumerate(step_results_json):
            if step.get('result') == 'FAILURE':
                start_idx = max(0, i - buffer)
                filtered_results.extend(step_results_json[start_idx:i+1])
            
            # Transform only the filtered data
        for step in filtered_results:
            transformed_data[step.get('uuid')] = transform_step(step)

        return transformed_data

def get_mapped_result_url(input_json):
    base_url = "custify-raw-data/analyzer_agent/{tenant_id}/case-{test_case_id}/result-{test_case_result_id}-mapped-results.json"
    return base_url.format(
        tenant_id=str(input_json.get('tenant_id')),
        test_case_id=str(input_json.get('test_case_id')),
        test_case_result_id=str(input_json.get('id'))
    )

# Helpers:
def transform_step(step):
    return {
        'step_result_number': step.get('stepNumber'),
        'uuid': step.get('uuid'),
        'startTime': step.get('startTime'),
        'endTime': step.get('endTime'),
        'message': step.get('message'),
        'result': step.get('result'),
        'step_id': step.get('metadata', {}).get('testStep', {}).get('id'),
        'action': step.get('metadata', {}).get('testStep', {}).get('action'),
        'test_case_result_id': step.get('testCaseResultId'),
        'test_case_id': step.get('metadata', {}).get('testStep', {}).get('testCaseId'),
        'network_logs': [],
        'execution_logs': [],
        'selenium_logs': [],
        'console_logs': []
    }