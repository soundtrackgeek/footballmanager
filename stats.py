class Stats:
    def __init__(self):
        self.goal_scorers = {}
        self.club_wins = {team: 0 for team in ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
                                               "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham",
                                               "Liverpool", "Luton", "Manchester City", "Manchester United", "Newcastle",
                                               "Nottingham Forest", "Sheffield United", "Tottenham", "West Ham", "Wolves"]}
        self.club_losses = {team: 0 for team in self.club_wins.keys()}

    def update_goal_scorers(self, scorers):
        for scorer, _ in scorers:
            if scorer.name in self.goal_scorers:
                self.goal_scorers[scorer.name] += 1
            else:
                self.goal_scorers[scorer.name] = 1

    def update_club_stats(self, home_team, away_team, home_goals, away_goals):
        if home_goals > away_goals:
            self.club_wins[home_team] += 1
            self.club_losses[home_team] = 0
            self.club_wins[away_team] = 0
            self.club_losses[away_team] += 1
        elif away_goals > home_goals:
            self.club_wins[away_team] += 1
            self.club_losses[away_team] = 0
            self.club_wins[home_team] = 0
            self.club_losses[home_team] += 1
        else:
            self.club_wins[home_team] = 0
            self.club_wins[away_team] = 0
            self.club_losses[home_team] = 0
            self.club_losses[away_team] = 0

    def display_top_scorers(self):
        print("\nTop 10 Goal Scorers:")
        sorted_scorers = sorted(self.goal_scorers.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (player, goals) in enumerate(sorted_scorers, 1):
            print(f"{i}. {player}: {goals} goals")

    def display_club_stats(self):
        print("\nTop 10 Clubs by Winning Streak:")
        sorted_wins = sorted(self.club_wins.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (club, wins) in enumerate(sorted_wins, 1):
            print(f"{i}. {club}: {wins} wins in a row")

        print("\nTop 10 Clubs by Losing Streak:")
        sorted_losses = sorted(self.club_losses.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (club, losses) in enumerate(sorted_losses, 1):
            print(f"{i}. {club}: {losses} losses in a row")

stats = Stats()
