import envs.hanabi as hanabi
from agents.random_agent import RandomAgent
import pprint

env = hanabi.Env()

agent = RandomAgent(action_num=env.action_num)

env.set_agents([agent for _ in range(env.num_players)])


trajectories, score = env.run(is_training=True)

print('\nTrajectories:')
print(trajectories)
print('\nSample raw observation:')
pprint.pprint(trajectories[0][0]['raw_obs'])
print('\nSample raw legal_actions:')
pprint.pprint(trajectories[0][0]['raw_legal_actions'])

