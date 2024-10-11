import random
import json
import os

class Player:
    def __init__(self, name, position, rating):
        self.name = name
        self.position = position
        self.rating = rating

class Team:
    def __init__(self, name):
        self.name = name
        self.squad = []

    def add_player(self, player):
        self.squad.append(player)

def create_teams():
    team_names = [
        "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
        "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
        "Liverpool", "Luton", "Manchester City", "Manchester United", "Newcastle",
        "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"
    ]
    teams = [Team(name) for name in team_names]
    for team in teams:
        generate_squad(team)
        save_team_to_file(team)
    return teams

def generate_random_rating():
    return random.randint(60, 90)

def generate_player(position):
    first_names = ["John", "David", "Michael", "James", "William", "Robert", "Richard", "Thomas", "Charles", "Daniel",
                   "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    return Player(f"{random.choice(first_names)} {random.choice(last_names)}", position, generate_random_rating())

def generate_squad(team):
    positions = {
        "GK": 3,
        "DF": 6,
        "MF": 6,
        "FW": 5
    }
    for position, count in positions.items():
        for _ in range(count):
            player = generate_player(position)
            team.add_player(player)

def save_team_to_file(team):
    team_data = {
        "name": team.name,
        "squad": [{"name": player.name, "position": player.position, "rating": player.rating} for player in team.squad]
    }
    
    file_path = os.path.join("Teams", f"{team.name}.json")
    with open(file_path, "w") as f:
        json.dump(team_data, f, indent=2)

def choose_team(teams):
    print("\nChoose your team:")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team.name}")
    
    while True:
        try:
            choice = int(input("Enter the number of your chosen team: ")) - 1
            if 0 <= choice < len(teams):
                return teams[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
