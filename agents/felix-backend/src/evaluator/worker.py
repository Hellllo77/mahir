"""Evaluator worker entry point (ADR-005 — separate worker tier).

Usage:
    python -m src.evaluator.worker

Or via rq CLI:
    rq worker mahir-evaluations --with-scheduler
"""
import logging

import redis
from rq import Worker

from src.config import settings
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

QUEUES = ["evaluation", "evaluation_batch"]


def main() -> None:
    conn = redis.from_url(settings.redis_url)
    worker = Worker(queues=QUEUES, connection=conn)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
