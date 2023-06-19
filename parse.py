from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
logfile_path = os.getenv("LOGFILE_PATH")

logfile_path = logfile_path

def parse_chatlog():
    file_path = logfile_path
    with open(file_path, 'r') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup


def count_player_attacks(playerName):
    counter = 0

    soup = parse_chatlog()

    attack_lines = soup.find_all('font', color='#FDFDFD')

    for line in attack_lines:
        text = line.get_text()
        if playerName in text and "[ATTACK" in text:
            counter += 1

    return counter

def count_player_initiatives(playerName):
    counter = 0

    soup = parse_chatlog()

    attack_lines = soup.find_all('font', color='#FDFDFD')

    for line in attack_lines:
        text = line.get_text()
        if playerName in text and "[INIT" in text:
            counter += 1

    return counter

def count_player_criticalhits(playerName):
    counter = 0

    soup = parse_chatlog()

    attack_lines = soup.find_all('font', color='#FDFDFD')

    for line in attack_lines:
        text = line.get_text()
        if playerName in text and "[CRITICAL" in text:
            counter += 1

    return counter