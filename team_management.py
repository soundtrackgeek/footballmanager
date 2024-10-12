import random
import json
import os
from player import Player, Position

# Add this dictionary at the top of the file, after the imports
STADIUMS = {
    "Arsenal": {"name": "Emirates Stadium", "capacity": 60704},
    "Aston Villa": {"name": "Villa Park", "capacity": 42785},
    "Bournemouth": {"name": "Vitality Stadium", "capacity": 11379},
    "Brentford": {"name": "Gtech Community Stadium", "capacity": 17250},
    "Brighton": {"name": "Amex Stadium", "capacity": 31800},
    "Burnley": {"name": "Turf Moor", "capacity": 21944},
    "Chelsea": {"name": "Stamford Bridge", "capacity": 40341},
    "Crystal Palace": {"name": "Selhurst Park", "capacity": 25486},
    "Everton": {"name": "Goodison Park", "capacity": 39572},
    "Fulham": {"name": "Craven Cottage", "capacity": 25700},
    "Liverpool": {"name": "Anfield", "capacity": 53394},
    "Luton": {"name": "Kenilworth Road", "capacity": 10356},
    "Manchester City": {"name": "Etihad Stadium", "capacity": 53400},
    "Manchester United": {"name": "Old Trafford", "capacity": 74140},
    "Newcastle": {"name": "St James' Park", "capacity": 52305},
    "Nottingham Forest": {"name": "City Ground", "capacity": 30445},
    "Sheffield United": {"name": "Bramall Lane", "capacity": 32050},
    "Tottenham": {"name": "Tottenham Hotspur Stadium", "capacity": 62850},
    "West Ham": {"name": "London Stadium", "capacity": 60000},
    "Wolves": {"name": "Molineux Stadium", "capacity": 31750}
}

class Team:
    def __init__(self, name):
        self.name = name
        self.squad = []
        self.selected_players = []
        self.finances = {
            'bank_balance': random.randint(20_000_000, 100_000_000),
            'loan': None,
            'sponsorship': None
        }
        self.stadium = STADIUMS[name]
        self.injured_players = []

    def add_player(self, player):
        self.squad.append(player)

    def calculate_team_rating(self):
        if not self.selected_players:
            return 0
        return sum(player.rating for player in self.selected_players) / len(self.selected_players)

    def auto_select_team(self):
        required_positions = {Position.GK: 1, Position.DF: 4, Position.MF: 4, Position.FW: 2}
        self.selected_players = []

        for position, count in required_positions.items():
            available_players = sorted(
                [p for p in self.squad if p.position == position and not p.injured],
                key=lambda x: x.rating,
                reverse=True
            )
            self.selected_players.extend(available_players[:count])

        return self.calculate_team_rating()

    def handle_injuries(self):
        for player in self.injured_players:
            player.injury_weeks_left -= 1
            if player.injury_weeks_left == 0:
                player.injured = False
                self.injured_players.remove(player)
                print(f"{player.name} has recovered from injury and is available for selection.")

    def injure_players(self):
        if random.random() < 0.1:  # 10% chance of injuries occurring
            num_injuries = random.randint(1, 2)
            for _ in range(num_injuries):
                if self.selected_players:
                    player = random.choice(self.selected_players)
                    if not player.injured and self.can_injure_player(player):
                        player.injured = True
                        player.injury_weeks_left = random.randint(1, 8)
                        self.injured_players.append(player)
                        print(f"{player.name} has been injured for {player.injury_weeks_left} weeks.")

    def can_injure_player(self, player):
        healthy_players_in_position = sum(1 for p in self.squad if p.position == player.position and not p.injured)
        return healthy_players_in_position > 4

    def add_sponsorship(self, sponsor, weekly_amount, duration):
        self.finances['sponsorship'] = {
            'sponsor': sponsor,
            'weekly_amount': weekly_amount,
            'duration': duration,
            'weeks_left': duration
        }

    def calculate_match_attendance(self):
        capacity = self.stadium["capacity"]
        attendance_percentage = random.uniform(0.75, 0.99)  # Between 75% and 99% capacity
        return int(capacity * attendance_percentage)

def create_teams():
    team_names = list(STADIUMS.keys())  # Use the keys from the STADIUMS dictionary
    teams = [Team(name) for name in team_names]
    for team in teams:
        generate_squad(team)
        save_team_to_file(team)
    return teams

def generate_squad(team):
    positions = ["GK", "DF", "MF", "FW"]
    position_counts = {
        "GK": 3,
        "DF": 6,
        "MF": 6,
        "FW": 5
    }
    for position, count in position_counts.items():
        for _ in range(count):
            player = Player.generate_player(position)
            team.add_player(player)

def save_team_to_file(team):
    team_data = {
        "name": team.name,
        "squad": [{"name": player.name, "position": player.position.name, "rating": player.rating, "age": player.age, "value": player.value} for player in team.squad],
        "stadium": team.stadium
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
    
    # Display selected players first
    if team.selected_players:
        print("\nSelected Starting XI:")
        for i, player in enumerate(team.selected_players, 1):
            print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")
    
    # Display unselected players
    print("\nOther Squad Players:")
    unselected_players = [p for p in team.squad if p not in team.selected_players]
    for i, player in enumerate(unselected_players, len(team.selected_players) + 1):
        print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")

def select_team(team):
    required_positions = {Position.GK: 1, Position.DF: 4, Position.MF: 4, Position.FW: 2}
    selected_players = []

    print(f"\nSelect 11 players for {team.name}:")
    
    # Handle injured players first
    if team.injured_players:
        print("\nInjured players:")
        for injured_player in team.injured_players:
            print(f"{injured_player.name} - {injured_player.position.name} - Out for {injured_player.injury_weeks_left} weeks")
            available_replacements = [p for p in team.squad if p.position == injured_player.position and not p.injured and p not in selected_players]
            print("\nAvailable replacements:")
            for i, player in enumerate(available_replacements, 1):
                print(f"{i}. {player.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")
            
            while True:
                try:
                    choice = int(input(f"Select replacement for {injured_player.name}: ")) - 1
                    if 0 <= choice < len(available_replacements):
                        selected_players.append(available_replacements[choice])
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

    # Select remaining players
    for position, count in required_positions.items():
        remaining_count = count - sum(1 for p in selected_players if p.position == position)
        if remaining_count > 0:
            print(f"\nSelect {remaining_count} {position.name}(s):")
            available_players = [p for p in team.squad if p.position == position and not p.injured and p not in selected_players]
            
            for _ in range(remaining_count):
                display_squad = [p for p in available_players if p not in selected_players]
                for i, player in enumerate(display_squad, 1):
                    print(f"{i}. {player.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")
                
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
    for i, player in enumerate(team.selected_players, 1):
        print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")
    
    team_rating = team.calculate_team_rating()
    print(f"\nTeam Rating: {team_rating:.2f}")

    return team_rating

def auto_select_team(team):
    team.auto_select_team()

def generate_sponsorship_offers():
    # Read sponsor names from the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sponsors_file = os.path.join(script_dir, 'sponsors.txt')
    
    with open(sponsors_file, 'r', encoding='utf-8') as f:
        business_names = [line.strip() for line in f if line.strip()]
    
    # Randomly select 3 sponsors
    selected_businesses = random.sample(business_names, 3)
    offers = []
    
    for business in selected_businesses:
        weekly_amount = random.randint(50_000, 500_000)
        duration = random.randint(10, 52)  # 10 weeks to 1 year
        offers.append({
            'sponsor': business,
            'weekly_amount': weekly_amount,
            'duration': duration
        })
    
    return offers
