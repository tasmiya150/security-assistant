import re

COMMON_PASSWORDS = {"123456", "password", "qwerty", "letmein", "admin", "welcome"}

def check_strength(password: str) -> dict:
    if password in COMMON_PASSWORDS:
        return {"strength": "Weak", "score": 0, "reasons": ["Common password"]}

    score = 0
    reasons = []

    if len(password) >= 8:
        score += 3
    else:
        reasons.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 2
    else:
        reasons.append("Add an uppercase letter")

    if re.search(r"[0-9]", password):
        score += 2
    else:
        reasons.append("Add a number")

    if re.search(r"[!@#$%^&*]", password):
        score += 3
    else:
        reasons.append("Add a special character (!@#$%^&*)")

    if score >= 8:
        strength = "Strong"
    elif score >= 5:
        strength = "Medium"
    else:
        strength = "Weak"

    return {"strength": strength, "score": score, "reasons": reasons}


def generate_password(length: int = 12) -> str:
    import secrets, string
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))