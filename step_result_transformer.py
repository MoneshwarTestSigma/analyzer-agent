def get_transformed_step_results_for_failure(step_results_json, screenshot_base_url, element_screenshot_base_url, failed_step_locator_base_url, buffer=0):
        transformed_data = {}
        filtered_results = []
        context_results = []
        for i, step in enumerate(step_results_json):
            # [1].metadata.testStep.ignoreStepResult
            if step.get('result') == 'FAILURE' and step.get('metadata',{}).get('testStep',{}).get('ignoreStepResult', False) == False:
                start_idx = max(0, i - buffer)
                filtered_results.extend(step_results_json[start_idx:i+1])
            context_results.append(context_transform(step))
            
            # Transform only the filtered data
        for step in filtered_results:
            transformed_data[step.get('uuid')] = transform_step(step , screenshot_base_url , element_screenshot_base_url, failed_step_locator_base_url)

        return transformed_data, context_results

def get_transformed_step_results_for_success(step_results_json, success_data, failed_result_context_details):
        step_id = failed_result_context_details[0].get("step_id")
        test_case_result_id = success_data.get('id')
        screenshot_base_url = get_success_screenshot_base_url(failed_result_context_details[0].get('screenshots'), test_case_result_id)
        element_screenshot_base_url = get_success_element_screenshot_base_url(failed_result_context_details[0].get('element_screenshots'))
        transformed_success_step = {}
        context_results = []
        for step in step_results_json:
            if step.get('metadata',{}).get('testStep',{}).get('id') == step_id:
                transformed_success_step = transform_step(step, screenshot_base_url, element_screenshot_base_url)
            context_results.append(context_transform(step))

        return transformed_success_step, context_results

def get_mapped_result_url(input_json):
    base_url = "custify-raw-data/analyzer-agent/{tenant_id}/case-{test_case_id}/mapped-results/result-{test_case_result_id}.json"
    return base_url.format(
        tenant_id=str(input_json.get('tenant_id')),
        test_case_id=str(input_json.get('test_case_id')),
        test_case_result_id=str(input_json.get('id'))
    )

# Helpers:
def get_success_screenshot_base_url(failure_screenshot_url, test_case_result_id):
    failure_base = failure_screenshot_url.split('/')[:-2]
    failure_base.append(str(test_case_result_id))
    return "/".join(failure_base) + "/"

def get_success_element_screenshot_base_url(failure_element_screenshot_url):
    failure_base = failure_element_screenshot_url.split('/')[:-1]
    return "/".join(failure_base) + "/"

def transform_step(step, screenshot_base_url, element_screenshot_base_url, failed_step_locator_base_url=None):
    element_id = step.get('fieldDefinitionDetails', {}).get('ui-identifier', {}).get('uiIdentifierEntity', {}).get('id')
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
        **({
            'element_id': element_id,
            'element_screenshots' : get_element_screenshot(element_screenshot_base_url, element_id),
            } if element_id is not None else {}),
        **({
            'failed_locator': get_failed_locator(step, failed_step_locator_base_url),
            } if failed_step_locator_base_url is not None else {}),
        'screenshots' : get_screenshot(step , screenshot_base_url)        
    }

def get_screenshot(step, screenshot_base_url):
    screenshot_name = step.get('screenshotName')
    if screenshot_name is None:
        return ""
    return screenshot_base_url + screenshot_name

def get_element_screenshot(element_screenshot_base_url, element_id):
    return element_screenshot_base_url + f"element-{element_id}.png"

def get_failed_locator(step, failed_step_locator_base_url):
    failed_step_locator_name = step.get('uuid')
    if failed_step_locator_name is None:
        return ""
    return failed_step_locator_base_url + failed_step_locator_name  + '.html'

def context_transform(step):
    return {
        'step_id': step.get('metadata', {}).get('testStep', {}).get('id'),
        'action': step.get('metadata', {}).get('testStep', {}).get('action'),
        'step_order': step.get('metadata', {}).get('testStep', {}).get('stepOrder'),
        'result': step.get('result'),
    }


