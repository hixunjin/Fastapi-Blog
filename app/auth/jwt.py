from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.settings import SECRET_KEY
from fastapi import Depends
from app.db.session import get_db
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.user.models import User

# 配置
SECRET_KEY = SECRET_KEY  # 密钥设置
ALGORITHM = "HS256"   #加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  #过期时间 1 天

# 用于 OAuth2 密码模式认证的 token 路由
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/auth/token")



# 创建 JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析 JWT token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None




# 获取当前用户（依赖项）
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token 无效")

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token 无效")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user





