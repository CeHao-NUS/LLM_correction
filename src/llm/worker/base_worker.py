from src.utils.py_utils import AttrDict, ParamDict
from src.llm.openai.completor_vision import OpenAICompletorVision
from src.llm.parser.exp.base_exp_parser import BaseExpParser
from src.llm.parser.assist.base_assist_parser import BaseAssistParser

from src.utils.file_utils import *

class BaseWorker:
    def __init__(self):
        self._hp = self._default_hparams() # default hparams
        self._setup()
    
    def _default_hparams(self):
        # default hparams
        default_dict = ParamDict({
            'llm': OpenAICompletorVision,   
            'exp_parser': BaseExpParser,
            'assist_parser': BaseAssistParser,
            'assist_checker': None,
            'system_prompt': './src/llm/prompts/system.txt',
            'user_prompt': './src/llm/prompts/user.txt',
            
        })
        return default_dict
    
    
    def reflection(self, exp_results):
        # formulate reflection
        
        # 1. parse exp results
        exp_prompt, images = self.exp_parser.parse(exp_results)
        
        # print(exp_prompt)
        
        # 2. formulate user
        user_prompt = self.user_prompt.format(exp_prompt=exp_prompt)
        # print(user_prompt)
        
        # 3. reflect by llm
        assist_results = self.llm.answer_with_image(user_prompt, images)
        # print(assist_results)
        
        # 4. parse assist results
        
        
    def _setup(self):
        # system
        self.system_prompt = read_txt_file(self._hp.system_prompt)
        
        # user
        self.user_prompt = read_txt_file(self._hp.user_prompt)
        
        # llm
        self.llm = self._hp.llm(api_key = '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')
        self.llm.add_system(self.system_prompt)
        
        # exp_parser
        self.exp_parser = self._hp.exp_parser()
        # assist_parser
        
        self.assist_parser = self._hp.assist_parser()
        # assist_checker


if __name__ == "__main__":
    worker = BaseWorker()
    exp_results = {
        'task': "grasp the red cube with gripper hand.",
        'states_init': {'hand': [0.002, -0.002, 0.165, -0.007, 1. , -0.024, -0.006], 'cube':[0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843]},
        'images_init': ['./src/temp/images/initial.png'],
        'states_final': {'hand': [0.085, 0.045, 0.058, -0.011, 0.999, -0.044, 0.018], 'cube':[0.074, 0.042, 0.066, -0.564, -0.004, -0.005, 0.825]},
        'images_final': ['./src/temp/images/succ.png'],
        'goal': [0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843],
        'delta_goal': [0, 0, 0, 0, 0, 0, 0],
        'final_goal': [0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843],
    }
    worker.reflection(exp_results)
    
    # python src/llm/worker/base_worker.py