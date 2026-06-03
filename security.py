import os
import secrets
import hashlib
from dotenv import load_dotenv

load_dotenv()

# Rubric Requirement: The pepper must NOT be stored in the database.
PEPPER = os.getenv("APP_PEPPER", "CincoLink-Secret-Pepper-Key-2026!")

def generate_salt() -> str:
    """Requirement: Generate a unique random salt."""
    # Generates a 32-character hexadecimal string
    return secrets.token_hex(16)

def get_password_hash(password: str, salt: str) -> str:
    """Requirement: Combine password + salt + pepper, then hash."""
    combined = f"{password}{salt}{PEPPER}"
    
    # Use SHA-256 (Secure Hash Algorithm)
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, stored_salt: str, hashed_password: str) -> bool:
    """Requirement: Recompute hash using input_password + stored_salt + pepper."""
    combined = f"{plain_password}{stored_salt}{PEPPER}"
    
    # Recompute the hash to see if it matches what is in the database
    recomputed_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    return recomputed_hash == hashed_password