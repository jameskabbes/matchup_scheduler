import kabbes_matchup_scheduler

settings = {
    "n_teams": int(input('n_teams: ')),
    "n_rounds": int(input('n_rounds: '))
}

c = kabbes_matchup_scheduler.Client( dict={"default_settings":settings} )
c.run()
