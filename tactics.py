from enum import Enum

class Formation(Enum):
    F_4_4_2 = "4-4-2"
    F_4_3_3 = "4-3-3"
    F_4_2_4 = "4-2-4"
    F_5_4_1 = "5-4-1"
    F_4_5_1 = "4-5-1"
    F_5_3_2 = "5-3-2"

class Tactics:
    def __init__(self):
        self.formation = Formation.F_4_4_2  # Default formation

    def get_formation_requirements(self):
        requirements = {
            Formation.F_4_4_2: {"DF": 4, "MF": 4, "FW": 2},
            Formation.F_4_3_3: {"DF": 4, "MF": 3, "FW": 3},
            Formation.F_4_2_4: {"DF": 4, "MF": 2, "FW": 4},
            Formation.F_5_4_1: {"DF": 5, "MF": 4, "FW": 1},
            Formation.F_4_5_1: {"DF": 4, "MF": 5, "FW": 1},
            Formation.F_5_3_2: {"DF": 5, "MF": 3, "FW": 2},
        }
        return requirements[self.formation]

def display_tactics_menu():
    print("\nTactics Menu:")
    print("1. Formation")
    print("2. Style (Not implemented yet)")
    print("0. Back to Main Menu")

def display_formation_menu():
    print("\nFormation Menu:")
    for i, formation in enumerate(Formation, 1):
        print(f"{i}. {formation.value}")
    print("0. Back to Tactics Menu")

def change_formation(team):
    display_formation_menu()
    choice = input("Enter your choice: ")
    
    if choice == "0":
        return False
    
    try:
        formation_index = int(choice) - 1
        if 0 <= formation_index < len(Formation):
            new_formation = list(Formation)[formation_index]
            team.tactics.formation = new_formation
            print(f"Formation changed to {new_formation.value}")
            team.selected_players = []  # Clear the selected players
            print("Please select a new team that fits the new formation.")
            return True
        else:
            print("Invalid choice. Please try again.")
            return False
    except ValueError:
        print("Invalid input. Please enter a number.")
        return False

def tactics_menu(team):
    while True:
        display_tactics_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            changed = change_formation(team)
            if changed:
                return True  # Indicate that the formation was changed
        elif choice == "2":
            print("\nStyle options are not implemented yet.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
    
    return False  # Indicate that no changes were made

def select_ai_formation(team):
    # Count the number of players in each position
    position_counts = {
        "DF": sum(1 for player in team.squad if player.position.name == "DF"),
        "MF": sum(1 for player in team.squad if player.position.name == "MF"),
        "FW": sum(1 for player in team.squad if player.position.name == "FW")
    }

    # Determine the best formation based on the squad composition
    if position_counts["FW"] >= 3:
        return Formation.F_4_3_3
    elif position_counts["MF"] >= 5:
        return Formation.F_4_5_1
    elif position_counts["DF"] >= 5:
        return Formation.F_5_3_2
    else:
        return Formation.F_4_4_2  # Default to 4-4-2 if no clear advantage
