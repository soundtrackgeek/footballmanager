import random
import json
from itertools import combinations

def generate_fixture_list(teams):
    fixtures = []
    for week in range(38):
        week_fixtures = []
        if week < 19:
            # First half of the season
            matches = list(combinations(teams, 2))
            random.shuffle(matches)
            week_fixtures = matches[:10]
        else:
            # Second half of the season (reverse fixtures)
            first_half_week = week - 19
            week_fixtures = [(away, home) for home, away in fixtures[first_half_week]]
        fixtures.append(week_fixtures)
    return fixtures

def save_fixture_list(fixtures):
    fixture_list = []
    for week, matches in enumerate(fixtures, 1):
        week_fixtures = [{"home": home.name, "away": away.name} for home, away in matches]
        fixture_list.append({"week": week, "matches": week_fixtures})
    
    with open("fixture_list.json", "w") as f:
        json.dump(fixture_list, f, indent=2)

def get_current_week_fixtures(fixtures, current_week):
    if 1 <= current_week <= 38:
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
