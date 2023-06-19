from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re
import math

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
    initiative_count = 0
    total_initiative = 0

    pattern = re.compile(r'\[[a-z]\d+(?:\+\d+)? = (\d+)', re.IGNORECASE)
    
    with open(logfile_path, 'r') as log_file:
        for line in log_file:
            if re.search(r'<font color="#FDFDFD">{}: \[INIT\]'.format(re.escape(playerName)), line, re.IGNORECASE):
                match = pattern.search(line)
                if match:
                    initiative_value = match.group(1)
                    if is_valid_initiative(initiative_value):
                        initiative_count += 1
                        total_initiative += int(initiative_value)
    average_initiative = total_initiative / initiative_count if initiative_count > 0 else 0
    average_initiative = math.floor(average_initiative)
    return initiative_count, average_initiative

def is_valid_initiative(initiative_value):
    try:
        initiative = int(initiative_value)
        if initiative >= 1: 
            return True
    except ValueError:
        pass
    return False

def count_player_criticalhits(playerName):
    counter = 0

    soup = parse_chatlog()

    attack_lines = soup.find_all('font', color='#FDFDFD')

    for line in attack_lines:
        text = line.get_text()
        if playerName in text and "[CRITICAL" in text:
            counter += 1

    return counter

# below code is if I want to run this file directly
# if __name__ == "__main__":
#     player_name = "PLAYER_NAME"  # Replace "Your Player Name" with the actual player name
#     count, average = count_player_initiatives(player_name)
#     print("Initiative Count:", count)
#     print("Average Initiative:", average)