import kabbes_matchup_scheduler

c = kabbes_matchup_scheduler.Client(
    n_teams = 16,
    n_rounds = 2
)

c.run()