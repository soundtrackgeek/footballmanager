import random
import time
from team_management import select_team, auto_select_team
from stats import stats
from player import Position
from colorama import init, Fore, Back, Style
from fixtures import get_current_week_fixtures  # Add this import
from transfer_market import update_transfer_market  # Add this import as well

# Initialize colorama
init(autoreset=True)

# Load commentator lines from file
def load_commentator_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Load the commentator lines at the beginning of the script
commentator_lines = load_commentator_lines('commentatorgoals.txt')

def determine_goal_scorer(team):
    weights = {Position.FW: 0.6, Position.MF: 0.3, Position.DF: 0.08, Position.GK: 0.02}
    players = team.selected_players
    weighted_players = [(p, weights[p.position] * p.rating) for p in players]
    total_weight = sum(w for _, w in weighted_players)
    r = random.uniform(0, total_weight)
    current_sum = 0
    for player, weight in weighted_players:
        current_sum += weight
        if r <= current_sum:
            return player
    return players[-1]  # Fallback to last player if something goes wrong

def simulate_game(home_team, away_team):
    home_rating = home_team.calculate_team_rating()
    away_rating = away_team.calculate_team_rating()
    
    rating_difference = home_rating - away_rating
    home_advantage = 5  # Home team gets a slight advantage

    home_strength = max(0, 50 + rating_difference + home_advantage)
    away_strength = max(0, 50 - rating_difference)

    home_goals = random.randint(0, int(home_strength / 10))
    away_goals = random.randint(0, int(away_strength / 10))

    home_scorers = []
    away_scorers = []

    for _ in range(home_goals):
        scorer = determine_goal_scorer(home_team)
        minute = random.randint(1, 90)
        home_scorers.append((scorer, minute))

    for _ in range(away_goals):
        scorer = determine_goal_scorer(away_team)
        minute = random.randint(1, 90)
        away_scorers.append((scorer, minute))

    home_scorers.sort(key=lambda x: x[1])
    away_scorers.sort(key=lambda x: x[1])

    return home_goals, away_goals, home_scorers, away_scorers

def calculate_ticket_revenue(team, attendance):
    ticket_prices = {
        "Manchester City": 75, "Liverpool": 70, "Manchester United": 70, "Arsenal": 65,
        "Chelsea": 65, "Tottenham": 60, "Newcastle": 55, "West Ham": 55,
        "Aston Villa": 50, "Brighton": 50, "Everton": 45, "Wolves": 45,
        "Crystal Palace": 40, "Fulham": 40, "Brentford": 35, "Nottingham Forest": 35,
        "Bournemouth": 30, "Burnley": 30, "Sheffield United": 30, "Luton": 25
    }
    
    ticket_price = ticket_prices.get(team.name, 40)  # Default to 40 if team not found
    return attendance * ticket_price

