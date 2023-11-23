from src.utils.file_utils import *
from src.utils.py_utils import AttrDict, ParamDict

class Main:
    
    def __init__(self, args):
        self.args = args # args
        self.setup_device() # set up device
        self._hp = self._default_hparams() # default hparams

    def _default_hparams(self):
        # default hparams
        default_dict = ParamDict({
            'seed': 0, 
            'agent': None,
        })
        return default_dict
    
    
    
    
    
    def setup_configs(self):
        # setup configs
        pass
    
    def setup_modules(self):
        # 1. env
        
        # 2. llm
        
        # 3. compensator
        pass
    
if __name__ == "__main__":
    mkdir("./temp") # create a temp folder to store results