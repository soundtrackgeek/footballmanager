import random
import json

def generate_fixture_list(teams):
    team_names = [team.name for team in teams]
    n = len(team_names)
    fixtures = []
    
    for i in range(n - 1):
        round_fixtures = []
        for j in range(n // 2):
            match = {
                "home": team_names[j],
                "away": team_names[n - 1 - j]
            }
            round_fixtures.append(match)
        fixtures.append(round_fixtures)
        
        # Rotate the list, keeping the first team fixed
        team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]
    
    # Generate the reverse fixtures for the second half of the season
    reverse_fixtures = []
    for round_fixtures in fixtures:
        reverse_round = []
        for match in round_fixtures:
            reverse_match = {
                "home": match["away"],
                "away": match["home"]
            }
            reverse_round.append(reverse_match)
        reverse_fixtures.append(reverse_round)
    
    all_fixtures = fixtures + reverse_fixtures
    
    # Randomize the order of rounds
    random.shuffle(all_fixtures)
    
    return [{"week": i+1, "matches": round_fixtures} for i, round_fixtures in enumerate(all_fixtures)]

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
