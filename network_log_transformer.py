from utils import convert_to_ist_ms


def create_network_log_map(har_entries):
    try:
        time_log_map = {}
        for entry in har_entries:
            if not is_json_xhr(entry):
                continue
            start_time_str = entry['startedDateTime']
            duration_ms = entry.get('time', 1000) # Default to 1000ms if duration is not present

            # Convert start_time string to datetime object and then to milliseconds
            try:
                start_time_ms = convert_to_ist_ms(start_time_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                start_time_ms = convert_to_ist_ms(start_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")

            end_time_ms = start_time_ms + duration_ms

            request = entry['request']
            response = entry['response']

            # Extract relevant request information
            request_data = {
                'method': request['method'],
                'url': request['url'],
                'headers': {h['name']: h['value'] for h in request['headers']},
                'postData': request.get('postData', {}).get('text', None) 
            }

            # Extract relevant response information
            response_data = {
                'status': response['status'],
                'statusText': response['statusText'],
                'headers': {h['name']: h['value'] for h in response['headers']}, 
                'content': {
                    'mimeType': response['content']['mimeType'],
                    'size': response['content']['size'],
                    'text': response['content'].get('text', None)
                }
            }
            rca_entry = {
                'request': request_data,
                'response': response_data,
            }
            time_log_map[(start_time_ms, end_time_ms)] = rca_entry
        
        return time_log_map

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {}


# Helper:

def is_json_xhr(entry):
    if entry.get('type') == 'xhr':
        return True

    request_headers = entry.get('request', {}).get('headers', [])
    response_headers = entry.get('response', {}).get('headers', [])

    # Check request headers for Content-Type
    if any(h.get('name', '').lower() == 'content-type' and 'application/json' in h.get('value', '') for h in request_headers):
        return True

    # Check response headers for Content-Type or Accept
    if any(h.get('name', '').lower() == 'content-type' and 'application/json' in h.get('value', '') for h in response_headers):
        return True

    if any(h.get('name', '').lower() == 'accept' and 'application/json' in h.get('value', '') for h in request_headers):
        return True

    return False