"""
    A3C agent class for spawning threads
"""

from threading import Thread

import grid2op

from grid2op.Reward import L2RPNSandBoxScore

import constants


class Worker(Thread):
    """
        The Agent class.

        Spawns multiple copies of the environment each with its own
        worker. All workers share weights to a common global network

        Parameters
        ----------
        index (int): Worker ID
    """

    def __init__(self, index: int, action_dim, state_size, env_name: str = 'l2rpn_wcci_2020', batch_size: int = 256, ** args):
        self.states = []
        self.rewards = []
        self.actions = []

        self.worker_idx = index
        self.actor = args['actor']
        self.critic = args['critic']
        self.optimizers = args['optimizers']

        self.gamma = args['gamma']
        self.action_dim = action_dim
        self.state_size = state_size

        self.env_name = env_name
        self.batch_size = batch_size

    def run(self):
        """
            Start thread
        """

        global episode, episode_test

        episode = 0

        print(f'Staring agent: {self.worker_idx}\n')

        env = grid2op.make(
            self.env_name, reward_class=L2RPNSandBoxScore, difficulty='competition')

        while episode < constants.EPISODE_STEPS:
            env.set_id(episode)
            state = env.reset()

            time_step_end = env.chronics_handler.max_timestep() - 2

            print('time step end: ', time_step_end)