def simulate_user_match(home_team, away_team):
    home_rating = home_team.calculate_team_rating()
    away_rating = away_team.calculate_team_rating()
    
    rating_difference = home_rating - away_rating
    home_advantage = 5  # Home team gets a slight advantage

    home_strength = max(0, 50 + rating_difference + home_advantage)
    away_strength = max(0, 50 - rating_difference)

    home_goals = 0
    away_goals = 0
    home_scorers = []
    away_scorers = []

    print(f"\nExciting match: {Fore.CYAN}{home_team.name}{Style.RESET_ALL} vs {Fore.CYAN}{away_team.name}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Kick-off!{Style.RESET_ALL}\n")

    for minute in range(1, 91):
        time.sleep(0.2)  # Simulate 0.2 seconds per minute
        print(f"\rMinute {minute:2d}: {home_team.name} {home_goals} - {away_goals} {away_team.name}", end="", flush=True)

        # Simulate goal chances
        if random.random() < 0.05:  # 5% chance of a goal attempt each minute
            if random.random() < home_strength / (home_strength + away_strength):
                scorer = determine_goal_scorer(home_team)
                home_goals += 1
                home_scorers.append((scorer, minute))
                print(f"\n\n{Fore.YELLOW}Minute {minute}: {home_team.name} {home_goals} - {away_goals} {away_team.name}{Style.RESET_ALL}")
                goal_message = f"GOAL! {scorer.name} scores for {home_team.name}!"
                for i in range(6):  # Increase the number of flashes
                    if i % 2 == 0:
                        print(f"{Fore.RED}{Back.WHITE}{goal_message}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}{goal_message}{Style.RESET_ALL}")
                    time.sleep(0.3)  # Slightly faster flashing
                    print("\033[A\033[K", end="")  # Clear the previous line
                print(f"{Fore.RED}{goal_message}{Style.RESET_ALL}")  # Print the message one last time
                print(f"{Fore.MAGENTA}{random.choice(commentator_lines)}{Style.RESET_ALL}\n")
            else:
                scorer = determine_goal_scorer(away_team)
                away_goals += 1
                away_scorers.append((scorer, minute))
                print(f"\n\n{Fore.YELLOW}Minute {minute}: {home_team.name} {home_goals} - {away_goals} {away_team.name}{Style.RESET_ALL}")
                goal_message = f"GOAL! {scorer.name} scores for {away_team.name}!"
                for i in range(6):  # Increase the number of flashes
                    if i % 2 == 0:
                        print(f"{Fore.RED}{Back.WHITE}{goal_message}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}{goal_message}{Style.RESET_ALL}")
                    time.sleep(0.3)  # Slightly faster flashing
                    print("\033[A\033[K", end="")  # Clear the previous line
                print(f"{Fore.RED}{goal_message}{Style.RESET_ALL}")  # Print the message one last time
                print(f"{Fore.MAGENTA}{random.choice(commentator_lines)}{Style.RESET_ALL}\n")

    print(f"\n{Fore.GREEN}Full-time: {home_team.name} {home_goals} - {away_goals} {away_team.name}{Style.RESET_ALL}")
    return home_goals, away_goals, home_scorers, away_scorers

def ensure_full_team(team):
    if len(team.selected_players) < 11:
        print(f"{team.name} doesn't have a full team selected. Selecting additional players...")
        available_players = [p for p in team.squad if p not in team.selected_players]
        
        while len(team.selected_players) < 11 and available_players:
            needed_position = get_needed_position(team.selected_players)
            suitable_players = [p for p in available_players if p.position == needed_position]
            
            if suitable_players:
                selected_player = max(suitable_players, key=lambda p: p.rating)
            else:
                selected_player = max(available_players, key=lambda p: p.rating)
            
            team.selected_players.append(selected_player)
            available_players.remove(selected_player)
            print(f"Added {selected_player.name} ({selected_player.position.name}) to the team.")

def get_needed_position(selected_players):
    position_counts = {Position.GK: 0, Position.DF: 0, Position.MF: 0, Position.FW: 0}
    for player in selected_players:
        position_counts[player.position] += 1
    
    if position_counts[Position.GK] < 1:
        return Position.GK
    elif position_counts[Position.DF] < 4:
        return Position.DF
    elif position_counts[Position.MF] < 4:
        return Position.MF
    else:
        return Position.FW

