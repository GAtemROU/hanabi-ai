from envs.env import Env
from envs.registration import register, make

register(env_id= 'hanabi', entry_point= 'envs.hanabi:HanabiEnv')
