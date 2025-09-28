from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.company_models import Company
from app.models.user_models import User
from app.utils.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SignupIn(BaseModel):
    email: str
    password: str
    company_name: str

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):  # type: ignore[override]
        data = super().model_validate(obj, *args, **kwargs)
        if len(data.password.encode("utf-8")) > 128:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password too long")
        if len(data.password) < 6:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password too short")
        return data


class MeOut(BaseModel):
    id: str
    email: str
    company_id: str
    role: str


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> MeOut:
    from app.utils.security import decode_token

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return MeOut(
        id=str(payload.get("sub")),
        email=payload.get("email", ""),
        company_id=str(payload.get("company_id")),
        role=payload.get("role", "user"),
    )


@router.post("/signup", response_model=TokenOut)
async def signup(data: SignupIn, db: AsyncSession = Depends(get_db)) -> TokenOut:
    # Create company
    company = Company(name=data.company_name)
    db.add(company)
    await db.flush()

    # Create user
    user = User(email=data.email, hashed_password=hash_password(data.password), company_id=company.id)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email, "company_id": str(user.company_id), "role": user.role})
    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)) -> TokenOut:
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token({"sub": str(user.id), "email": user.email, "company_id": str(user.company_id), "role": user.role})
    return TokenOut(access_token=token)


@router.get("/me", response_model=MeOut)
async def me(current: MeOut = Depends(get_current_user)) -> MeOut:
    return current


