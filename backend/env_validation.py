import os

REQUIRED_ENV_VARS = [
    "DATABASE_URL",
    "JWT_SECRET_KEY",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
]


def validate_env() -> None:
    missing = []

    for var_name in REQUIRED_ENV_VARS:
        value = os.getenv(var_name)
        if value is None or value.strip() == "":
            missing.append(var_name)

    errors = []

    if missing:
        errors.append(
            "Missing required environment variables: " + ", ".join(missing)
        )

    access_token_expire = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if access_token_expire is not None and access_token_expire.strip() != "":
        try:
            expire_minutes = int(access_token_expire)
            if expire_minutes <= 0:
                errors.append(
                    "ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer."
                )
        except ValueError:
            errors.append(
                "ACCESS_TOKEN_EXPIRE_MINUTES must be an integer."
            )

    if errors:
        raise RuntimeError("Environment configuration error. " + " ".join(errors))