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
            
            sample = False
            reflect = False
            
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
            
            
            # ========================================================================================
            exp_results = read_pickle_file('./temp/exp_results.pkl')
            done_reflection = False
            
            while not done_reflection:
                if reflect:
                    # 4. reflection
                    self.llm.reflection(exp_results)
                
                # 5. parse assist results
                assit = read_txt_file('./temp/assist_results/assist_results.txt')
                
                # a temporay parser
                import re, ast
                pattern = r"```(.*?)```"
                result_dict_string = re.search(pattern, assit, re.DOTALL).group(1)
                llm_results = ast.literal_eval(result_dict_string)
                    
                # print(llm_results)
                
                # 6. check and update compensator
                if 'success' in llm_results.keys():
                    if llm_results['success']:
                        print('task is successful')
                        break
                    else:
                        print('task is failed')
                        if 'change of goal' in llm_results.keys():
                            self.compensator.update(exp_results['states_init'], exp_results['goal'], llm_results['change of goal'])
                            print('compensator is updated, change of goal is: {}'.format(llm_results['change of goal']))
                            done_reflection = True
                        else:
                            print('compensator is not updated, try again')
                else:
                    print('did not get success info, try again')
            
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