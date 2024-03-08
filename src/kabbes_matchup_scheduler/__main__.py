from kabbes_matchup_scheduler.scheduler import Scheduler
scheduler = Scheduler(**{
    'n_teams': 4,
    'n_rounds': 3,
    'teams_per_matchup': 2,
    'matchups_per_round': None,
})

scheduler.run()
