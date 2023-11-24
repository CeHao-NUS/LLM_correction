

exp_results_base = {
        'task': "grasp the red cube with gripper hand.",
        'states_init': {'hand': [0.002, -0.002, 0.165, -0.007, 1. , -0.024, -0.006], 'cube':[0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843]},
        'images_init': ['./src/temp/images/initial.png'],
        
        # succ
        'states_final': {'hand': [0.085, 0.045, 0.058, -0.011, 0.999, -0.044, 0.018], 'cube':[0.074, 0.042, 0.066, -0.564, -0.004, -0.005, 0.825]},
        'images_final': ['./src/temp/images/succ.png'],
        
        # fail
        # 'states_final': {'hand': [0.005, -0.04 , 0.031, -0.007, 1. , -0.025, -0.008], 'cube':[0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843]},
        # 'images_final': ['./src/temp/images/fail.png'],
        
        
        'goal': [0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843],
        'delta_goal': [0, 0, 0, 0, 0, 0, 0],
        'final_goal': [0.074, 0.037, 0.02 , -0.539, -0. , 0. , 0.843],
    }

exp_results_test = {
        'task': 'grasp the green cube Franka Panda robot hand.',
        'states_init': {'hand': [0.61491, -0.0149375, 0.163396, 0.016978, 0.999406, 0.0243841, -0.00156698], 'cube':[0.559831, -0.000170831, 0.0200164, 0.707, 5.71526e-09, 3.72529e-09, -0.707]},
        'images_init': ['./src/temp/images/init_head_camera.png',
                        './src/temp/images/init_right_camera.png',
                        './src/temp/images/init_hand_camera.png'],
        
        'states_final': {'hand': [0.555736, -8.44061e-05, 0.0264938, 0.0167019, 0.999411, 0.0241847, 0.00342211], 'cube':[0.560008, -0.000116406, 0.0188121, 0.706898, -0.00192597, 0.00153267, -0.707097]},
        'images_final': ['./src/temp/images/final_head_camera.png',
                         './src/temp/images/final_right_camera.png',
                        './src/temp/images/final_hand_camera.png'],
    
        
        
        'goal': [0.559831, -0.000170831, 0.0200164, 0.707, 5.71526e-09, 3.72529e-09, -0.707],
        'delta_goal': [0, 0, 0, 0, 0, 0, 0],
        'final_goal': [0.559831, -0.000170831, 0.0200164, 0.707, 5.71526e-09, 3.72529e-09, -0.707],
    }