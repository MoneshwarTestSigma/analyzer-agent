import os
import openai

from element_prompt import get_element_prompt
from element_llm_utils import get_element_input
from utils import save_file
from s3_client import S3Client


def analyse_element_failure(api_key, input_data , step_screenshot, element_screenshot):
    client = openai.OpenAI(api_key=api_key)
    prompt = get_element_prompt(input_data)
    
    message_content = [{"type": "text", "text": prompt}]
    s3_client = S3Client()

    if element_screenshot:
        presigned_url = s3_client.get_presigned_url(element_screenshot)
        if (presigned_url):
            element_screenshot = presigned_url
            message_content.append({"type": "image_url", "image_url": {"url": element_screenshot}})
    if step_screenshot:
        presigned_url = s3_client.get_presigned_url(step_screenshot)
        if (presigned_url):
            step_screenshot = presigned_url
            message_content.append({"type": "image_url", "image_url": {"url": step_screenshot}})
        
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages = [
            {
                "role": "user",
                "content": message_content
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    API_KEY = os.getenv("OPEN_AI_API_KEY")
    input_data = get_element_input()
    step = input_data.get("screenshots")
    element = input_data.get("element_screenshots")
    if "screenshots" in input_data:
        del input_data["screenshots"]
    if "element_screenshots" in input_data:
        del input_data["element_screenshots"]
    root_cause = analyse_element_failure(API_KEY , input_data , step , element)
    save_file(root_cause, 'element_root_cause.txt')
    print(root_cause)