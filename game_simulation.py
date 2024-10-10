import random

def simulate_game(home_team, away_team):
    home_goals = random.randint(0, 5)
    away_goals = random.randint(0, 5)
    return home_goals, away_goals

def play_week(fixtures, table, current_week):
    week_fixtures = fixtures[current_week - 1]["matches"]
    print(f"\nWeek {current_week} Results:")
    for match in week_fixtures:
        home_team = match["home"]
        away_team = match["away"]
        home_goals, away_goals = simulate_game(home_team, away_team)
        table.update(home_team, away_team, home_goals, away_goals)
        print(f"{home_team} {home_goals} - {away_goals} {away_team}")
    table.display()
    return current_week + 1

def simulate_season(remaining_fixtures, table):
    for week, fixtures in enumerate(remaining_fixtures, start=1):
        print(f"\nSimulating Week {week}")
        play_week(fixtures, table, week)
        input("Press Enter to continue to the next week...")
    print("\nSeason completed!")
