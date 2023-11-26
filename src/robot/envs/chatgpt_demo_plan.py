import copy
import pdb
import time
import sapien.core as sapien
from mani_skill2.envs.pick_and_place.pick_clutter import PickClutterEnv
from mani_skill2.envs.pick_and_place.pick_single import PickSingleYCBEnv, build_actor_ycb
from mani_skill2 import ASSET_DIR
from mani_skill2.utils.registration import register_env
from typing import Dict, List
import numpy as np
import random
from sapien.core import Pose
from scipy.spatial.transform import Rotation
from mani_skill2.utils.sapien_utils import (
    get_entity_by_name,
    look_at,
    set_articulation_render_material,
    vectorize_pose,
)
from mani_skill2.sensors.camera import CameraConfig
import json
# from .visu_utils import view_point_cloud_parts, pc_camera_to_world
from collections import Counter
from .chat_gpt_demo import PickCubeDemo
import mplib
from PIL import Image

@register_env("PickCube_Plan-v0", max_episode_steps=200)
class Pick_Cube_plan(PickCubeDemo):

    def setup_planner(self):
        link_names = [link.get_name() for link in self.agent.robot.get_links()]
        joint_names = [joint.get_name() for joint in self.agent.robot.get_active_joints()]
        self.planner = mplib.Planner(
            urdf="./data/descriptions/panda_v2.urdf",
            srdf="./data/descriptions/panda_v2.srdf",
            user_link_names=link_names,
            user_joint_names=joint_names,
            move_group="panda_hand_tcp",
            joint_vel_limits=np.ones(7),
            joint_acc_limits=np.ones(7))
        self.active_joints = self.agent.robot.get_active_joints()
        for joint in self.active_joints:
            joint.set_drive_property(stiffness=1000, damping=200)

    def follow_path(self, result):
        n_step = result['position'].shape[0]
        for i in range(n_step):
            qf = self.agent.robot.compute_passive_force(
                gravity=True,
                coriolis_and_centrifugal=True)
            self.agent.robot.set_qf(qf)
            for j in range(7):
                self.active_joints[j].set_drive_target(result['position'][i][j])
                self.active_joints[j].set_drive_velocity_target(result['velocity'][i][j])
            self._scene.step()
            if i % 4 == 0:
                self._scene.update_render()
                self.render()

    def open_gripper(self):
        for joint in self.active_joints[-2:]:
            joint.set_drive_target(1)
        for i in range(1000):
            qf = self.agent.robot.compute_passive_force(
                gravity=True,
                coriolis_and_centrifugal=True)
            self.agent.robot.set_qf(qf)
            self._scene.step()
            if i % 4 == 0:
                self._scene.update_render()
                self.render()
                if abs(self.agent.robot.get_qpos()[-1] - 0.04) < 0.002:
                    break
    def close_gripper(self):
        for joint in self.active_joints[-2:]:
            joint.set_drive_target(-1)
        for i in range(1000):
            qf = self.agent.robot.compute_passive_force(
                gravity=True,
                coriolis_and_centrifugal=True)
            self.agent.robot.set_qf(qf)
            self._scene.step()
            if i % 4 == 0:
                self._scene.update_render()
                self.render()

    def check_grasp(self):
        gripper_state = self.agent.robot.get_qpos()[-2:]
        if gripper_state[0] < 0.005 or gripper_state[1] < 0.005:
            return -1
        else:
            return 1

    def move_to_pose(self, pose):
        result = self.planner.plan_screw(pose, self.agent.robot.get_qpos(), time_step=1 / 250,
                                         use_point_cloud=self.use_point_cloud, use_attach=self.use_attach)
        if result['status'] != "Success":
            result = self.planner.plan(pose, self.agent.robot.get_qpos(), time_step=1 / 250,
                                       use_point_cloud=self.use_point_cloud, use_attach=self.use_attach)
            if result['status'] != "Success":
                print(result['status'])
                return -1
            
        self.follow_path(result)
        return 0

    def add_point_cloud(self, obs):
        scene_object_pcd, _ = self.get_scene_point_cloud(obs)
        self.planner.update_point_cloud(scene_object_pcd)
        return
    
    def get_object_ee_pose(self):
        obj = self.obj
        robot_base_pose = self.agent.robot.pose
        robot_base_pose_inv = robot_base_pose.inv()
        object_pose_to_base = robot_base_pose_inv.transform(obj.pose)
        robot_ee_pose = robot_base_pose_inv.transform(self.tcp.pose)
        return object_pose_to_base, robot_ee_pose

    def disable_use_point_cloud(self):
        self.use_point_cloud = False
        self.use_attach = False

    def plan_pick_and_place(self, obs=None, view_target=False, use_point_cloud=False, noise=False, bias=False):
        self.render()
        # robot_base_pose = self.agent.robot.pose
        # robot_base_pose_inv = robot_base_pose.inv()
        # if view_target:
        #     self.view_position(point=self.get_object_geom_pose().p, radius=0.03, color=[0, 1, 0])
        # object_pose_to_base = robot_base_pose_inv.transform(self.get_object_geom_pose())
        # robot_ee_pose = robot_base_pose_inv.transform(self.tcp.pose)

        object_pose_to_base, robot_ee_pose = self.get_object_ee_pose()
        # print("object_pose_to_base", object_pose_to_base)
        # print("robot_ee_pose", robot_ee_pose)


        pos = object_pose_to_base.p
        if noise:
            pos[:2] = pos[:2] + np.random.uniform(-0.05, 0.05, 2)
            pos[2] = pos[2] + np.random.uniform(-0.025, 0.025, 1)

        if bias:
            pos[0] = pos[0] + np.random.uniform(-0.05, 0.05, 1)
            pos[1] = pos[1] + np.random.uniform(-0.05, 0.05, 1)
            pos[2] = pos[2] + np.random.uniform(-0.05, 0.05, 1)

        quat = robot_ee_pose.q
        pickup_pose = np.hstack((pos, quat))
        self.use_point_cloud = use_point_cloud
        if self.use_point_cloud:
            self.add_point_cloud(obs)
        self.use_attach = False
        
        '''
        agent odict_keys(['qpos', 'qvel', 'base_pose'])
        extra odict_keys(['tcp_pose', 'goal_pos'])
        camera_param odict_keys(['head_camera', 'right_camera', 'hand_camera'])
        image odict_keys(['head_camera', 'right_camera', 'hand_camera'])
        '''
        
        obs0 = self.get_obs()
        # print("obs0", obs0.keys())
        # print("obs0['image']", obs0['image'].keys())
        # print("obs0['image']['head_camera']", obs0['image']['head_camera'].keys())
        
        # obs1 = self.observation(obs0)
        # print("obs1", obs1.keys())
        
        
        # self.output("init")
        # 1. move to pickup pose
        
        pickup_pose[2] = pickup_pose[2] + 0.2
        # self.view_position(point=pickup_pose[:3]+self.agent.robot.pose.p, radius=0.01, color=[1, 1, 0])
        res = self.move_to_pose(pickup_pose)
        if res == -1:
            return
        
        self.open_gripper()
        pickup_pose[2] = pickup_pose[2] - 0.20
        # self.view_position(point=pickup_pose[:3]+self.agent.robot.pose.p, radius=0.01, color=[0, 1, 0])
        res = self.move_to_pose(pickup_pose)
        if res == -1:
            return
        
        self.close_gripper()
        res = self.check_grasp()

        # 2. final pose
        

        # if res == -1:
        #     return
        # goal_pose = robot_base_pose_inv.transform(self.goal_site.pose)
        # goal_pose = np.hstack((goal_pose.p, pickup_pose[3:]))
        # self.move_to_pose(goal_pose)
        # if res == -1:
        #     return







