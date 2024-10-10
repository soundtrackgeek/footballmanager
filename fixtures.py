import random
import json

def generate_fixture_list(teams):
    team_names = [team.name for team in teams]
    n = len(team_names)
    fixtures = []
    
    for _ in range(2):  # Two rounds (home and away)
        for i in range(n - 1):
            round_fixtures = []
            for j in range(n // 2):
                if _ == 0:  # First round
                    match = {
                        "home": team_names[j],
                        "away": team_names[n - 1 - j]
                    }
                else:  # Second round (reverse fixtures)
                    match = {
                        "home": team_names[n - 1 - j],
                        "away": team_names[j]
                    }
                round_fixtures.append(match)
            fixtures.append(round_fixtures)
            
            # Rotate the list, keeping the first team fixed
            team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]
    
    # Randomize the order of rounds while keeping week pairs together
    week_pairs = list(zip(fixtures[:19], fixtures[19:]))
    random.shuffle(week_pairs)
    shuffled_fixtures = [round for pair in week_pairs for round in pair]
    
    return [{"week": i+1, "matches": round_fixtures} for i, round_fixtures in enumerate(shuffled_fixtures)]

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
