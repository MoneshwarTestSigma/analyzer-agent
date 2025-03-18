_prompt ="""
You are tasked with analyzing and categorizing errors from test execution results. The input will be provided in JSON format, and you need to categorize the errors into specific types, identify root causes, and suggest actionable steps to resolve the issues.

Here is the input JSON structure:

<input_json>
{INPUT_JSON}
</input_json>

Your task is to categorize the errors in the input JSON into the following four categories:

1. TEST_DATA
2. ELEMENT
3. TIMEOUT
4. LAB

For each error, you should:

1. Determine the appropriate error category
2. Identify the root cause of the error
3. Suggest actionable steps to resolve the issue

Here are examples of each error category to guide your analysis:

1. Test Data Related Errors:
   Example: Mismatch between expected and actual URL or data values.

2. Element Related Errors:
   Example: Element not found on the page or incorrect element locator.

3. Timeout Related Errors:
   Example: Page load timeout or element wait timeout.

4. Lab Specific Issues:
   Example: Issues related to test environment setup or configuration.

After analyzing the input JSON, provide your output in the following JSON format only provide this output format don't add anything to it:

<output_format>
   "classified_error": "Error category",
   "root_cause": "Brief explanation of the root cause",
   "suggestions": ["Actionable step 1", "Actionable step 2"]
</output_format>

To complete this task:

1. Carefully read and analyze the input JSON, paying attention to the "message", "action", and other relevant fields in the "failed_result_context_details" array, as well as the "test_case_message" field.

2. For each error found in the input:
   a. Determine the most appropriate error category based on the provided examples and your analysis.
   b. Identify the root cause of the error by examining the error message and related logs.
   c. Suggest 2-3 actionable steps to resolve the issue.

3. Construct your response using the specified output JSON format, ensuring that each error is properly categorized, has an identified root cause, and includes actionable suggestions.

4. If there are multiple errors in the input, include all of them in your output, with each error as a separate object in the "errors" array.

5. If there are no errors in the input JSON or if the input is empty, return an empty "errors" array in your output.

Provide your analysis and output in the specified JSON format, ensuring that all error categories, root causes, and suggestions are clear, concise, and relevant to the input data.

Analysis Instructions:
1. Carefully review all provided logs and screenshots.
2. Identify any errors or issues present in the data.
3. Determine the root cause of each identified error.
4. Generate actionable suggestions for resolving each issue.

Important Guidelines:
Verify all inputs given to you before making any conclusions.
Provide suggestions only in the context of the failure step action.
Ensure suggestions are actionable and allow another AI agent to fix the problem without additional information.
Do not speculate or provide information outside the given context.
For network logs, focus on requests relevant to the context, not every failed request.
Use screenshots to verify page load status and element presence when applicable.
"""

def get_prompt_data(input_data):
  actual_prompt = _prompt.format(
                INPUT_JSON = str(input_data)
            )
  print(actual_prompt)

def get_file_data(file_name):
   with open(file_name, "r") as f:
      return f.read()

if __name__=="__main__":
   input_data = get_file_data("summarized_mapped_results.txt")
   get_prompt_data(input_data)

