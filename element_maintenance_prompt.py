output_format="""```json
{
    "locator_type_enum": "<xpath/csspath/id_value/name/class_name/tag_name/js_path>",
    "field_name": "<suggest a meaningful name for the element>",
    "field_definition": "<reliable identifier value that aligns with the locator_type_enum>"
}
```"""

_prompt = """
You are an intelligent agent tasked with identifying the most suitable HTML element based on the provided element details.
Your goal is to analyze the Page source, a visual representation (screenshot), test execution details and a natural language description of the target element to determine the best match element.  

First, analyze the two images provided in the element_screenshot_url (the expected image) and step_screenshot_url (the obtained image). Compare them to identify any visual discrepancies or issues.
In the element screenshot , the entire page will be there and the element will be highlighted in green color box.

Instructions:
Element Matching Criteria:
- Identify the element based on its text content, type, attributes, or structure within the HTML.
- Do not restrict matches to exact text; consider contextual similarities.
- If multiple elements match, select the most stable one (e.g., avoid dynamic IDs, prefer well-structured class names).
- Priority: Always return the key attribute of the best-matched tag. The key is a unique identifier for each tag and must be included in the output.
- If analyzer suggestion is available, use it to get the reliable identifier
- locator_type_enum should be <xpath/csspath/id_value/name/class_name/tag_name/js_path> mostly prefer xpath and csspath in the order mentioned

Input Data:
- HTML Source: The HTML of the webpage. Each element has a unique key attribute for identification.
- Webpage Screenshot at the time of failure: A visual representation of the page (for context).
- Element Screenshot: The element screenshot in which element is inside a green box.
- Test Steps: A list of steps that we are performing on the webpage.
- Failed Step Details: The step that failed during the test execution along with the available logs and error message.
- Strightly adhere to the output format below don't add anything extra.


Output Format:
- Your response must strictly adhere to the JSON format below, without any additional text or explanations.

Reasoning Process:
- Analyze the entire HTML source and identify all elements that partially or fully match the context.
- Evaluate each candidate element based on stability (e.g., prefer id, name, or well-structured class attributes over dynamic or ambiguous attributes).
- If multiple elements match, select the one that is most likely to remain consistent across page loads (e.g., avoid elements with dynamic attributes).

<OUTPUT FORMAT>
{output_format}
</OUTPUT FORMAT>

<PAGE SOURCE AT THE TIME OF ELEMENT CAPTURE>
{page_source}
</PAGE SOURCE AT THE TIME OF ELEMENT CAPTURE>

<FAILED STEP DETAILS>
{failed_step}
</FAILED STEP DETAILS>

<PAGE SOURCE WHEN FAILED TO LOCATE THE ELEMENT>
{page_source_when_failed}
</PAGE SOURCE WHEN FAILED TO LOCATE THE ELEMENT>

<TEST STEPS>
{test_steps}
</TEST STEPS>

<ANALYSER SUGGESTION>
{suggestion}
</ANALYSER SUGGESTION>

"""

def get_element_maintenance_prompt(page_source, failed_step, page_source_when_failed, test_steps, suggestion):
    actual_prompt = _prompt.format(
        page_source=page_source,
        failed_step=failed_step,
        page_source_when_failed=page_source_when_failed,
        test_steps=test_steps,
        suggestion=suggestion,
        output_format=output_format
    )
    return actual_prompt