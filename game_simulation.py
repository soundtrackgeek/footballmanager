import random

def simulate_game(home_team, away_team):
    home_goals = random.randint(0, 5)
    away_goals = random.randint(0, 5)
    return home_goals, away_goals

def play_week(fixtures, table, current_week):
    week_fixtures = fixtures[current_week - 1]["matches"]
    for match in week_fixtures:
        home_team = match["home"]
        away_team = match["away"]
        home_goals, away_goals = simulate_game(home_team, away_team)
        table.update(home_team, away_team, home_goals, away_goals)
        print(f"{home_team} {home_goals} - {away_goals} {away_team}")
    return current_week + 1

def simulate_season(fixtures, table):
    current_week = 1
    while current_week <= 38:
        print(f"\nSimulating Week {current_week}")
        current_week = play_week(fixtures, table, current_week)
        input("Press Enter to continue to the next week...")
    print("\nSeason completed!")
