import pdb

import sapien.core as sapien
from mani_skill2 import ASSET_DIR
from mani_skill2.envs.pick_and_place.pick_cube import PickCubeEnv
from mani_skill2.sensors.camera import CameraConfig
from mani_skill2.utils.registration import register_env
from mani_skill2.utils.sapien_utils import look_at
import gymnasium as gym
import numpy as np
import time
import os
# from .visu_utils import *
from sapien.core import Pose
from transforms3d.euler import euler2quat

@register_env("PickCube-v1", max_episode_steps=200, override=True)
class PickCubeDemo(PickCubeEnv):
    # ================ from source =======================
    def _initialize_task(self, max_trials=100, verbose=False):
        obj_pos = self.obj.pose.p

        # Sample a goal position far enough from the object
        for i in range(max_trials):
            goal_xy = self._episode_rng.uniform(-0.1, 0.1, [2])
            goal_z = self._episode_rng.uniform(0, 0.5) + obj_pos[2]
            goal_pos = np.hstack([goal_xy, goal_z])
            if np.linalg.norm(goal_pos - obj_pos) > self.min_goal_dist:
                if verbose:
                    print(f"Found a valid goal at {i}-th trial")
                break

        self.goal_pos = goal_pos
        self.goal_site.set_pose(Pose(self.goal_pos))
    # =============================================================
    def _load_actors(self):
        # Load objects
        self.obj = self._build_cube(half_size=self.cube_half_size,
                                    color=(np.random.uniform(0.1, 0.99),
                                           np.random.uniform(0.1, 0.99),
                                           np.random.uniform(0.1, 0.99)))
        self.goal_site = self._build_sphere_site(radius=0.01)
        # -------------------------------------------------------------------------- #
        # Load static scene
        # -------------------------------------------------------------------------- #
        builder = self._scene.create_actor_builder()
        path = f"{ASSET_DIR}/hab2_bench_assets/stages/Baked_sc1_staging_00.glb"
        pose = sapien.Pose(q=[0.707, 0.707, 0, 0])  # y-axis up for Habitat scenes
        # NOTE: use nonconvex collision for static scene
        builder.add_nonconvex_collision_from_file(path, pose)
        builder.add_visual_from_file(path, pose)
        self.arena = builder.build_static()
        # Add offset so that the workspace is on the table
        offset = np.array([-2.0616, -3.1837, 0.66467 + 0.095])
        self.arena.set_pose(sapien.Pose(-offset))

    def _initialize_actors(self):
        # xy = self._episode_rng.uniform(-0.1, 0.1, [2])
        xy = [0, 0]

        xyz = np.hstack([xy, self.cube_half_size[2]])
        # xyz = np.hstack([xy, 0.2])
        q = [1, 0, 0, 0]
        self.obj.set_pose(Pose(xyz, q))


    def initialize_episode(self):
        super().initialize_episode()

        # Rotate the robot for better visualization
        self.agent.robot.set_pose(
            sapien.Pose([0, -0.56, 0], [0.707, 0, 0, 0.707])
        )

    def _register_render_cameras(self):
        cam_cfg = super()._register_render_cameras()
        cam_cfg.p = cam_cfg.p + [0.5, 0.5, -0.095]
        cam_cfg.fov = 1.5
        return cam_cfg

    def _register_cameras(self):
        pose = look_at([0.0, 0.5, 0.8], [0.0, 0, 0.1])
        camera_1 = CameraConfig(
            "head_camera", pose.p, pose.q, 1280, 720, np.pi / 2, 0.01, 10)

        pose = look_at([0.3, 0.5, 0.8], [0.0, 0, 0.1])
        camera_2 = CameraConfig(
            "right_camera", pose.p, pose.q, 1280, 720, np.pi / 2, 0.01, 10)
        return [camera_1, camera_2]
        # render camera

    def get_object_geom_pose(self, view=False):
        object_pose = self.obj.pose
        if view:
            self.view_position(point=object_pose.p, color=[1, 1, 0], radius=0.01, name='point_position_center')
        return object_pose

    def view_position(self, point: np.ndarray, color=[1, 0, 0], radius=0.03, name='point_visual'):
        builder = self._scene.create_actor_builder()
        builder.add_sphere_visual(radius=radius, color=color)
        sphere = builder.build_static(name)
        sphere.set_pose(Pose(point))
        
    # def save_obs_bbox_and_mask(self, obs, save_path=None):
    #     import json
    #     self.get_object_actors()
    #     camera_datas = dict()
    #     cameras = obs["image"].keys()
    #     camera_params = obs["camera_param"]
    #     for camera in cameras:
    #         # cam2_wolrd = self._get_camera_extrinsic(obs=camera_params, camera_id=camera)
    #         rgb, mask = self.get_object_mask(obs=obs, camera_id=camera)
    #         camera_datas[camera] = {"mask": mask, "rgb": rgb}
    #     if save_path is not None:
    #         for camera_data in camera_datas:
    #             camera_file_path = save_path + "/" + str(camera_data)
    #             os.makedirs(camera_file_path, exist_ok=True)
    #             obs_path = camera_file_path + "/obs.png"
    #             image = Image.fromarray(camera_datas[camera_data]["rgb"])
    #             image.save(obs_path)
    #             mask_path = camera_file_path + "/mask.png"
    #             image = Image.fromarray(camera_datas[camera_data]["mask"])
    #             image.save(mask_path)
    #         object_json = dict()
    #         for object_name, object_mask_id in zip(self.object_actor_names, self.object_actor_ids):
    #             object_json[object_name] = object_mask_id
    #         object_mask_path = save_path + "/object_mask.json"
    #         tf = open(object_mask_path, "w")
    #         json.dump(object_json, tf)
    #         print("finish save grasp pose: ", object_mask_path)


    def get_object_mask(self, obs, camera_id="head_camera", view=False):
        Segmentation = obs["image"][camera_id]["Segmentation"][:, :, 1].astype(np.uint8)
        mask = np.zeros_like(Segmentation)
        mask[Segmentation == self.obj.get_id()] = 1
        rgb = obs["image"][camera_id]["rgb"]
        if view:
            import matplotlib.pyplot as plt
            plt.subplot(1, 2, 1)
            plt.imshow(rgb)
            plt.subplot(1, 2, 2)
            plt.imshow(mask)
            plt.show()
        return rgb, mask


    def _setup_lighting(self):
        self._scene.set_ambient_light([0.3, 0.3, 0.3])
        self._scene.add_point_light([0, 0, 1.0], [1, 1, 1], shadow=False)
        self._scene.add_point_light([1, 1, 1], [1, 1, 1], shadow=False)
        self._scene.add_point_light([-1, -1, 1], [1, 1, 1], shadow=False)
        self._scene.add_point_light([1, -1, 1], [1, 1, 1], shadow=False)
        self._scene.add_point_light([-1, 1, 1], [1, 1, 1], shadow=False)

    def reset(self, seed=None, options=None):
        if options is None:
            options = dict()
        options["reconfigure"] = True
        super().reset(seed=seed, options=options)
        # print("reset env: ", self.episode_idx, episode_idx, reconfigure)
        return self.get_obs(), {}

#
# env = gym.make("PickCube-v1", obs_mode="rgbd", render_mode="human", camera_cfgs=dict(texture_names=("Color", "Position", "Segmentation")))
# print("Observation space", env.observation_space)
# print("Action space", env.action_space)
# obs, reset_info = env.reset(seed=0) # reset with a seed for randomness
# terminated, truncated = False, False
# while not terminated and not truncated:
#     action = env.action_space.sample()
#     rgb, mask = env.get_object_mask(obs)
#     object_pose = env.get_object_geom_pose()
#     obs, reward, terminated, truncated, info = env.step(action)
#     object_pose = env.obj.pose.p
#     pdb.set_trace()
#     print("env.obj.pose.p: ",  env.obj.pose.p)
#     env.render()  # a display is required to render
#     # plot_img(env.unwrapped.render_cameras)
# env.close()
