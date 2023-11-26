import gymnasium as gym
import numpy as np
from PIL import Image
import os

class DemoPlanner:
    
    def __init__(self):
        # build env
        env = gym.make("PickCube_Plan-v0",
                obs_mode="rgbd",
                # shader_dir= "rt",
                control_mode="pd_ee_delta_pose",
                render_mode="human",
                camera_cfgs=dict(texture_names=("Color", "Position", "Segmentation")))
        self.env = env
        
        
    def reset(self, bias=None):
        self.bias = bias
        
        self.exp_results = {'task': 'grasp the cube Franka Panda robot hand.'}
        
        obs, reset_info = self.env.reset()
        self.env.setup_planner()
        self.env.render()
        self.env.disable_use_point_cloud()
        
        obs = self._get_base_obs()
        goal = self.plan_goal(obs)
        
        self.exp_results.update({
            'states_init': obs,
            'images_init': self.get_images('init'),
        })
        
        return obs, goal
        
    def plan_goal(self, obs):
        goal = np.hstack((obs['object'][:3], obs['robot'][3:]))
        return goal
        
    def step(self, goal, delta_goal, final_goal):
        
        # 1. move to above
        self.env.open_gripper()
        final_goal1 = final_goal.copy()
        final_goal1[2] = final_goal1[2] + 0.2
        res = self.env.move_to_pose(final_goal1)
        
        # 2. move to final
        final_goal2 = final_goal.copy()
        res = self.env.move_to_pose(final_goal2)
        self.env.close_gripper()
        
        res = self.env.check_grasp()
        
        self.exp_results.update({
            'states_final': self._get_base_obs(),
            'images_final': self.get_images('final'),
            'goal': goal,
            'delta_goal': delta_goal,
            'final_goal': final_goal,
        })
        
        return res
    
    def get_exp_results(self):
        return self.exp_results

    def _get_base_obs(self):
        object_pose_to_base, robot_ee_pose = self.env.get_object_ee_pose()
        obs = {'robot': np.hstack((robot_ee_pose.p, robot_ee_pose.q)), 'object': np.hstack((object_pose_to_base.p, object_pose_to_base.q))}
        if self.bias is not None:
            obs['object'] += self.bias
        return obs
    
    def get_images(self, name):
        obs = self.env.get_obs()
        obs = self.env.observation(obs)
        cameras = obs["image"].keys()
        
        images = []
        for camera in cameras:
            rgb, mask = self.env.get_object_mask(obs, camera_id=camera)
            rgb = obs["image"][camera]["rgb"]
            image = Image.fromarray(rgb)
            
            # generate dir, and save
            base_dir = './temp/images/'
            final_dir = os.path.join(base_dir, name + '_' + camera + ".png")
            image.save(final_dir)
            images.append(final_dir)
            
        return images
            