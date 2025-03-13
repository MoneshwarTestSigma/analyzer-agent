import gzip
import json
import urllib

def get_transformed_step_results(stepResultUrls, buffer=0):
        transformed_data = {}
        for url in stepResultUrls :
            step_results = getStepFile(url)
            # First, find failure entries and their context
            filtered_results = []
            for i, step in enumerate(step_results):
                if step.get('result') == 'FAILURE':
                    # Get up to buffer previous entries and the failure entry
                    start_idx = max(0, i - buffer)
                    filtered_results.extend(step_results[start_idx:i+1])
            
            filtered_results = step_results
            # Transform only the filtered data
            for step in filtered_results:
                transformed_data[step.get('uuid')] = transform_step(step)

            print(f"Transformed step results count: {len(transformed_data)}")   


        return transformed_data

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
        'test_case_result_id': step.get('testCaseResultId'),
        'test_case_id': step.get('metadata', {}).get('testStep', {}).get('testCaseId'),
        'network_logs': [],
        'execution_logs': [],
        'selenium_logs': [],
        'console_logs': []
    }

def getStepFile(url):
    try:
        with urllib.request.urlopen(url) as response:
            compressed_data = response.read()
            data = gzip.decompress(compressed_data).decode('utf-8') 
            return json.loads(data) 
    except Exception as e:
        print(f"Error fetching file from {url}: {e}")
        return None