
import gymnasium as gym
import matplotlib.pyplot as plt
import time
import pdb
import json
import numpy as np
from PIL import Image
from src.robot.envs import *

def plot_img(img, title=None):
    plt.figure(figsize=(10,6))
    if title is not None:
        plt.title(title)
    plt.imshow(img)
    plt.show()
    
    
def make_env():

    env = gym.make("PickCube_Plan-v0",
                obs_mode="rgbd",
                # shader_dir= "rt",
                control_mode="pd_ee_delta_pose",
                render_mode="human",
                camera_cfgs=dict(texture_names=("Color", "Position", "Segmentation")))
    # print("Observation space", env.observation_space)
    # print("Action space", env.action_space)
    return env

def save_images(env, name):
    obs = env.get_obs()
    obs = env.observation(obs)
    cameras = obs["image"].keys()
    for camera in cameras:
        rgb, mask = env.get_object_mask(obs, camera_id=camera)
        rgb = obs["image"][camera]["rgb"]

        image = Image.fromarray(rgb)
        image.save(name + '_' + camera + ".png")

def run(env):

    obs, reset_info = env.reset(seed=np.random.randint(0, 100000, 1))
    env.setup_planner()
    env.render()
    env.disable_use_point_cloud()
    
    object_pose_to_base, robot_ee_pose = env.get_object_ee_pose()
    pos = object_pose_to_base.p
    quat = robot_ee_pose.q
    pickup_pose = np.hstack((pos, quat))
    
    # print('states_init', object_pose_to_base, robot_ee_pose)
    # print('goal', pickup_pose)
    # print('delta_goal', [])
    # save_images(env, 'init')
    print('pickup_pose', pickup_pose)
    
    # formal movement
    pickup_pose[2] = pickup_pose[2] + 0.2
    res = env.move_to_pose(pickup_pose)
    
    env.open_gripper()
    pickup_pose[2] = pickup_pose[2] - 0.20
    res = env.move_to_pose(pickup_pose)
    env.close_gripper()
    
    res = env.check_grasp()
    print('success', res)
    
    # object_pose_to_base, robot_ee_pose = env.get_object_ee_pose()
    # print('states_final', object_pose_to_base, robot_ee_pose)
    # save_images(env, 'final')
    
    
    # final state
    # rgb, mask = env.get_object_mask(obs)


if __name__ == "__main__":
    env = make_env()
    run(env)