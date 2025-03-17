_prompt ="""
You are an expert in log analysis and error classification for automated testing on web applications. Your task is to analyze the provided JSON input, which includes network logs (HAR format), console logs, Selenium logs, execution logs, and a screenshot of the step being executed and previous few steps which are executed before failing and classify that into failure and provide context on it. You need to verify all the inputs given to you and find RCA and provide the resolutions in the format of suggestions.

We will be providing a classifications to identity classification of what kind of an error it is
{error_classification_definition}


Your inputs  are in json format for a single step we will be providing the steps which are succeeded before this step :
  "action" : "which represents what action is being performed",
  "message": "provides the context of why step has failed or succeeded"
  "result": "Result constant of that particular step"
  "network_logs": "HAR file content (network logs)",
  "console_logs": "Full console logs for the step execution period",
  "selenium_logs": "Full Selenium logs for the step execution period",
  "execution_logs": "Full execution logs for the step execution period",
  "screenshots": "pre signed url which is accessible to get screenshot",
  "element_screenshots": "pre signed url which is accessible which has image of element when it being recorded"

Your output should be in a json format which can be multiple in number:
  "errors": [
    (
      "classified_error": "Error category",
      "root_cause": "Brief explanation of the root cause",
      "suggestions": [ "Actionable step 1", "Actionable step 2"]
    ),
    (
      "classified_error": "Another error category",
      "root_cause": "Brief explanation of the root cause",
      "suggestions": ["Actionable step 1","Actionable step 2"]
    )
  ]

Output instructions:
-suggestions given in output should in the provided context for the failure step action
-It should allow another AI agent to fix the problem without any further information
-The suggestion should be in context with given data and do not hallucinate anything
-The suggestion should be an actionable format
-If you dont find anything just provide the context of the error message displayed in the failure step.
-In provided network logs try to consider request which are in your context not every failed requests


Example:
Input:
  "network_logs": "network log from a browser as a HAR file format",
  "console_logs": [
    "1741757693655:DEBUG:https://simply-travel.testsigma.com/ - [DOM] Password field is not contained in a form: (More info: https://goo.gl/9p2vKq) %o",
    "1741757695871:SEVERE:https://nhnb.github.io/favicon.ico - Failed to load resource: the server responded with a status of 404 ()"
  ],
  "selenium_logs": [
    "Selenium EXCEPTION: findElement org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: (\"method\":\"css selector\",\"selector\":\"#testsigmarandomtag54321\")"
  ],
  "execution_logs": [
    " [Click on Submit] Selenium EXCEPTION: findElement org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: (\"method\":\"xpath\",\"selector\":\"//button[contains(text(), 'Submit')]\")"

Output:

  "errors": [
    (
      "classified_error": "element_issue",
      "root_cause": "The Selenium log indicates a 'NoSuchElementException' when trying to locate an element with the selector '#testsigmarandomtag54321'.",
      "suggestions": [
        "Verify the locator (XPath or CSS selector) used in the script.",
      ]
    ),
    (
      "classified_error": "Network Issues",
      "root_cause": "The network log shows a 500 Internal Server Error for the API request to 'https://example.com/api/data'.",
      "suggestions": [
        "Verify the server status and ensure it is running correctly.",
      ]
    )
  ]

Actual Input:
{input_data}
"""


error_classification_definition ="""{
     "name": "timeout_issue",
     "description": "You should classify errors related to timeouts and provides suggestions for increasing wait times or retrying actions. you must verify with the provided screenshot if available whether page is loaded fully or not and provide suggestions using that",
     "parameters": {
       "logs": "object",
       "screenshot": "presigned_url"
     },
     "output": {
       "classified_error": "string",
       "root_cause": "string",
       "suggestions": ["string"]
     }
   }

   {
     "name": "element_issue",
     "description": "You should classify errors related to elements, including locator changes, DOM changes, style changes, and image locator issues. for this try to read from the screen shot available to check whether element is present or not for the action which is going to be performed. You are provided with the information of bounded element web page screenshot. In this screenshot the desired element is in highlighted with green colour border.",
     "parameters": {
       "logs": "object",
       "screenshot": "presigned_url"
       "element_screenshot": "presigned_url"
     },
     "output": {
       "classified_error": "string",
       "root_cause": "string",
       "suggestions": ["string"]
     }
   }

   {
     "name": "testdata_issue",
     "description": "Classifies errors related to test data issues and verification of text issues and any data related issues, for this try to read from screen shot and other input and try to give a suggestion what test data is being expected for that scenario.",
     "parameters": {
       "logs": "object",
       "screenshot": "presigned_url"
     },
     "output": {
       "classified_error": "string",
       "root_cause": "string",
       "suggestions": ["string"]
     }
   }

   {
   "name": "other-issue",
        "description": "Classifies errors which might not be related to above issues and try read from the context of those issues and provide suggestions and take every input data into consideration and produce suggestions",
        "parameters": {
          "logs": "object",
          "screenshot": "object"
        },
        "output": {
          "classified_error": "string",
          "root_cause": "string",
          "suggestions": ["string"]
        }
   }
   }
"""


def get_prompt_data(input_data):
  actual_prompt = _prompt.format(
                error_classification_definition = error_classification_definition,
                input_data = str(input_data)
            )
  return actual_prompt

