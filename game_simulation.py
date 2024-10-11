import random
from team_management import select_team, auto_select_team

def determine_goal_scorer(team):
    weights = {'FW': 0.6, 'MF': 0.3, 'DF': 0.08, 'GK': 0.02}
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
                auto_select_team(player_team)

        home_goals, away_goals, home_scorers, away_scorers = simulate_game(home_team, away_team)
        table.update(home_team_name, away_team_name, home_goals, away_goals)
        
        print(f"\n{home_team_name} {home_goals} - {away_goals} {away_team_name}")
        if home_scorers:
            print(f"{home_team_name} scorers:")
            for scorer, minute in home_scorers:
                print(f"  {scorer.name} ({minute}')")
        if away_scorers:
            print(f"{away_team_name} scorers:")
            for scorer, minute in away_scorers:
                print(f"  {scorer.name} ({minute}')")

    return current_week + 1

def simulate_season(fixtures, table, start_week, player_team):
    total_weeks = len(fixtures)
    for week in range(start_week, total_weeks + 1):
        print(f"\nSimulating Week {week}")
        play_week(fixtures, table, week, player_team)
        if week < total_weeks:
            input("Press Enter to continue to the next week...")
    print("\nSeason completed!")