def play_week(fixtures, table, current_week, player_team, transfer_market):
    print(f"\n{Fore.CYAN}Preparing for Week {current_week}{Style.RESET_ALL}")
    
    # Handle injuries and team selection for all teams
    for team in table.teams:
        team.handle_injuries()
        if team != player_team:
            team.auto_select_team()
        else:
            team.check_and_replace_unavailable_players()

    if not player_team.selected_players:
        print("You haven't selected your team yet. Please select your team now.")
        select_team(player_team)
    
    # Check if the player's team has 11 players
    while len(player_team.selected_players) < 11:
        missing_position = player_team.get_missing_position()
        if missing_position is None:
            print("Error: Unable to determine missing position. Please select your entire team manually.")
            select_team(player_team)
            break
        print(f"Your team is missing a {missing_position}. Please select a replacement.")
        available_players = player_team.get_available_players(missing_position)
        if not available_players:
            print(f"No available {missing_position} players. You need to transfer in a new player or change your formation.")
            return current_week  # Return without playing the match

        print("\nCurrent team:")
        for i, player in enumerate(player_team.selected_players, 1):
            print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating}")
        avg_rating = player_team.calculate_team_rating()
        print(f"\nCurrent Team Average Rating: {avg_rating:.2f}")

        player_team.replace_missing_player(missing_position)

    print("Your team is ready for the match. Here's your current lineup:")
    for i, player in enumerate(player_team.selected_players, 1):
        print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating}")
    avg_rating = player_team.calculate_team_rating()
    print(f"\nTeam Average Rating: {avg_rating:.2f}")
    
    change = input("Do you want to make any changes to your lineup? (y/n): ")
    if change.lower() == 'y':
        select_team(player_team)

    print(f"\n{Fore.YELLOW}Simulating Week {current_week}{Style.RESET_ALL}")
    week_fixtures = get_current_week_fixtures(fixtures, current_week)
    
    # Simulate all matches
    for match in week_fixtures:
        home_team = next(team for team in table.teams if team.name == match['home'])
        away_team = next(team for team in table.teams if team.name == match['away'])
        
        if home_team == player_team or away_team == player_team:
            print(f"\n{Fore.CYAN}Your match:{Style.RESET_ALL}")
            home_goals, away_goals, home_scorers, away_scorers = simulate_user_match(home_team, away_team)
        else:
            home_goals, away_goals, home_scorers, away_scorers = simulate_game(home_team, away_team)
            print(f"\n{Fore.GREEN}{home_team.name} {home_goals} - {away_goals} {away_team.name}{Style.RESET_ALL}")
        
        for scorer, minute in home_scorers:
            print(f"{Fore.YELLOW}Goal! {scorer.name} scores for {home_team.name} ({minute}'){Style.RESET_ALL}")
        for scorer, minute in away_scorers:
            print(f"{Fore.YELLOW}Goal! {scorer.name} scores for {away_team.name} ({minute}'){Style.RESET_ALL}")
        
        # Simulate injuries for both teams after the match
        home_team.injure_players()
        away_team.injure_players()
        
        # Display injuries
        if home_team.injured_players or away_team.injured_players:
            print(f"\n{Fore.RED}Injuries:{Style.RESET_ALL}")
            if home_team.injured_players:
                print(f"{Fore.RED}For {home_team.name}:{Style.RESET_ALL}")
                for player in home_team.injured_players:
                    print(f"{Fore.RED}- {player.name} - {player.injury_weeks_left} weeks{Style.RESET_ALL}")
            if away_team.injured_players:
                print(f"{Fore.RED}For {away_team.name}:{Style.RESET_ALL}")
                for player in away_team.injured_players:
                    print(f"{Fore.RED}- {player.name} - {player.injury_weeks_left} weeks{Style.RESET_ALL}")
        
        table.update(match['home'], match['away'], home_goals, away_goals)
        stats.update_goal_scorers(home_scorers)
        stats.update_goal_scorers(away_scorers)
        stats.update_club_stats(match['home'], match['away'], home_goals, away_goals)

    update_transfer_market(transfer_market, table.teams)
    return current_week + 1

def update_team_finances(team, weekly_financial_summary):
    if team.name not in weekly_financial_summary:
        weekly_financial_summary[team.name] = {'ticket_revenue': 0, 'sponsorship': 0, 'loan_payment': 0}
    
    # Handle sponsorship
    if team.finances['sponsorship']:
        sponsorship = team.finances['sponsorship']
        sponsorship_income = sponsorship['weekly_amount']
        team.finances['bank_balance'] += sponsorship_income
        weekly_financial_summary[team.name]['sponsorship'] = sponsorship_income
        sponsorship['weeks_left'] -= 1
        
        if sponsorship['weeks_left'] == 0:
            print(f"\n{team.name}'s sponsorship with {sponsorship['sponsor']} has ended.")
            team.finances['sponsorship'] = None

    # Handle loan repayment
    if team.finances['loan']:
        loan = team.finances['loan']
        loan_payment = loan['weekly_payment']
        team.finances['bank_balance'] -= loan_payment
        weekly_financial_summary[team.name]['loan_payment'] = loan_payment
        loan['remaining'] -= loan_payment
        loan['weeks_left'] -= 1
        
        if loan['weeks_left'] == 0:
            print(f"\n{team.name} has fully repaid their loan.")
            team.finances['loan'] = None

    # Add ticket revenue to bank balance
    team.finances['bank_balance'] += weekly_financial_summary[team.name]['ticket_revenue']

def simulate_season(fixtures, table, start_week, player_team):
    total_weeks = len(fixtures)
    for week in range(start_week, total_weeks + 1):
        print(f"\nSimulating Week {week}")
        play_week(fixtures, table, week, player_team)
        if week < total_weeks:
            input("Press Enter to continue to the next week...")
    print("\nSeason completed!")