from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, BearerTransport
from fastapi_users.authentication import JWTStrategy
from starlette.requests import Request
from authentication.manager import get_user_manager
from authentication.models import User
from config import SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


async def get_enabled_backends(request: Request):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', request.url.path)
    """Return the enabled dependencies following custom logic."""
    if request.url.path == "/auth/jwt-test":
        print('!!!!!', 'passed jwt')
        return [jwt_backend]
    else:
        return [jwt_backend]


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)
auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
jwt_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)
cookie_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)
current_active_user = fastapi_users.current_user(active=True, get_enabled_backends=get_enabled_backends)
