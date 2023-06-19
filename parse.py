from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import os
import re
import math

load_dotenv()
logfile_path = os.getenv("LOGFILE_PATH")
startdate = os.getenv("START_DATE") # this is if you want a specific date to start parsing from

diceRolePattern = re.compile(r'\[[a-z]\d+(?:\+\d+)? = (\d+)', re.IGNORECASE)

def parse_chatlog():
    file_path = logfile_path
    with open(file_path, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the session start tag that matches or is closest to the specified date
    target_date = datetime.strptime(startdate, '%Y-%m-%d')
    session_start_tags = soup.find_all('a', {'name': True})
    closest_date_tag = None
    for tag in session_start_tags:
        session_date = datetime.strptime(tag['name'], '%Y-%m-%d')
        if session_date >= target_date:
            closest_date_tag = tag
            break

    # Remove all elements preceding the closest date tag
    if closest_date_tag:
        previous_elements = closest_date_tag.find_all_previous()
        for element in previous_elements:
            element.extract()

    # Get the original HTML content of the remaining soup
    parsed_html = str(soup)

    return parsed_html


def count_player_attacks(playerName):
    attack_count = 0
    total_attack = 0

    parsed_text = parse_chatlog()

    for line in parsed_text.splitlines():
        if re.search(r'<font color="#FDFDFD">{}: \[ATTACK '.format(re.escape(playerName)), line, re.IGNORECASE):
            match = diceRolePattern.search(line)
            if match:
                attack_value = match.group(1)
                if is_valid_roll(attack_value):
                    attack_count += 1
                    total_attack += int(attack_value)
    average_attack = total_attack / attack_count if attack_count > 0 else 0
    average_attack = math.floor(average_attack)

    return attack_count, average_attack

def count_player_initiatives(playerName):
    initiative_count = 0
    total_initiative = 0
    
    parsed_text = parse_chatlog()
    for line in parsed_text.splitlines():
        if re.search(r'<font color="#FDFDFD">{}: \[INIT\]'.format(re.escape(playerName)), line, re.IGNORECASE):
            match = diceRolePattern.search(line)
            if match:
                initiative_value = match.group(1)
                if is_valid_roll(initiative_value):
                    initiative_count += 1
                    total_initiative += int(initiative_value)
    average_initiative = total_initiative / initiative_count if initiative_count > 0 else 0
    average_initiative = math.floor(average_initiative)

    return initiative_count, average_initiative

def is_valid_roll(value):
    try:
        roll = int(value)
        if roll >= 1: 
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

if __name__ == "__main__":
    player_name = "brynlin"  # Replace "Your Player Name" with the actual player name
    count, average = count_player_attacks(player_name)
    print("Attack Count:", count)
    print("Average Attack Roll:", average)