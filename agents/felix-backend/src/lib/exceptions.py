from fastapi import HTTPException, status


def not_found(resource: str = "Resource") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"type": "not_found", "message": f"{resource} not found."})


def forbidden(msg: str = "Forbidden.") -> HTTPException:
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"type": "forbidden", "message": msg})


def unauthorized(msg: str = "Invalid or missing credentials.") -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "unauthorized", "message": msg}, headers={"WWW-Authenticate": "Bearer"})


def bad_request(msg: str, detail: dict | None = None) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"type": "validation_error", "message": msg, **({"details": detail} if detail else {})},
    )


def phase_locked() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={"type": "phase_locked", "message": "Complete the exploration phase before consolidation unlocks."},
    )


def conflict(msg: str, type_: str = "conflict") -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"type": type_, "message": msg})
