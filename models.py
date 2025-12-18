from pydantic import BaseModel


class Profile(BaseModel):
    userSlug: str
    realName: str | None
    userAvatar: str | None = None
    countryCode: str | None
    countryName: str | None


class User(BaseModel):
    username: str
    profile: Profile


class RankingNode(BaseModel):
    currentGlobalRanking: int
    currentRating: float
    dataRegion: str | None
    user: User


class Leaderboard(BaseModel):
    rankingNodes: list[RankingNode]
    totalPages: int


class DataWrapper(BaseModel):
    globalRanking: Leaderboard


class LeaderboardResponse(BaseModel):
    data: DataWrapper
