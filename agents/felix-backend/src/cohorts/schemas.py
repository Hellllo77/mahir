from pydantic import BaseModel


class CohortSummary(BaseModel):
    id: str
    name: str
    status: str
    learner_count: int
