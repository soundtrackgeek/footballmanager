class TeamStats:
    def __init__(self, team_name):
        self.team_name = team_name
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

class Table:
    def __init__(self, teams):
        self.stats = {team.name: TeamStats(team.name) for team in teams}

    def update(self, home_team, away_team, home_goals, away_goals):
        home_stats = self.stats[home_team]
        away_stats = self.stats[away_team]

        home_stats.played += 1
        away_stats.played += 1
        home_stats.goals_for += home_goals
        home_stats.goals_against += away_goals
        away_stats.goals_for += away_goals
        away_stats.goals_against += home_goals

        if home_goals > away_goals:
            home_stats.won += 1
            home_stats.points += 3
            away_stats.lost += 1
        elif home_goals < away_goals:
            away_stats.won += 1
            away_stats.points += 3
            home_stats.lost += 1
        else:
            home_stats.drawn += 1
            away_stats.drawn += 1
            home_stats.points += 1
            away_stats.points += 1

    def display(self):
        sorted_stats = sorted(
            self.stats.values(),
            key=lambda x: (x.points, x.goal_difference, x.goals_for),
            reverse=True
        )

        print("\nCurrent Table:")
        print(f"{'Team':<20} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>3} {'GA':>3} {'GD':>3} {'Pts':>3}")
        print("-" * 50)
        for stat in sorted_stats:
            print(f"{stat.team_name:<20} {stat.played:3d} {stat.won:3d} {stat.drawn:3d} {stat.lost:3d} "
                  f"{stat.goals_for:3d} {stat.goals_against:3d} {stat.goal_difference:3d} {stat.points:3d}")

def create_table(teams):
    return Table(teams)
