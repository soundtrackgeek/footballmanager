import random

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
    team_names = [
        "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
        "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
        "Liverpool", "Luton", "Manchester City", "Manchester United", "Newcastle",
        "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"
    ]
    teams = [Team(name) for name in team_names]
    for team in teams:
        generate_squad(team)
    return teams

def generate_player(position):
    first_names = ["John", "David", "Michael", "James", "William", "Robert", "Richard", "Thomas", "Charles", "Daniel"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return Player(f"{random.choice(first_names)} {random.choice(last_names)}", position)

def generate_squad(team):
    positions = ["GK", "DF", "MF", "FW"]
    for _ in range(20):
        position = random.choice(positions)
        player = generate_player(position)
        team.add_player(player)

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
