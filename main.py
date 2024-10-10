from team_management import create_teams, choose_team
from fixtures import generate_fixture_list, save_fixture_list, get_current_week_fixtures, load_fixture_list
from table import create_table
from game_simulation import play_week, simulate_season

def display_menu():
    print("\nFootball Manager Menu:")
    print("1. Team")
    print("2. Tactics")
    print("3. Fixtures")
    print("4. Transfer Market")
    print("5. Play Game")
    print("6. Table")
    print("7. Simulate Season")
    print("0. Exit")

def main():
    teams = create_teams()
    player_team = choose_team(teams)
    
    fixtures = load_fixture_list()
    if fixtures is None:
        fixtures = generate_fixture_list(teams)
        save_fixture_list(fixtures)
    
    table = create_table(teams)
    current_week = 1
    total_weeks = len(fixtures)

    while True:
        print(f"\nCurrent Week: {current_week}/{total_weeks}")
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nYour Team:")
            for player in player_team.squad:
                print(f"{player.name} - {player.position}")
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
                current_week = play_week(fixtures, table, current_week)
                print("\nWeek completed. Updated table:")
                table.display()
            else:
                print("\nThe season has ended. No more games to play.")
        elif choice == "6":
            table.display()
        elif choice == "7":
            confirm = input(f"Are you sure you want to simulate the remaining {total_weeks - current_week + 1} weeks of the season? (y/n): ")
            if confirm.lower() == 'y':
                simulate_season(fixtures[current_week-1:], table)
                current_week = total_weeks + 1
            else:
                print("Season simulation cancelled.")
        elif choice == "0":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
