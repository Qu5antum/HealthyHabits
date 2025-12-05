from dataclasses import dataclass
from environs import Env

@dataclass
class Config: 
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    URL_DATABASE: str

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        SECRET_KEY=env.str("SECRET_KEY"),
        ALGORITHM=env.str("ALGORITHM"),
        ACCESS_TOKEN_EXPIRE_MINUTES=env.int("ACCESS_TOKEN_EXPIRE_MINUTES"),
        URL_DATABASE = env.str("URL_DATABASE")
    )

config = load_config()