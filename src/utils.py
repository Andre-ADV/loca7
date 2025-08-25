from fastapi import HTTPException

def check_if_exists(obj, error_msg: str) -> None:
    if obj is None:
        raise HTTPException(
            status_code = 404,
            detail=error_msg
        )

