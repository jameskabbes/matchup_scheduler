from kabbes_matchup_scheduler.scheduler import Scheduler
scheduler = Scheduler(**{
    'n_teams': 8,
    'n_rounds': 7,
    'teams_per_matchup': 2,
    'matchups_per_round': None,
})

scheduler.run()
