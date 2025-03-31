import hashlib


def sha256_hex(value: str) -> str:
    """
    Create a SHA-256 hash and encode it as lowercase hex string.
    This mimics the @oslojs/crypto and encoding libraries used in the frontend.

    Args:
        value: The string to hash

    Returns:
        Lowercase hexadecimal representation of the hash
    """
    # Create a SHA-256 hash of the value
    hash_bytes = hashlib.sha256(value.encode()).digest()

    # Convert to lowercase hex to match encodeHexLowerCase from @oslojs/encoding
    return hash_bytes.hex().lower()
