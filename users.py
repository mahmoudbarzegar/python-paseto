# Fake user database
from settings import USERS_DB
from tokens import create_token_pair, parse_token


def login(username: str, password: str) -> dict:
    """Simulates a login endpoint.

    Returns token pair if credentials are correct.
    """
    user = USERS_DB.get(username)

    if not user or user["password"] != password:
        raise PermissionError("Invalid username or password.")

    tokens = create_token_pair(
        user_id=user["id"],
        username=username,
        email=user["email"],
    )

    print(f"✅ Login successful! Welcome, {username}!")
    print(f"   Access token  : {tokens['access'][:60]}...")
    print(f"   Refresh token : {tokens['refresh'][:60]}...")
    return tokens


def access_protected_resource(access_token: str) -> dict:
    """Simulates a protected endpoint.

    Returns user info if the access token is valid.
    """
    claims = parse_token(access_token, expected_type="access")

    print("✅ Access granted!")
    print(f"   user_id  : {claims['user_id']}")
    print(f"   username : {claims['username']}")
    print(f"   email    : {claims['email']}")
    print(f"   expires  : {claims['exp']}")
    return claims
