import random
import json
from itertools import combinations

def generate_fixture_list(teams):
    team_names = [team.name for team in teams]
    fixtures = []
    
    for _ in range(2):  # Two rounds (home and away)
        round_fixtures = []
        teams_copy = team_names.copy()
        random.shuffle(teams_copy)
        
        if len(teams_copy) % 2 != 0:
            teams_copy.append("BYE")
        
        n = len(teams_copy)
        
        for _ in range(n - 1):
            week_fixtures = []
            for i in range(n // 2):
                match = {"home": teams_copy[i], "away": teams_copy[n - 1 - i]}
                if match["home"] != "BYE" and match["away"] != "BYE":
                    week_fixtures.append(match)
            round_fixtures.append(week_fixtures)
            teams_copy = [teams_copy[0]] + [teams_copy[-1]] + teams_copy[1:-1]
        
        fixtures.extend(round_fixtures)
    
    random.shuffle(fixtures)
    return [{"week": i+1, "matches": week} for i, week in enumerate(fixtures)]

def save_fixture_list(fixtures):
    with open("fixture_list.json", "w") as f:
        json.dump(fixtures, f, indent=2)

def get_current_week_fixtures(fixtures, current_week):
    if 1 <= current_week <= len(fixtures):
        return fixtures[current_week - 1]["matches"]
    else:
        return []

def load_fixture_list():
    try:
        with open("fixture_list.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fixture list not found. Please generate a new fixture list.")
        return None
