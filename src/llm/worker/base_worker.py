from src.utils.py_utils import AttrDict, ParamDict
from src.llm.openai.completor_vision import OpenAICompletorVision
from src.llm.parser.exp.base_exp_parser import BaseExpParser
from src.llm.parser.assist.base_assist_parser import BaseAssistParser

class BaseWorker:
    def __init__(self):
        self._hp = self._default_hparams() # default hparams
        pass
    
    def _default_hparams(self):
        # default hparams
        default_dict = ParamDict({
            'llm': OpenAICompletorVision,   
            'exp_parser': BaseExpParser,
            'assist_parser': BaseAssistParser,
            'assist_checker': None,
            'system_prompt': None,
            'user_prompt': None,
            
        })
        return default_dict
    
    
    def reflection(self, exp_results):
        # formulate reflection
        
        # 1. parse exp results
        exp_prompt, images = self.exp_parser.parse(exp_results)
        
        # 2. formulate user
        user_prompt = self.user_prompt.format(exp_prompt=exp_prompt)
        
        # 3. reflect by llm
        # assist_results = self.llm.answer_with_image(user_prompt, images)
        
        # 4. parse assist results
        
        
    def _setup(self):
        # llm
        self.llm = self._hp.llm(api_key = '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')
        
        # exp_parser
        self.exp_parser = self._hp.exp_parser()
        # assist_parser
        
        self.assist_parser = self._hp.assist_parser()
        # assist_checker


if __name__ == "__main__":
    worker = BaseWorker()
    worker._setup()
    exp_results = {
        'states_init': [1,2,3],
        'images_init': ['a.jpg', 'b.jpg'],
        'states_final': [4,5,6],
        'images_final': ['c.jpg', 'd.jpg'],
        'goal': [7,8,9],
        'delta_goal': [10,11,12],
        'final_goal': [13,14,15]
    }
    worker.reflection(exp_results)
    
    # python src/llm/worker/base_worker.py