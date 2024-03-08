from typing import TypedDict

type IDType = int
type TeamID = IDType

type LocaleIndex = int

type MatchupType = list[IDType]
type RoundType = list[MatchupType]
type ScheduleType = list[RoundType]


ConstraintConfig = TypedDict('ConstraintConfig', {
    'min': int,
    'max': int
})

OpponentCountConfig = TypedDict('OpponentCountConfig', {
    'count': ConstraintConfig,
    'locale': ConstraintConfig
})


class ConstraintsConfig(TypedDict):
    n_matchups: ConstraintConfig
    opponent_count: OpponentCountConfig
    locale_count: ConstraintConfig
