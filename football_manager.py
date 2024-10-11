import random
import json
from itertools import combinations

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class Team:
    def __init__(self, name):
        self.name = name
        self.squad = []

    def add_player(self, player):
        self.squad.append(player)

def create_teams():
    teams = [
        "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
        "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
        "Liverpool", "Luton", "Manchester City", "Manchester United", "Newcastle",
        "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"
    ]
    return [Team(name) for name in teams]

def generate_player(position):
    first_names = ["John", "David", "Michael", "James", "William", "Robert", "Richard", "Thomas", "Charles", "Daniel",
                   "Juan", "Mohammed", "Yuki", "Liam", "Sven", "Alejandro", "Dmitri", "Kwame", "Raj", "Giovanni",
                   "Hiroshi", "Fatima", "Olga", "Zain", "Aisha", "Chen", "Priya", "Hassan", "Ingrid", "Paolo"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Nguyen", "Kim", "Patel", "Müller", "Ivanov", "Silva", "Kowalski", "Tanaka", "O'Brien", "Dubois",
                  "Yamamoto", "Ali", "Petrov", "Gonzalez", "Andersson", "Chen", "Singh", "Rossi", "Novak", "Sato"]
    return Player(f"{random.choice(first_names)} {random.choice(last_names)}", position)

def generate_squad(team):
    positions = ["GK", "DF", "MF", "FW"]
    for _ in range(20):
        position = random.choice(positions)
        player = generate_player(position)
        team.add_player(player)

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

def main():
    teams = create_teams()
    for team in teams:
        generate_squad(team)
    
    print("Welcome to Football Manager!")
    num_players = int(input("Enter the number of players (1-4): "))
    
    player_teams = []
    for i in range(num_players):
        print(f"\nPlayer {i+1}, choose your team:")
        for j, team in enumerate(teams):
            print(f"{j+1}. {team.name}")
        
        choice = int(input("Enter the number of your chosen team: ")) - 1
        chosen_team = teams[choice]
        player_teams.append(chosen_team)
        print(f"Player {i+1} has chosen {chosen_team.name}")
        
        print("\nYour squad:")
        for player in chosen_team.squad:
            print(f"{player.name} - {player.position}")
    
    print("\nGenerating fixture list for the season...")
    fixtures = generate_fixture_list(teams)
    save_fixture_list(fixtures)
    print("Fixture list has been generated and saved to 'fixture_list.json'")

if __name__ == "__main__":
    main()
