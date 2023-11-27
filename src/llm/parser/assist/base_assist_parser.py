from src.utils.file_utils import *

class BaseAssistParser:
    def __init__(self):
        pass
    
import re
import ast
    
if __name__ == '__main__':
    # p = """
    #     ```
    #     "result": 123
    #     ```, yes, not , hello
    # """
    # s = re.search('```\n(.*)\n```', p)
    # s = '{' + s.group(1) + '}'
    
    # b = ast.literal_eval(s)
    
    # print(b)
    
    
    string = """
        ```
        {
            'success': False,
            'change of goal': [-0.0059, -0.01955, -0.0141, 0, 0, 0, 0],
        }
        ```
        """
    
    # string = read_txt_file('./temp/assist_results/assist_results.txt')

    pattern = r"```(.*?)```"
    match = re.resarch(pattern, string, re.DOTALL)  # re.DOTALL makes '.' match newlines as well

    b = ast.literal_eval(match.group(1))

    # if match:
    #     content = match.group(1).strip()  # This extracts the content within the backticks and strips any leading/trailing whitespace
    #     print(content)
    # else:
    #     print("No match found")
