from kabbes_matchup_scheduler.scheduler import Scheduler
scheduler = Scheduler(overwrite_config={
    'n_teams': 10,
    'n_rounds': 6,
    'teams_per_matchup': 2,
    'matchups_per_round': None,
    'shuffle': False
})

scheduler.run()
