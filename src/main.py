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
        
        for idx in range(1):
            
            sample = False
            
            if sample:
                # 1. reset
                import numpy as np
                bias = np.array([0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0])
                
                obs, goal = self.planner.reset(bias=None)
                
                # 2. compensate
                delta_goal = self.compensator.compensate(obs, goal)
                final_goal = goal + delta_goal
                
                # 3. step
                res = self.planner.step(goal, delta_goal, final_goal, bias=bias)
                exp_results = self.planner.get_exp_results()
                
                print('success', res)
                write_pickle_file('./temp/exp_results.pkl', exp_results)
            
            
                exp_results = read_pickle_file('./temp/exp_results.pkl')
                
                # 4. update
                self.llm.reflection(exp_results)
            
            # 5. parse
    
    
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