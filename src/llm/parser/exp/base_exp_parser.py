

class BaseExpParser:
    
    def parse(self, exp_results):
        # inputs:
        # 1. initial state_dict, initial_images
        # 2. terminal state_dict, terminal_images
        # 3. initial goal, delta_goal, final_goal
        
        task = exp_results['task']
        states_init = exp_results['states_init']
        images_init = exp_results['images_init'] # list of image paths
        states_final = exp_results['states_final']
        images_final = exp_results['images_final'] # list of image paths
        goal = exp_results['goal']
        delta_goal = exp_results['delta_goal']
        final_goal = exp_results['final_goal']
        
        len_images_init = len(images_init)
        len_images_final = len(images_final)
        
        
        states_init_str = str(states_init)
        states_final_str = str(states_final)
        goal_str = str(goal)
        delta_goal_str = str(delta_goal)
        final_goal_str = str(final_goal)
        
        prompt = f"""
        Task description: {task}.
        The initial states are: {states_init}. The final states are {states_final}.
        The goal from planner is {goal}. The change of goal from compensator is {delta_goal}. So the final goal is {final_goal}.
        The first {len_images_init} images are initial states; the following {len_images_final} images are final states.
        """
        
        return prompt, images_init + images_final