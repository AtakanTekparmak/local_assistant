import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def get_weather(city: str) -> str:
    """
    Get the weather for a given city

    Args:
        city (str): The city to get the weather for

    Returns:
        str: The weather for the given city
    """
    # Add 'hl=en' to the URL to request the page in English
    url = f"https://www.google.com/search?q={quote_plus(city + ' weather')}&hl=en"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"  # Request English language content
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the temperature element
        temp_element = soup.find('span', {'id': 'wob_tm'})
        
        # Find the weather condition element
        condition_element = soup.find('span', {'id': 'wob_dc'})
        
        if temp_element and condition_element:
            temperature = temp_element.text
            condition = condition_element.text
            return f"The current weather in {city} is {condition} with a temperature of {temperature}°C"
        else:
            return "Weather information not found"
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"