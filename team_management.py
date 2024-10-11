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
        self.selected_players = []

    def add_player(self, player):
        self.squad.append(player)

    def calculate_team_rating(self):
        if not self.selected_players:
            return 0
        return sum(player.rating for player in self.selected_players) / len(self.selected_players)

    def auto_select_team(self):
        required_positions = {"GK": 1, "DF": 4, "MF": 4, "FW": 2}
        self.selected_players = []

        for position, count in required_positions.items():
            available_players = sorted(
                [p for p in self.squad if p.position == position],
                key=lambda x: x.rating,
                reverse=True
            )
            self.selected_players.extend(available_players[:count])

        return self.calculate_team_rating()

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

def display_squad(team):
    print(f"\n{team.name} Squad:")
    for i, player in enumerate(team.squad, 1):
        print(f"{i}. {player.name} - {player.position} - Rating: {player.rating}")

def select_team(team):
    required_positions = {"GK": 1, "DF": 4, "MF": 4, "FW": 2}
    selected_players = []

    print(f"\nSelect 11 players for {team.name}:")
    
    for position, count in required_positions.items():
        print(f"\nSelect {count} {position}(s):")
        available_players = [p for p in team.squad if p.position == position and p not in selected_players]
        
        for _ in range(count):
            display_squad = [p for p in available_players if p not in selected_players]
            for i, player in enumerate(display_squad, 1):
                print(f"{i}. {player.name} - Rating: {player.rating}")
            
            while True:
                try:
                    choice = int(input(f"Select player {len(selected_players) + 1}: ")) - 1
                    if 0 <= choice < len(display_squad):
                        selected_players.append(display_squad[choice])
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

    team.selected_players = selected_players
    print("\nSelected Team:")
    for player in team.selected_players:
        print(f"{player.name} - {player.position} - Rating: {player.rating}")
    
    team_rating = team.calculate_team_rating()
    print(f"\nTeam Rating: {team_rating:.2f}")

    return team_rating

def auto_select_team(team):
    team.auto_select_team()
