"""UUIDv7 — time-sortable UUID per ADR-002 convention."""
import os
import time
import uuid


def uuid7() -> uuid.UUID:
    """Generate a UUIDv7 (time-ordered) value.

    Layout (128 bits):
        [48 bits ms timestamp][4 bits version=7][12 bits rand_a][2 bits variant][62 bits rand_b]
    """
    ms = int(time.time() * 1000) & 0xFFFFFFFFFFFF
    rand = int.from_bytes(os.urandom(10), "big")

    rand_a = (rand >> 62) & 0xFFF
    rand_b = rand & 0x3FFFFFFFFFFFFFFF

    hi = (ms << 16) | (0x7 << 12) | rand_a
    lo = (0b10 << 62) | rand_b

    return uuid.UUID(int=(hi << 64) | lo)


def uuid7_str() -> str:
    return str(uuid7())
