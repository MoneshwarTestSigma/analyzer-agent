from s3_client import S3Client
from utils import get_bucket_and_path


def get_transformed_step_results(step_results_json, screenshot_base_url, element_screenshot_base_url , buffer=0):
        transformed_data = {}
        filtered_results = []
        for i, step in enumerate(step_results_json):
            if step.get('result') == 'FAILURE':
                start_idx = max(0, i - buffer)
                filtered_results.extend(step_results_json[start_idx:i+1])
            
            # Transform only the filtered data
        for step in filtered_results:
            transformed_data[step.get('uuid')] = transform_step(step , screenshot_base_url , element_screenshot_base_url)

        return transformed_data

def get_mapped_result_url(input_json):
    base_url = "custify-raw-data/analyzer_agent/{tenant_id}/case-{test_case_id}/result-{test_case_result_id}-mapped-results.json"
    return base_url.format(
        tenant_id=str(input_json.get('tenant_id')),
        test_case_id=str(input_json.get('test_case_id')),
        test_case_result_id=str(input_json.get('id'))
    )

# Helpers:
def transform_step(step , screenshot_base_url , element_screenshot_base_url):
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
        'console_logs': [],
        'screenshots' : get_screenshot_presigned(step , screenshot_base_url),
        'element_screenshots' : get_element_screenshot_presigned(step , element_screenshot_base_url)
    }

def get_screenshot_presigned(step , screenshot_base_url):
    screenshot_name = step.get('screenshotName')
    if screenshot_name is None:
        return ""
    s3_client = S3Client()
    bucket, path = get_bucket_and_path(screenshot_base_url)
    presigned_url = s3_client.get_presigned_url(
        bucket,
        f"{path}{screenshot_name}"
    )
    return presigned_url

def get_element_screenshot_presigned(step , element_screenshot_base_url):
    element_id = step.get('fieldDefinitionDetails', {}).get('ui-identifier', {}).get('uiIdentifierEntity', {}).get('id')
    if element_id is None:
        return ""
    bucket, path = get_bucket_and_path(element_screenshot_base_url)
    s3_client = S3Client()
    presigned_url = s3_client.get_presigned_url(
        bucket,
        f"{path}element-{element_id}.png"
    )
    return presigned_url