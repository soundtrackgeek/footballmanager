import random
import json
from itertools import combinations

def generate_fixture_list(teams):
    team_names = [team.name for team in teams]
    if len(team_names) % 2 != 0:
        team_names.append("BYE")  # Handle odd number of teams

    n = len(team_names)
    fixtures = []

    # Generate first half of the season
    for week in range(n - 1):
        week_matches = []
        for i in range(n // 2):
            home = team_names[i]
            away = team_names[n - 1 - i]
            if home != "BYE" and away != "BYE":
                # Randomly assign home and away
                if random.choice([True, False]):
                    match = {"home": home, "away": away}
                else:
                    match = {"home": away, "away": home}
                week_matches.append(match)
        fixtures.append({"week": week + 1, "matches": week_matches})
        # Rotate teams (except the first team)
        team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]

    # Generate second half by reversing home and away
    second_half = []
    for week in fixtures:
        reversed_matches = [{"home": match["away"], "away": match["home"]} for match in week["matches"]]
        second_half.append({"week": week["week"] + (n - 1), "matches": reversed_matches})

    full_season = fixtures + second_half

    return full_season

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
