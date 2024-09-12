import random
import time
import requests


headers_list = [
    { 
        'authority': 'fbref.com', 
        'cache-control': 'max-age=0', 
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
        'sec-ch-ua-mobile': '?0', 
        'upgrade-insecure-requests': '1', 
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'sec-fetch-site': 'none', 
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-user': '?1', 
        'sec-fetch-dest': 'document', 
        'sec-ch-ua-platform': 'macOS',
        'accept-language': 'en-US,en;q=0.9', 
    },
    { 
        'authority': 'fbref.com', 
        'cache-control': 'max-age=0', 
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"', 
        'sec-ch-ua-mobile': '?0', 
        'upgrade-insecure-requests': '1', 
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-user': '?1', 
        'sec-fetch-dest': 'document', 
        'sec-ch-ua-platform': 'macOS',
        'accept-language': 'en-US,en;q=0.9', 
    }
] 

def crawl(url):
    """
    Sends a GET request to the url and returns the response.
    Includes a random timeout between 2 and 20 seconds to avoid hitting rate limits.
    If the server responds with a 429 error, raises an exception
    """
    timeout = random.randint(2, 20)
    time.sleep(timeout)
    print('sleeping for ', timeout)

    # Choose a random set of headers to include in the request
    headers = random.choice(headers_list)
    
    # Send the request
    data = requests.get(url, headers=headers)
    
    # If the server responds with a 429 error, raise an exception
    if 'Rate Limited Request (429 error)' in data.text:
        raise Exception('Rate limit error')
    
    # Return the response
    return data
