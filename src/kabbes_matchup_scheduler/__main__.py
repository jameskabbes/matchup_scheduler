from kabbes_matchup_scheduler.scheduler import Scheduler
scheduler = Scheduler(overwrite_config={
    'n_teams': 8,
    'n_rounds': 4,
    'teams_per_matchup': 2,
    'matchups_per_round': 1,
    'shuffle': False
})

scheduler.run()
