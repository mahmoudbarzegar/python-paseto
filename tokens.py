import binascii

import paseto
from paseto.exceptions import PasetoException
from paseto.keys.symmetric_key import SymmetricKey
from paseto.protocols.v4 import ProtocolVersion4

from settings import SECRET_KEY_HEX, USERS_DB


def load_key() -> SymmetricKey:
    """Load a key from its hex string representation."""
    return SymmetricKey(binascii.unhexlify(SECRET_KEY_HEX), protocol=ProtocolVersion4)  # type: ignore


def create_access_token(user_id: int, username: str, email: str) -> str:
    """Creates a short-lived access token (5 minutes).

    Contains user identity claims.
    """
    token = paseto.create(
        key=load_key(),
        purpose="local",  # encrypted — nobody can read without the key
        claims={
            "user_id": user_id,
            "username": username,
            "email": email,
            "token_type": "access",
        },
        exp_seconds=300,  # 5 minutes
    )
    return token


def create_refresh_token(user_id: int) -> str:
    """Creates a long-lived refresh token (7 days).

    Contains minimal claims — only used to get a new access token.
    """
    token = paseto.create(
        key=load_key(),
        purpose="local",
        claims={
            "user_id": user_id,
            "token_type": "refresh",
        },
        exp_seconds=7 * 24 * 3600,  # 7 days
    )
    return token


def create_token_pair(user_id: int, username: str, email: str) -> dict:
    """Creates both access and refresh tokens at once. Call this on login."""
    return {
        "access": create_access_token(user_id, username, email),
        "refresh": create_refresh_token(user_id),
    }


def parse_token(raw_token: str, expected_type: str = "access") -> dict:
    """Parses and validates a PASETO token.

    Returns the claims dict if valid.
    Raises ValueError if:
        - token is malformed or tampered
        - token has expired
        - token_type doesn't match expected_type
    """
    try:
        result = paseto.parse(
            key=load_key(),
            purpose="local",
            token=raw_token,
        )
    except PasetoException as e:
        raise ValueError(f"Invalid or expired token: {e}") from e

    claims = result["message"]

    if claims.get("token_type") != expected_type:
        raise ValueError(f"Wrong token type. Expected '{expected_type}', got '{claims.get('token_type')}'")

    return claims


def refresh_access_token(refresh_token: str) -> str:
    """Simulates a refresh endpoint.

    Returns a new access token if the refresh token is valid.
    """
    claims = parse_token(refresh_token, expected_type="refresh")

    # Find user from DB using user_id in claims
    user_id = claims["user_id"]
    user = next((u for u in USERS_DB.values() if u["id"] == user_id), None)

    if not user:
        raise ValueError("User not found.")

    username = next(k for k, v in USERS_DB.items() if v["id"] == user_id)

    new_access_token = create_access_token(
        user_id=user_id,
        username=username,
        email=user["email"],
    )

    print("✅ New access token issued!")
    print(f"   {new_access_token[:60]}...")
    return new_access_token
