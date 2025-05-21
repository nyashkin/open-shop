from typing import Literal, Optional

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from .base import BaseAppSettings
from pydantic import PositiveInt, model_validator, ValidationError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature, InvalidKey


class JwtSettings(BaseAppSettings):
    public_key: str
    private_key: Optional[str]
    rsa_password: Optional[str]
    algorithm: Literal["HS256", "RS256"] = "RS256"
    access_token_expire_minutes: PositiveInt = 15
    refresh_token_expire_days: PositiveInt = 14

    @model_validator(mode="after")
    def validate_keys(self) -> None:
        try:
            pub_k: RSAPublicKey = serialization.load_pem_public_key(
                data=self.public_key.encode("utf-8"), backend=default_backend()
            )
            if self.algorithm == "RS256":
                if not self.private_key:
                    raise InvalidKey("If RSA256 is enabled private key can not be None")

                pr_k = serialization.load_pem_private_key(
                    data=self.private_key.encode("utf-8"),
                    backend=default_backend(),
                    password=self.rsa_password,
                )

                if pr_k.public_key().public_numbers() != pub_k.public_numbers():
                    raise InvalidKey("Public and private keys not matched")
        except (InvalidKey, InvalidSignature, ValueError) as e:
            raise ValueError(f"Keys validation error: {e}")
