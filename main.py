from team_management import create_teams, choose_team, display_squad, select_team, generate_sponsorship_offers
from fixtures import generate_fixture_list, save_fixture_list, get_current_week_fixtures, load_fixture_list
from table import create_table
from game_simulation import play_week, simulate_season, simulate_game, simulate_user_match
from stats import stats
from transfer_market import TransferMarket, transfer_market_menu, update_transfer_market
from tactics import Tactics, tactics_menu, select_ai_formation
from colorama import init, Fore, Style

import random
import codecs

# Initialize colorama
init(autoreset=True)

def display_menu():
    print("\nFootball Manager Menu:")
    print("1. Team")
    print("2. Tactics")
    print("3. Fixtures")
    print("4. Transfer Market")
    print("5. Play Game")
    print("6. Table")
    print("7. Simulate Season")
    print("8. Stats")
    print("9. Finances")
    print("10. Injured Players")  # New option
    print("0. Exit")

def display_team_menu():
    print("\nTeam Menu:")
    print("1. View Team")
    print("2. Select Team")
    print("0. Back to Main Menu")

def display_stats_menu():
    print("\nStats Menu:")
    print("1. Player Stats")
    print("2. Club Stats")
    print("0. Back to Main Menu")

def team_menu(player_team):
    while True:
        display_team_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            display_squad(player_team)
        elif choice == "2":
            select_team(player_team)
            print("Team selected successfully.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def stats_menu():
    while True:
        display_stats_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            stats.display_top_scorers()
        elif choice == "2":
            stats.display_club_stats()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def display_finances_menu():
    print("\nFinances Menu:")
    print("1. View Finances")
    print("2. Sponsorships")
    print("3. Bank Loan")
    print("0. Back to Main Menu")

def finances_menu(player_team):
    while True:
        display_finances_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            view_finances(player_team)
        elif choice == "2":
            handle_sponsorships(player_team)
        elif choice == "3":
            handle_bank_loan(player_team)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def view_finances(team):
    print(f"\n{team.name} Finances:")
    print(f"Available Funds: £{team.finances['bank_balance']:,}")
    
    if team.finances['loan']:
        loan = team.finances['loan']
        print("\nActive Loan:")
        print(f"Remaining balance: £{loan['remaining']:,.2f}")
        print(f"Weekly payment: £{loan['weekly_payment']:,.2f}")
        print(f"Weeks left: {loan['weeks_left']}")
    else:
        print("\nNo active loans.")
    
    if team.finances['sponsorship']:
        sponsorship = team.finances['sponsorship']
        print("\nActive Sponsorship:")
        print(f"Sponsor: {sponsorship['sponsor']}")
        print(f"Weekly income: £{sponsorship['weekly_amount']:,}")
        print(f"Weeks left: {sponsorship['weeks_left']}")
    else:
        print("\nNo active sponsorship.")

def handle_sponsorships(team):
    if team.finances['sponsorship']:
        print("\nYou already have an active sponsorship. You can't have multiple sponsorships at the same time.")
        return

    offers = generate_sponsorship_offers()
    
    print("\nSponsorship Offers:")
    for i, offer in enumerate(offers, 1):
        print(f"{i}. {offer['sponsor']}")
        print(f"   Weekly Amount: £{offer['weekly_amount']:,}")
        print(f"   Duration: {offer['duration']} weeks")
        print()
    
    choice = int(input("Enter the number of the sponsorship you want to accept (0 to decline all): ")) - 1
    
    if 0 <= choice < len(offers):
        selected_offer = offers[choice]
        team.add_sponsorship(selected_offer['sponsor'], selected_offer['weekly_amount'], selected_offer['duration'])
        print(f"\nCongratulations! You have accepted the sponsorship offer from {selected_offer['sponsor']}.")
        print(f"You will receive £{selected_offer['weekly_amount']:,} per week for {selected_offer['duration']} weeks.")
    elif choice == -1:
        print("\nYou have declined all sponsorship offers.")
    else:
        print("\nInvalid choice. No sponsorship accepted.")

def handle_bank_loan(team):
    # Read bank names from the file using UTF-8 encoding
    with codecs.open('banks.txt', 'r', encoding='utf-8') as file:
        bank_names = [line.strip() for line in file if line.strip()]
    
    loan_amount = int(input("Enter the amount you want to loan (in pounds): "))
    
    available_banks = random.sample(bank_names, 3)
    
    print("\nChoose a bank for your loan:")
    for i, bank in enumerate(available_banks, 1):
        print(f"{i}. {bank}")
    
    bank_choice = int(input("Enter the number of your chosen bank: ")) - 1
    chosen_bank = available_banks[bank_choice]
    
    loan_duration = random.randint(52, 260)  # 1 to 5 years in weeks
    interest_rate = random.uniform(0.05, 0.15)  # 5% to 15%
    
    total_repayment = loan_amount * (1 + interest_rate)
    weekly_payment = total_repayment / loan_duration
    
    print(f"\nLoan terms from {chosen_bank}:")
    print(f"Loan amount: £{loan_amount:,}")
    print(f"Duration: {loan_duration} weeks")
    print(f"Interest rate: {interest_rate:.2%}")
    print(f"Total repayment: £{total_repayment:,.2f}")
    print(f"Weekly payment: £{weekly_payment:,.2f}")
    
    confirm = input("\nDo you want to accept this loan? (y/n): ")
    if confirm.lower() == 'y':
        team.finances['bank_balance'] += loan_amount
        team.finances['loan'] = {
            'amount': loan_amount,
            'remaining': total_repayment,
            'weekly_payment': weekly_payment,
            'weeks_left': loan_duration
        }
        print(f"\nLoan accepted. £{loan_amount:,} has been added to your bank balance.")
    else:
        print("\nLoan offer declined.")

def display_injured_players(teams):
    print("\nInjured Players List:")
    for team in teams:
        if team.injured_players:
            print(f"\n{team.name}:")
            for player in team.injured_players:
                print(f"  {player.name} - {player.position.name} - Out for {player.injury_weeks_left} week(s)")
        else:
            print(f"\n{team.name}: No injured players")

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

    # Process transfers after all matches have been played
    update_transfer_market(transfer_market, table.teams, player_team)
    
    return current_week + 1

def main():
    teams = create_teams()
    player_team = choose_team(teams)
    transfer_market = TransferMarket()
    
    # Add tactics to each team
    for team in teams:
        team.tactics = Tactics()
        if team != player_team:
            team.tactics.formation = select_ai_formation(team)
    
    # Always generate a new fixture list when starting a new game
    fixtures = generate_fixture_list(teams)
    save_fixture_list(fixtures)
    
    table = create_table(teams)
    current_week = 1
    total_weeks = len(fixtures)

    print("\nWelcome to Football Manager!")
    print("You are managing", player_team.name)
    print("All teams, including yours, will automatically select their best 11 players for each match.")
    print("You can view your team and manually select players, but this won't affect the game simulation.")
    print("In match simulations, players will score goals based on their positions and ratings.")
    print("Forwards have a higher chance of scoring, but any player can potentially score a goal.")
    print("Goal times will be shown for each scorer.")

    while True:
        print(f"\n{Fore.CYAN}Current Week: {current_week}/{total_weeks}{Style.RESET_ALL}")
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            team_menu(player_team)
        elif choice == "2":
            formation_changed = tactics_menu(player_team)
            if formation_changed:
                print("You need to select a new team that fits the new formation.")
                select_team(player_team)
        elif choice == "3":
            print(f"\n{Fore.YELLOW}Fixtures for Week {current_week}:{Style.RESET_ALL}")
            week_fixtures = get_current_week_fixtures(fixtures, current_week)
            for match in week_fixtures:
                print(f"{match['home']} vs {match['away']}")
        elif choice == "4":
            transfer_market_menu(player_team, transfer_market, teams)
        elif choice == "5":
            if current_week <= total_weeks:
                print(f"\n{Fore.GREEN}Results of other matches:{Style.RESET_ALL}")
                current_week = play_week(fixtures, table, current_week, player_team, transfer_market)
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            else:
                print("\nThe season has ended. No more games to play.")
        elif choice == "6":
            table.display()
        elif choice == "7":
            confirm = input(f"Are you sure you want to simulate the remaining {total_weeks - current_week + 1} weeks of the season? (y/n): ")
            if confirm.lower() == 'y':
                simulate_season(fixtures, table, current_week, player_team)
                current_week = total_weeks + 1
            else:
                print("Season simulation cancelled.")
        elif choice == "8":
            stats_menu()
        elif choice == "9":
            finances_menu(player_team)
        elif choice == "10":
            display_injured_players(teams)
        elif choice == "0":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()