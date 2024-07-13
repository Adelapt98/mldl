import gym
import os
import numpy as np
from stable_baselines3 import PPO, SAC
import argparse

# Import your custom environment if necessary
from env.custom_hopper import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default=None, type=str, help='Model path')
    parser.add_argument('--device', default='cpu', type=str, help='network device [cpu, cuda]')
    parser.add_argument('--render', default=False, action='store_true', help='Render the simulator')
    parser.add_argument('--episodes', default=10, type=int, help='Number of test episodes')
    parser.add_argument('--algorithm', default='PPO', type=str, choices=['PPO','SAC'], help='Algorithm to use for training [reinforce, reinforce_baseline, actor_critic]')

    return parser.parse_args()

args = parse_args()

def test_saved_model(algo, env_id, model_path, num_episodes=10):
    env = gym.make(env_id)
    
    # Load the trained model
    if algo == 'PPO':
        model = PPO.load(model_path)
    elif algo == 'SAC':
        model = SAC.load(model_path)
    else:
        raise ValueError("Algorithm not supported")
    
    # Test the model
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            env.render()
        print(f"Episode {episode + 1}: Reward = {episode_reward}")

if __name__ == "__main__":
    # Example usage
    ALGO = args.algorithm  # Change to 'SAC' if you want to test SAC
    ENV_ID = 'CustomHopper-target-v0'  # Change to your specific environment
    MODEL_PATH = args.model #'./models/PPO_final_model.zip'  # Change to the path of your saved model
    NUM_EPISODES = 100  # Number of episodes to test the agent

    test_saved_model(ALGO, ENV_ID, MODEL_PATH, NUM_EPISODES)