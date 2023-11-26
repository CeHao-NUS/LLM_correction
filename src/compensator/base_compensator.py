import numpy as np

class BaseCompensator:
    
    def __init__(self):
        pass
    
    def compensate(self, state, goal):
        # return delta_goal
        raise NotImplementedError
    
    def update(self, state, goal, delta_goal):
        raise NotImplementedError
    
class DummyCompensator(BaseCompensator):
    def __init__(self):
        self.delta_goal = np.zeros(7)
        super().__init__()
    
    def compensate(self, state, goal):
        return self.delta_goal
    
    def update(self, state, goal, delta_goal):
        self.delta_goal = delta_goal
        