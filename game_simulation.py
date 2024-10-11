import random
from team_management import select_team, auto_select_team

def simulate_game(home_team, away_team):
    home_rating = home_team.calculate_team_rating()
    away_rating = away_team.calculate_team_rating()
    
    rating_difference = home_rating - away_rating
    home_advantage = 5  # Home team gets a slight advantage

    home_strength = max(0, 50 + rating_difference + home_advantage)
    away_strength = max(0, 50 - rating_difference)

    home_goals = random.randint(0, int(home_strength / 10))
    away_goals = random.randint(0, int(away_strength / 10))

    return home_goals, away_goals

def play_week(fixtures, table, current_week, player_team):
    week_fixtures = fixtures[current_week - 1]["matches"]
    print(f"\nWeek {current_week} Results:")
    for match in week_fixtures:
        home_team_name = match["home"]
        away_team_name = match["away"]
        
        home_team = next(team for team in table.teams if team.name == home_team_name)
        away_team = next(team for team in table.teams if team.name == away_team_name)

        # Auto-select team for AI-controlled teams
        if home_team != player_team:
            auto_select_team(home_team)
        if away_team != player_team:
            auto_select_team(away_team)

        # Handle player's team selection
        if home_team == player_team or away_team == player_team:
            if not player_team.selected_players:
                print(f"Please select your team for the match: {home_team_name} vs {away_team_name}")
                select_team(player_team)

        home_goals, away_goals = simulate_game(home_team, away_team)
        table.update(home_team_name, away_team_name, home_goals, away_goals)
        print(f"{home_team_name} {home_goals} - {away_goals} {away_team_name}")
    table.display()
    return current_week + 1

def simulate_season(fixtures, table, start_week, player_team):
    total_weeks = len(fixtures)
    for week in range(start_week, total_weeks + 1):
        print(f"\nSimulating Week {week}")
        play_week(fixtures, table, week, player_team)
        if week < total_weeks:
            input("Press Enter to continue to the next week...")
    print("\nSeason completed!")
