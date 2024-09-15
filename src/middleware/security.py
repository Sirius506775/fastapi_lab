from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_access_token(auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))) -> str:
    """header에서 access token이 있는지 검증하는 함수
    정상적으로 요청이 온 경우, access token을 반환한다.
    잘못된 요청이 온 경우, HTTPException을 발생시킨다.
    """

    if auth_header is None:
        raise HTTPException(status_code=401, detail="Not Authorized")
    return auth_header.credentials
