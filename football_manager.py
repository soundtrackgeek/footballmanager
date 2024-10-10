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
    teams = [
        "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
        "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
        "Liverpool", "Luton", "Manchester City", "Manchester United", "Newcastle",
        "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"
    ]
    return [Team(name) for name in teams]

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

def main():
    teams = create_teams()
    for team in teams:
        generate_squad(team)
    
    print("Welcome to Football Manager!")
    num_players = int(input("Enter the number of players (1-4): "))
    
    for i in range(num_players):
        print(f"\nPlayer {i+1}, choose your team:")
        for j, team in enumerate(teams):
            print(f"{j+1}. {team.name}")
        
        choice = int(input("Enter the number of your chosen team: ")) - 1
        chosen_team = teams.pop(choice)
        print(f"Player {i+1} has chosen {chosen_team.name}")
        
        print("\nYour squad:")
        for player in chosen_team.squad:
            print(f"{player.name} - {player.position}")

if __name__ == "__main__":
    main()
