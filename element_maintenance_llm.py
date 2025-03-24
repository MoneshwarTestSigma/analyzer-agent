import os
import openai

from element_maintenance_prompt import get_element_maintenance_prompt
from utils import save_file
from s3_client import S3Client
import argparse
import json


def analyse_element_failure(api_key, input_data , step_screenshot, element_screenshot, locator, page):
    client = openai.OpenAI(api_key=api_key)
    s3_client = S3Client()

    if locator:
        locator_data = s3_client.get_file(locator)
        # save_file(locator_data, "locator.html")

    if page:
        page_data = s3_client.get_file(page)
        save_file(page_data, "page.json")

    prompt = get_element_maintenance_prompt(
        page_data,
        input_data.get('mapped_results'),
        locator_data,
        input_data.get('step_context'),
        input_data.get('suggestion')
    )
    
    message_content = [{"type": "text", "text": prompt}]


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

def removeFromInputIfExists(input):
    for key in input:
        if key in input:
            del input[key]
    return input


def main(input_data):
    API_KEY = os.getenv("OPEN_AI_API_KEY")
    step = input_data.get("screenshot_url")
    element = input_data.get("element_screenshot_url")
    failed_locator = input_data.get("failed_locator_url")
    page_source = input_data.get("locator_tree_url")
    # input_data = removeFromInputIfExists(["step_screenshot_url", "element_screenshot_url", "failed_locator_url", "locator_tree_url"])
    root_cause = analyse_element_failure(API_KEY , input_data , step , element, failed_locator, page_source)
    save_file(root_cause, 'element_root_cause.txt')
    print(root_cause)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log URLs from JSON input.")
    parser.add_argument("--json_file", required=True, help="Path to JSON file containing URLs")

    args = parser.parse_args()
    
    try:
        with open(args.json_file, 'r') as f:
            input_json = json.load(f)
        main(input_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        raise Exception(f"Error parsing JSON file: {e}")
    except FileNotFoundError:
        print(f"JSON file not found: {args.json_file}")
        raise Exception(f"JSON file not found: {args.json_file}")