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
        user_prompt  = user_prompt + '''
        Please answer the questions (1) and (2)
        '''
        
        # 3. reflect by llm
        prompt2 = '''
        Please answer the following questions (3)
        '''
        prompt3 = '''
        Please answer the following questions (4)
        '''
        assist_results1 = self.llm.answer_with_image(user_prompt, images)
        assist_results2 = self.llm.answer(prompt2)
        assist_results3 = self.llm.answer(prompt3)
        
        all_results = assist_results1 + "========== \n \n" + assist_results2 + "========== \n \n" + assist_results3
        
        # print(assist_results)
        mkdir('./src/temp/assist_results')
        write_txt_file('./src/temp/assist_results/assist_results.txt', all_results)
        
        # 4. parse assist results
        
        
    def _setup(self):
        # system
        self.system_prompt = read_txt_file(self._hp.system_prompt)
        
        # user
        self.user_prompt = read_txt_file(self._hp.user_prompt)
        
        # llm
        # api_key = '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'
        api_key = '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'
        self.llm = self._hp.llm(api_key=api_key)
        self.llm.add_system(self.system_prompt)
        
        # exp_parser
        self.exp_parser = self._hp.exp_parser()
        # assist_parser
        
        self.assist_parser = self._hp.assist_parser()
        # assist_checker


if __name__ == "__main__":
    worker = BaseWorker()
    
    from src.llm.worker.store import exp_results_base, exp_results_test
    # exp_results = exp_results_base
    exp_results = exp_results_test
    
    worker.reflection(exp_results)
    
    # python src/llm/worker/base_worker.py