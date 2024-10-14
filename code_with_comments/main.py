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
    # Display the main menu options for the user
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
    # Display the team management menu options
    print("\nTeam Menu:")
    print("1. View Team")
    print("2. Select Team")
    print("0. Back to Main Menu")

def display_stats_menu():
    # Display the statistics menu options
    print("\nStats Menu:")
    print("1. Player Stats")
    print("2. Club Stats")
    print("0. Back to Main Menu")

def team_menu(player_team):
    # Menu to manage the user's team
    while True:
        display_team_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Display the current squad
            display_squad(player_team)
        elif choice == "2":
            # Allow user to select players for their team
            select_team(player_team)
            print("Team selected successfully.")
        elif choice == "0":
            # Go back to the main menu
            break
        else:
            print("Invalid choice. Please try again.")

def stats_menu():
    # Menu to view statistics related to players and clubs
    while True:
        display_stats_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Display top scorers
            stats.display_top_scorers()
        elif choice == "2":
            # Display club statistics
            stats.display_club_stats()
        elif choice == "0":
            # Go back to the main menu
            break
        else:
            print("Invalid choice. Please try again.")

def display_finances_menu():
    # Display the finances management menu options
    print("\nFinances Menu:")
    print("1. View Finances")
    print("2. Sponsorships")
    print("3. Bank Loan")
    print("0. Back to Main Menu")

def finances_menu(player_team):
    # Menu to manage finances, including sponsorships and loans
    while True:
        display_finances_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # View team's financial details
            view_finances(player_team)
        elif choice == "2":
            # Handle sponsorship offers
            handle_sponsorships(player_team)
        elif choice == "3":
            # Handle taking out a bank loan
            handle_bank_loan(player_team)
        elif choice == "0":
            # Go back to the main menu
            break
        else:
            print("Invalid choice. Please try again.")

def view_finances(team):
    # Display the financial details of the team
    print(f"\n{team.name} Finances:")
    print(f"Available Funds: £{team.finances['bank_balance']:,}")
    
    if team.finances['loan']:
        # Display details of any active loan
        loan = team.finances['loan']
        print("\nActive Loan:")
        print(f"Remaining balance: £{loan['remaining']:,.2f}")
        print(f"Weekly payment: £{loan['weekly_payment']:,.2f}")
        print(f"Weeks left: {loan['weeks_left']}")
    else:
        print("\nNo active loans.")
    
    if team.finances['sponsorship']:
        # Display details of any active sponsorship
        sponsorship = team.finances['sponsorship']
        print("\nActive Sponsorship:")
        print(f"Sponsor: {sponsorship['sponsor']}")
        print(f"Weekly income: £{sponsorship['weekly_amount']:,}")
        print(f"Weeks left: {sponsorship['weeks_left']}")
    else:
        print("\nNo active sponsorship.")

def handle_sponsorships(team):
    # Handle sponsorship offers for the team
    if team.finances['sponsorship']:
        # Check if there is already an active sponsorship
        print("\nYou already have an active sponsorship. You can't have multiple sponsorships at the same time.")
        return

    offers = generate_sponsorship_offers()
    
    print("\nSponsorship Offers:")
    for i, offer in enumerate(offers, 1):
        # Display each sponsorship offer
        print(f"{i}. {offer['sponsor']}")
        print(f"   Weekly Amount: £{offer['weekly_amount']:,}")
        print(f"   Duration: {offer['duration']} weeks")
        print()
    
    choice = int(input("Enter the number of the sponsorship you want to accept (0 to decline all): ")) - 1
    
    if 0 <= choice < len(offers):
        # Accept the chosen sponsorship offer
        selected_offer = offers[choice]
        team.add_sponsorship(selected_offer['sponsor'], selected_offer['weekly_amount'], selected_offer['duration'])
        print(f"\nCongratulations! You have accepted the sponsorship offer from {selected_offer['sponsor']}.")
        print(f"You will receive £{selected_offer['weekly_amount']:,} per week for {selected_offer['duration']} weeks.")
    elif choice == -1:
        # Decline all sponsorship offers
        print("\nYou have declined all sponsorship offers.")
    else:
        # Handle invalid choice
        print("\nInvalid choice. No sponsorship accepted.")

