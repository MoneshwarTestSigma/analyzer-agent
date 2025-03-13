import re
import json
from datetime import datetime
import pytz
import urllib.request



def getFile(url , decode):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode(decode)
            if(decode == 'windows-1252'):
                return data.splitlines()
            return json.loads(data) 
    except Exception as e:
        print(f"Error fetching file from {url}: {e}")
        return None

def save_mapped_results(mapped_results, output_file):
    with open(output_file, 'w') as f:
        json.dump(mapped_results, f, indent=4)


def parse_log_entry(line):
        uuid_match = re.search(r'\[Step-([a-f0-9-]+)\]', line)
        message_match = re.search(r'\[Step-[a-f0-9-]+\](.*?)$', line)
        if uuid_match and message_match:
            return {
                'uuid': uuid_match.group(1),
                'message': message_match.group(1)
            }
        return None

def convert_to_ist_ms(timestamp: str, fmt: str) -> int:
    """
    Convert any formatted timestamp to IST (Indian Standard Time) and return in milliseconds.

    :param timestamp: Input timestamp as a string.
    :param fmt: Format of the input timestamp (e.g., "%Y-%m-%dT%H:%M:%S.%f%z").
    :return: Converted IST timestamp in milliseconds.
    """
    # Define the IST timezone
    ist = pytz.timezone("Asia/Kolkata")

    # Parse the input timestamp based on the provided format
    input_time = datetime.strptime(timestamp, fmt)

    # Convert to IST
    ist_time = input_time.astimezone(ist)

    # Return the timestamp in milliseconds
    return int(ist_time.timestamp() * 1000)



def get_time_in_milliseconds(timestamp_ms: int) -> int:
    """
    Convert epoch timestamp to time of day in milliseconds
    
    :param timestamp_ms: Epoch timestamp in milliseconds
    :return: Time of day in milliseconds (HH:MM:SS.mmm as milliseconds)
    """
    # Convert epoch milliseconds to datetime in IST
    ist = pytz.timezone("Asia/Kolkata")
    dt = datetime.fromtimestamp(timestamp_ms / 1000, ist)
    
    # Extract time components and convert to milliseconds
    return (dt.hour * 3600000) + (dt.minute * 60000) + (dt.second * 1000) + (dt.microsecond // 1000)


def get_ms_from_time_old(time_str, source_tz=pytz.timezone("Asia/Kolkata")):
    """
    Convert time string from source timezone to IST milliseconds
    """
    hour, minute, second_ms = time_str.split(':')
    second, ms = second_ms.split('.')

    # Create datetime in source timezone
    source_time = datetime.now(source_tz).replace(
        hour=int(hour),
        minute=int(minute),
        second=int(second),
        microsecond=int(ms) * 1000
    )

    # Convert to IST
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = source_time.astimezone(ist)

    # Convert IST time to milliseconds
    return (ist_time.hour * 3600000 + 
            ist_time.minute * 60000 + 
            ist_time.second * 1000 + 
            ist_time.microsecond // 1000)

def get_ms_from_time(time_str, source_tz):
    """
    Convert time string from source timezone to IST milliseconds.

    :param time_str: Time string in HH:MM:SS.sss format
    :param source_tz: Source timezone as a string (e.g., 'America/New_York', 'UTC-4')
    :return: Milliseconds since the start of the day in IST
    """
    # Parse time components
    hour, minute, second_ms = time_str.split(':')
    second, ms = second_ms.split('.')

    # Define source timezone
    source_tz_obj = pytz.timezone(source_tz)

    # Create a datetime object for an arbitrary date (e.g., Jan 1, 2000)
    dt = datetime(2000, 1, 1, int(hour), int(minute), int(second), int(ms) * 1000)
    dt = source_tz_obj.localize(dt)  # Localize to source timezone

    # Convert to IST
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = dt.astimezone(ist)

    # Convert IST time to milliseconds since midnight
    return (ist_time.hour * 3600000 +
            ist_time.minute * 60000 +
            ist_time.second * 1000 +
            ist_time.microsecond // 1000)
