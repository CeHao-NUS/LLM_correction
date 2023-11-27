from src.utils.file_utils import *
from src.utils.py_utils import AttrDict, ParamDict

from src.robot.planner.demo_planner import DemoPlanner
from src.llm.worker.base_worker import BaseWorker
from src.compensator.base_compensator import DummyCompensator

from src.robot.envs import *

class Main:
    
    def __init__(self, args):
        self.args = args # args
        # self.setup_device() # set up device
        self._hp = self._default_hparams() # default hparams
        self._setup_modules() # setup modules
        self.train() # train

    def _default_hparams(self):
        # default hparams
        default_dict = ParamDict({
            'planner': DemoPlanner, 
            'llm': BaseWorker,
            'compensator': DummyCompensator,
        })
        return default_dict
    
    def train(self):
        
        for idx in range(5):
            print(f'============================= iter {idx} ==============================')
            sample = 1
            reflect = 1
            
            self.llm.clear()
            
            if sample:
                # 1. reset
                import numpy as np
                bias = np.array([0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0])
                
                obs, goal = self.planner.reset(bias=None)
                
                # 2. compensate
                delta_goal = self.compensator.compensate(obs, goal)
                print('change of goal', delta_goal)
                final_goal = goal + delta_goal
                
                # 3. step
                res = self.planner.step(goal, delta_goal, final_goal, bias=bias)
                exp_results = self.planner.get_exp_results()
                
                print('env success checker', res)
                new_path_dir = save_path_time(EXP_DIR)
                write_pickle_file(EXP_DIR, exp_results)
                write_pickle_file(new_path_dir, exp_results)
            
            # ========================================================================================
            exp_results = read_pickle_file(EXP_DIR)

            if reflect:
                # 4. reflection
                llm_results = self.llm.reflection(exp_results)
                print('llm_results', llm_results)
                
            if llm_results['success'] == True:
                print('task is successful')
                break
            elif llm_results['success'] == False:
                # 5. update compensator
                self.compensator.update(exp_results['states_init'], exp_results['goal'], llm_results['change of goal'])
            elif llm_results['success'] == None:
                print('need more info')
                break
                


            
    def _setup_configs(self):
        # setup configs
        pass
    
    def _setup_modules(self):
        # 1. env
        self.planner = self._hp.planner()
        
        # 2. llm
        self.llm = self._hp.llm()
        
        # 3. compensator
        self.compensator = self._hp.compensator()
        
    
if __name__ == "__main__":
    mkdir("./temp") # create a temp folder to store results
    args = None
    m = Main(args) # create main object