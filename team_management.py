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
                [p for p in self.squad if p.position == position],
                key=lambda x: x.rating,
                reverse=True
            )
            self.selected_players.extend(available_players[:count])

        return self.calculate_team_rating()

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
    positions = {
        Position.GK: 3,
        Position.DF: 6,
        Position.MF: 6,
        Position.FW: 5
    }
    for position, count in positions.items():
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
    for i, player in enumerate(team.squad, 1):
        print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")

def select_team(team):
    required_positions = {Position.GK: 1, Position.DF: 4, Position.MF: 4, Position.FW: 2}
    selected_players = []

    print(f"\nSelect 11 players for {team.name}:")
    
    for position, count in required_positions.items():
        print(f"\nSelect {count} {position.name}(s):")
        available_players = [p for p in team.squad if p.position == position and p not in selected_players]
        
        for _ in range(count):
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
    for player in team.selected_players:
        print(f"{player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")
    
    team_rating = team.calculate_team_rating()
    print(f"\nTeam Rating: {team_rating:.2f}")

    return team_rating

def auto_select_team(team):
    team.auto_select_team()

def generate_sponsorship_offers():
    business_names = [
        "AirWave Airlines", "TechTron Solutions", "GreenLeaf Energy",
        "MegaMart Stores", "SwiftStream Internet", "GlobalGear Sports",
        "HealthHub Hospitals", "CrystalClear Beverages", "FutureFinance Bank",
        "EcoEats Restaurants", "SkyHigh Construction", "BrightStar Electronics",
        "RapidRide Automobiles", "CozyHome Furniture", "PetPals Supplies",
        "FitFocus Gyms", "LuxeLook Fashion", "SmartStudy Education",
        "TravelTrends Agency", "MediaMax Entertainment"
    ]
    
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