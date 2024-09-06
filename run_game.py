import envs.hanabi as hanabi
from agents.random_agent import RandomAgent
import pprint
import utils.parser as parser
from envs.registration import make


args = parser.get_args()
env = make(
        args.env,
        config={
            'seed': args.seed,
        }
    )

agent = RandomAgent(num_actions=env.num_actions)

env.set_agents([agent for _ in range(env.num_players)])


trajectories, score = env.run(is_training=True)

print('\nTrajectories:')
# print(trajectories)
print('\nSample raw observation:')
# pprint.pprint(trajectories[0][0]['raw_obs'])
print('\nSample raw legal_actions:')
# pprint.pprint(trajectories[0][0]['raw_legal_actions'])

