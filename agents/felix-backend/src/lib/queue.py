"""Redis / RQ queue helpers for async evaluation dispatch (ADR-005)."""
import redis
from rq import Queue

from src.config import settings

_redis_conn: redis.Redis | None = None
_eval_queue: Queue | None = None


def get_redis() -> redis.Redis:
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = redis.from_url(settings.redis_url)
    return _redis_conn


def get_eval_queue() -> Queue:
    global _eval_queue
    if _eval_queue is None:
        _eval_queue = Queue("evaluation", connection=get_redis())
    return _eval_queue


def enqueue_evaluation(submission_id: str, priority: str = "interactive") -> str:
    """Enqueue an evaluation task; returns the RQ job id."""
    from src.evaluator.tasks import run_evaluation

    queue_name = "evaluation_batch" if priority == "batch" else "evaluation"
    q = Queue(queue_name, connection=get_redis())
    job = q.enqueue(run_evaluation, submission_id, job_timeout=120)
    return job.id