def handle_bank_loan(team):
    # Handle taking out a bank loan
    # Read bank names from the file using UTF-8 encoding
    with codecs.open('banks.txt', 'r', encoding='utf-8') as file:
        bank_names = [line.strip() for line in file if line.strip()]
    
    loan_amount = int(input("Enter the amount you want to loan (in pounds): "))
    
    # Randomly select three available banks
    available_banks = random.sample(bank_names, 3)
    
    print("\nChoose a bank for your loan:")
    for i, bank in enumerate(available_banks, 1):
        # Display the available banks for the loan
        print(f"{i}. {bank}")
    
    bank_choice = int(input("Enter the number of your chosen bank: ")) - 1
    chosen_bank = available_banks[bank_choice]
    
    # Randomly determine the loan duration and interest rate
    loan_duration = random.randint(52, 260)  # 1 to 5 years in weeks
    interest_rate = random.uniform(0.05, 0.15)  # 5% to 15%
    
    # Calculate total repayment and weekly payment
    total_repayment = loan_amount * (1 + interest_rate)
    weekly_payment = total_repayment / loan_duration
    
    # Display loan terms
    print(f"\nLoan terms from {chosen_bank}:")
    print(f"Loan amount: £{loan_amount:,}")
    print(f"Duration: {loan_duration} weeks")
    print(f"Interest rate: {interest_rate:.2%}")
    print(f"Total repayment: £{total_repayment:,.2f}")
    print(f"Weekly payment: £{weekly_payment:,.2f}")
    
    # Ask user to confirm the loan
    confirm = input("\nDo you want to accept this loan? (y/n): ")
    if confirm.lower() == 'y':
        # Update the team's financial details with the new loan
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
    # Display the list of injured players for each team
    print("\nInjured Players List:")
    for team in teams:
        if team.injured_players:
            # Display injured players for the team
            print(f"\n{team.name}:")
            for player in team.injured_players:
                print(f"  {player.name} - {player.position.name} - Out for {player.injury_weeks_left} week(s)")
        else:
            # If no injured players, display a message
            print(f"\n{team.name}: No injured players")

def main():
    # Main function to start the Football Manager game
    teams = create_teams()  # Create all the teams
    player_team = choose_team(teams)  # Let user choose a team to manage
    transfer_market = TransferMarket()  # Initialize the transfer market
    
    # Add tactics to each team
    for team in teams:
        team.tactics = Tactics()  # Initialize tactics for each team
        if team != player_team:
            team.tactics.formation = select_ai_formation(team)  # Select AI formation for non-player teams
    
    # Generate a new fixture list when starting a new game
    fixtures = generate_fixture_list(teams)
    save_fixture_list(fixtures)
    
    table = create_table(teams)  # Create the league table
    current_week = 1  # Start at week 1
    total_weeks = len(fixtures)  # Total number of weeks in the season

    # Display welcome message
    print("\nWelcome to Football Manager!")
    print("You are managing", player_team.name)
    print("All teams, including yours, will automatically select their best 11 players for each match.")
    print("You can view your team and manually select players, but this won't affect the game simulation.")
    print("In match simulations, players will score goals based on their positions and ratings.")
    print("Forwards have a higher chance of scoring, but any player can potentially score a goal.")
    print("Goal times will be shown for each scorer.")

    # Main game loop
    while True:
        # Display current week and menu options
        print(f"\n{Fore.CYAN}Current Week: {current_week}/{total_weeks}{Style.RESET_ALL}")
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Access team menu
            team_menu(player_team)
        elif choice == "2":
            # Access tactics menu
            formation_changed = tactics_menu(player_team)
            if formation_changed:
                # Prompt user to select a new team if the formation has changed
                print("You need to select a new team that fits the new formation.")
                select_team(player_team)
        elif choice == "3":
            # Display current week's fixtures
            print(f"\n{Fore.YELLOW}Fixtures for Week {current_week}:{Style.RESET_ALL}")
            week_fixtures = get_current_week_fixtures(fixtures, current_week)
            for match in week_fixtures:
                print(f"{match['home']} vs {match['away']}")
        elif choice == "4":
            # Access transfer market menu
            transfer_market_menu(player_team, transfer_market, teams)
        elif choice == "5":
            # Play the current week's matches
            if current_week <= total_weeks:
                print(f"\n{Fore.GREEN}Results of other matches:{Style.RESET_ALL}")
                current_week = play_week(fixtures, table, current_week, player_team, transfer_market)
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            else:
                # If the season is over, no more games to play
                print("\nThe season has ended. No more games to play.")
        elif choice == "6":
            # Display the league table
            table.display()
        elif choice == "7":
            # Simulate the remaining weeks of the season
            confirm = input(f"Are you sure you want to simulate the remaining {total_weeks - current_week + 1} weeks of the season? (y/n): ")
            if confirm.lower() == 'y':
                simulate_season(fixtures, table, current_week, player_team)
                current_week = total_weeks + 1  # Set current week to after the season ends
            else:
                print("Season simulation cancelled.")
        elif choice == "8":
            # Access stats menu
            stats_menu()
        elif choice == "9":
            # Access finances menu
            finances_menu(player_team)
        elif choice == "10":
            # Display injured players
            display_injured_players(teams)
        elif choice == "0":
            # Exit the game
            print("Thank you for playing. Goodbye!")
            break
        else:
            # Handle invalid menu choice
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()