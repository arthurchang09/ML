"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from os import path
import pickle

import numpy as np
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    """
    filename=path.join(path.dirname(__file__), 'save', 'SVRp1.pickle')
    filename1=path.join(path.dirname(__file__), 'save', 'SVRp2.pickle')
    with open(filename, 'rb') as file:
        p1 = pickle.load(file)
    with open(filename1, 'rb') as file:
        p2 = pickle.load(file)
    a=8
    """
    filename=path.join(path.dirname(__file__), 'save', 'SVM_C.pickle')
    with open(filename, 'rb') as file:
        p1 = pickle.load(file)
    #filename1=path.join(path.dirname(__file__), 'save', 'SVM_C_2P.pickle')
    #with open(filename1, 'rb') as file:
    #    p2 = pickle.load(file)
    pre_blocker=(90,240)
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False
            pre_blocker=scene_info["blocker"]
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information
        feature=[]
        feature2=[]
        Ball=scene_info["ball"]
        Ball_speed=scene_info["ball_speed"]
        Blocker=scene_info["blocker"]
        Blocker_speed=Blocker[0]-pre_blocker[0]
        pre_blocker=scene_info["blocker"]
        p1x=scene_info["platform_1P"][0]
        p1y=scene_info["platform_1P"][1]
        p2x=scene_info["platform_2P"][0]
        p2y=scene_info["platform_2P"][1]
        feature.append(Ball[0])
        feature.append(Ball[1])
        feature.append(Ball_speed[0])
        feature.append(Ball_speed[1])
        feature.append(Blocker[0])
        feature.append(Blocker[1])
        feature.append(Blocker_speed)
        feature.append(p1x)
        feature.append(p1y)
        
        feature2.append(Ball[0])
        feature2.append(Ball[1])
        feature2.append(Ball_speed[0])
        feature2.append(Ball_speed[1])
        feature2.append(Blocker[0])
        feature2.append(Blocker[1])
        feature2.append(Blocker_speed)
        feature2.append(p2x)
        feature2.append(p2y)
        
        feature=np.array(feature)
        feature2=np.array(feature2)
        
        feature=feature.reshape(-1,9)
        feature2=feature2.reshape(-1,9)
        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            #comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_RIGHT"})
            #ball_served = True
            """
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            """
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_RIGHT"})
            ball_served = True
            """
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            
            
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            """
            
            
        else:
            """
            if a==1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                a=a+1
            elif a==2:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                a=a+1
            else:
                a=a+1
                if a>=25:
                    a=1
            """
            """
            x1=p1.predict(feature)
            x2=p2.predict(feature)
            if side=="1P":
                if x1>scene_info["plateform_1P"][0]:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                elif x1<scene_info["platform"][0]:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            else:
                if x2>scene_info["plateform_1P"][0]:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
                elif x2<scene_info["platform"][0]:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
            """
            y1=p1.predict(feature)
            #y2=p2.predict(feature2)
            if side=="1P":
                if y1==0:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                elif y1==1:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            """
            else:
                if y2==0:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
                elif y2==1:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
                else:
                    comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            """