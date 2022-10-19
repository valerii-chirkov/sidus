from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas import RequestUser, Response, TokenResponse, UserSchema, LoginUser
import crud
from security import JWTConfig, JWTBearer


router = APIRouter()

# password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Todo разделить на модули login/user (crud, routes, schemas, models ...)
# Todo Бизнес логику вынести в services или в классы, и наследоваться от BaseSmth


@router.post('/login')
async def login(request: LoginUser, db: Session = Depends(get_db, use_cache=False)):
    try:
        _user = crud.get_user_by_email(db=db, email=request.email)
        if not pwd_context.verify(request.password, _user.hashed_password):
            return Response(code=400, status="Bad Request", message="Invalid password")\
                .dict(exclude_none=True)

        token = JWTConfig.generate_token({"sub": _user.email})
        return Response(code=200, status="Ok", message="Logged in",
                        result=TokenResponse(access_token=token, token_type="Bearer"))\
            .dict(exclude_none=True)
    except Exception as e:
        error_message = str(e.args)
        print(error_message)
        return Response(code=500, status="Internal Server Error", message="Internal Server Error")\
            .dict(exclude_none=True)

# def create_user(db: Session, *, obj_in: UserSchema) -> User:
#     db_obj = User(
#         email=obj_in.email,
#         hashed_password=get_password_hash(obj_in.password),
#         full_name=obj_in.full_name,
#         is_superuser=obj_in.is_superuser,
#     )
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
#     return db_obj


@router.post('/create')
async def signup(request: RequestUser, db: Session = Depends(get_db, use_cache=False)):
    try:
        _user = UserSchema(full_name=request.parameter.full_name,
                           email=request.parameter.email,
                           hashed_password=pwd_context.hash(request.parameter.hashed_password),
                           is_active=request.parameter.is_active,
                           is_superuser=request.parameter.is_superuser)
        crud.create_user(db, _user)
        return Response(code=200, status='ok', message='User saved').dict(exclude_none=True)
    except Exception as e:
        print(e.args)
        return Response(code=500, status='Error', message='Internal Server Error')\
            .dict(exclude_none=True)

# @router.post('/create')
# async def create(request: RequestUser, db: Session = Depends(get_db)):
#     crud.create_user(db=db, user=request.parameter)
#     return Response(code=200, status="Ok", message="Created a user").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db, use_cache=True)):
    _user = crud.get_user(db=db, skip=0, limit=100)
    return Response(code=200, status="Ok", message="Fetched all users", result=_user)\
        .dict(exclude_none=True)


@router.get('/{user_id}')
async def get_by_id(user_id: int, db: Session = Depends(get_db, use_cache=True)):
    _user = crud.get_user_by_id(db=db, user_id=user_id)
    return Response(code=200, status="Ok", message="Fetched a user", result=_user) \
        .dict(exclude_none=True)


# @router.get('/{email}')
# async def get_by_email(email: str, db: Session = Depends(get_db, use_cache=True)):
#     _user = crud.get_user_by_email(db=db, email=email)
#     return Response(code=200, status="Ok", message="Fetched a user", result=_user) \
#         .dict(exclude_none=True)


@router.put('/update')
async def update_user(request: RequestUser, db: Session = Depends(get_db, use_cache=False),
                      dependencies=Depends(JWTBearer())):
    _user = crud.update_user(db=db,
                             user_id=request.parameter.id,
                             full_name=request.parameter.full_name,
                             email=request.parameter.email,
                             hashed_password=request.parameter.hashed_password,
                             is_active=request.parameter.is_active,
                             is_superuser=request.parameter.is_superuser, )
    return Response(code=200, status="Ok", message="Updated a user", result=_user)


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db, use_cache=False),
                      dependencies=Depends(JWTBearer())):
    crud.delete_user(db=db, user_id=user_id)
    return Response(code=200, status="Ok", message="Deleted a user").dict(exclude_none=True)

