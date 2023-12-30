import fire
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from enum import Enum

class Station(Enum):
    PARIS_GARE_DU_NORD = "paris-gare-du-nord", 8727100
    LONDON_ST_PANCRAS = "london-st-pancras", 7015400

    def __init__(self, station_name: str, station_code: int):
        self.station_name = station_name
        self.station_code = station_code

URL_BASE = "https://www.eurostar.com/be-en/travel-info/timetable/"

def validate_station(station: str) -> bool:
    return any(station == s.station_name for s in Station)

def fetch_and_parse(start: str, dest: str, date: str, train: Optional[str] =
                    None) -> None:
    """
    Fetches and parses the timetable information from the Eurostar website for a
    given route on a specific date. Prints the results.

    Example usage:
        eurostar-watcher.py paris-gare-du-nord london-st-pancras 2023-12-30

    Args:
        start (str): The name of the starting station. Must be a valid station
        name as defined in the Station enum.
        dest (str): The name of the destination station. Must be a valid
        station name as defined in the Station enum.
        date (str): The travel date in 'YYYY-MM-DD' format.
        train (str): the specific train, for e.g "ES 9047"
    """
    if not validate_station(start) or not validate_station(dest):
        raise ValueError("Start or destination station is invalid.")

    start_n = next(s for s in Station if s.station_name == start).station_code
    dest_n = next(s for s in Station if s.station_name == dest).station_code

    url = f"{URL_BASE}{start_n}/{dest_n}/{start}/{dest}/?date={date}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Could not retrieve the page content")

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all(attrs={"data-testid": "clickable-card"})

    all_texts = [card.get_text(separator=' ', strip=True) for card in cards]
    
    for text in all_texts:
        if "On time" in text:
            text = text.replace("On time", "\033[92mOn time\033[0m")
        if "Train cancelled" in text:
            text = text.replace("Train cancelled", "\033[91mTrain cancelled\033[0m")

        if train in text:
            text = f"\033[94m* \033[0m{text}"
        else:
            text = f"  {text}"

        print(text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(fetch_and_parse)
