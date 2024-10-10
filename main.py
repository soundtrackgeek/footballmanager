from team_management import create_teams, choose_team
from fixtures import generate_fixture_list, save_fixture_list, get_current_week_fixtures, load_fixture_list

def display_menu():
    print("\nFootball Manager Menu:")
    print("1. Team")
    print("2. Tactics")
    print("3. Fixtures")
    print("4. Transfer Market")
    print("5. Play Game")
    print("0. Exit")

def main():
    teams = create_teams()
    player_team = choose_team(teams)
    
    fixtures = load_fixture_list()
    if fixtures is None:
        fixtures = generate_fixture_list(teams)
        save_fixture_list(fixtures)
    
    current_week = 1

    while True:
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
            print("\nPlay Game feature not implemented yet.")
        elif choice == "0":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
