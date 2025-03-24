_prompt = """
You are an AI assistant tasked with analyzing test case failures in web applications. Your goal is to categorize the error, identify the root cause, and provide actionable suggestions based on the given information.

You will be provided with the following input data:

<input_json>
{INPUT_JSON}
</input_json>

First, analyze the two images provided in the element_screenshot_url (the expected image) and step_screenshot_url (the obtained image). Compare them to identify any visual discrepancies or issues.
In the element screenshot , the entire page will be there and the element will be highlighted in green color box.

Next, consider the following error categories and their descriptions:

1. ELEMENT_NOT_FOUND
   Causes: Incorrect identifier, element not on the page, or inside an iframe.
   Solutions: Verify identifier correctness, check page content, and switch to the correct iframe.

2. DUPLICATE_UI_IDENTIFIERS
   Cause: Multiple elements share the same identifier.
   Solution: Use a more specific XPath or unique attribute.

3. HIDDEN_OR_DISABLED_ELEMENT
   Causes: Elements dynamically created or explicitly disabled/hidden.
   Solutions: Wait for element availability, find an alternative interactable element.

4. INCORRECT_OR_INVALID_UI_IDENTIFIER
   Causes: Mismatch between locator type and value, or element not displayed.
   Solutions: Correct locator format, ensure element is present.

5. EMPTY_UI_IDENTIFIER
   Cause: Missing identifier value.
   Solution: Ensure UI identifier is properly defined.

6. ELEMENT_NOT_CLICKABLE_OR_INTERACTABLE
   Causes: Overlapping elements, element outside viewport, or page loading issues.
   Solutions: Wait for overlays to disappear, close pop-ups, scroll to the element.

7. STALE_ELEMENT_EXCEPTION
   Causes: The element is removed or reloaded dynamically.
   Solutions: Use explicit waits, refresh the page, or re-fetch the element identifier.

8. BROWSER_SPECIFIC_ISSUES
   Causes: Elements may be positioned differently in various browsers due to differences in rendering engines.
   Solutions: Provide a proper XPath to ensure consistency across browsers.

Based on the provided information, including the error message, browser details, and image analysis, classify the error into one of the categories above. If the error doesn't fit precisely into one category, choose the most relevant one.

Provide your analysis and recommendations in the following format just give this data alone as output(don't include <output> tags in actual output you provide, just return the json) don't add anything extra:

<output>
   "classified_error": "Error category",
   "root_cause": "Brief explanation of the root cause",
   "suggestions": ["Actionable step 1", "Actionable step 2"]
</output>

Ensure that your root cause explanation is concise and directly related to the classified error. The suggestions should be specific, actionable steps that can help resolve the issue.
"""

def get_element_prompt(input_data):
    actual_prompt = _prompt.format(INPUT_JSON = input_data)
    return actual_prompt

