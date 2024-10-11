from team_management import create_teams, choose_team, display_squad, select_team
from fixtures import generate_fixture_list, save_fixture_list, get_current_week_fixtures, load_fixture_list
from table import create_table
from game_simulation import play_week, simulate_season
from stats import stats

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

def main():
    teams = create_teams()
    player_team = choose_team(teams)
    
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
        print(f"\nCurrent Week: {current_week}/{total_weeks}")
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            team_menu(player_team)
        elif choice == "2":
            print("\nTactics feature not implemented yet.")
        elif choice == "3":
            print(f"\nFixtures for Week {current_week}:")
            week_fixtures = get_current_week_fixtures(fixtures, current_week)
            for match in week_fixtures:
                print(f"{match['home']} vs {match['away']}")
        elif choice == "4":
            print("\nTransfer Market feature not implemented yet.")
        elif choice == "5":
            if current_week <= total_weeks:
                print(f"\nSimulating Week {current_week}")
                current_week = play_week(fixtures, table, current_week, player_team)
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
        elif choice == "0":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
