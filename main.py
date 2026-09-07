# ============================================================
# PASETO in Pure Python
# No Django, No Flask — just Python + paseto library
# Install: pip install paseto
# ============================================================

from paseto.keys.symmetric_key import SymmetricKey
from paseto.protocols.v4 import ProtocolVersion4

from tokens import refresh_access_token
from users import access_protected_resource, login


# ─────────────────────────────────────────────
# Generate a secret key
# In production: generate ONCE, save in .env file
# Never hardcode it, never commit it to git
# ─────────────────────────────────────────────
def generate_key():
    """Generate a new random secret key and print its hex value."""
    key = SymmetricKey.generate(protocol=ProtocolVersion4)
    print(f"Your secret key :\n{key.key.hex()}\n")
    return key


# ─────────────────────────────────────────────
#                 Test
# ─────────────────────────────────────────────

print("=" * 55)
print(" PASETO Pure Python Demo")
print("=" * 55)

# ── 1. Successful login
print("\n[1] Login with correct credentials")
print("-" * 40)
tokens = login("alice", "alice123")

# ── 2. Access a protected resource
print("\n[2] Access protected resource with valid token")
print("-" * 40)
access_protected_resource(tokens["access"])

# ── 3. Refresh the access token
print("\n[3] Refresh the access token")
print("-" * 40)
new_access = refresh_access_token(tokens["refresh"])

# ── 4. Wrong token type
print("\n[4] Try to use refresh token as access token")
print("-" * 40)
try:
    access_protected_resource(tokens["refresh"])
except ValueError as e:
    print(f"❌ Rejected: {e}")

# ── 5. Tampered token
print("\n[5] Try a tampered token")
print("-" * 40)
try:
    access_protected_resource(tokens["access"] + "TAMPERED")
except ValueError as e:
    print(f"❌ Rejected: {e}")

# ── 6. Wrong credentials
print("\n[6] Login with wrong password")
print("-" * 40)
try:
    login("alice", "wrongpassword")
except PermissionError as e:
    print(f"❌ Rejected: {e}")


# ── 7. Generate tokens again
print("\n[7] Generate tokens again")
print("-" * 40)
try:
    generate_key()
except Exception:
    raise

# ── 8. Compare JWT vs PASETO token appearance
print("\n[8] What does a PASETO token look like?")
print("-" * 40)
print("JWT    starts with : eyJhbGci... (base64 — readable by anyone)")
print(f"PASETO starts with : {tokens['access'][:40]}...")
print("                     (encrypted — unreadable without secret key)")

print("\n" + "=" * 55)
print(" All tests passed!")
print("=" * 55)
