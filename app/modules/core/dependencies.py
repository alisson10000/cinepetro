from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modules.core.database import get_db
from app.modules.core.security import decode_access_token
from app.modules.user.services import get_by_id
from app.modules.core.logger import logger  # ⬅️ Import do logger

# Define o esquema de autenticação via OAuth2 com token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Recupera o usuário autenticado a partir do token JWT.
    Lança HTTP 401 se o token for inválido ou o usuário não existir.
    """

    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        logger.warning("⚠️ [TOKEN] Token inválido ou sem 'sub'")  # ⬅️ Log de token inválido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(payload["sub"])
    except (ValueError, TypeError):
        logger.warning(f"⚠️ [TOKEN] ID inválido no token | sub={payload.get('sub')}")  # ⬅️ Log de ID malformado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID de usuário inválido no token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_by_id(db, user_id)

    if not user:
        logger.warning(f"⚠️ [TOKEN] Usuário não encontrado | user_id={user_id}")  # ⬅️ Log de usuário inexistente
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"🔓 [TOKEN] Acesso autenticado | user_id={user.id} | email={user.email}")  # ⬅️ Log de sucesso
    return user
