import random
class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.next=self.car_lane
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        warning=0       #0 no forward 1 forward car 
        forward=()
        near = set()
        speed=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        before=0
        if self.car_pos!=(): 
            self.car_lane = self.car_pos[0] // 70
            #print(self.car_lane)
            before=self.next
            if self.car_lane==0:
                near.add(2)
                near.add(7)
                near.add(12)
                near.add(1)
                near.add(6)
                near.add(11)
                speed[12]=20
                speed[11]=20
            elif self.car_lane==1:
                near.add(1)
                near.add(6)
                near.add(11)
                speed[11]=20
            elif self.car_lane==8:
                near.add(4)
                near.add(9)
                near.add(14)
                near.add(5)
                near.add(10)
                near.add(15)
                speed[14]=20
                speed[15]=20
            elif self.car_lane==7:
                near.add(5)
                near.add(10)
                near.add(15)
                speed[15]=20
            for car in scene_info["cars_info"]:
                    if car["id"] != self.player_no:
                        x = self.car_pos[0] - car["pos"][0]
                        y = self.car_pos[1] - car["pos"][1]
                        car_lane=car["pos"][0]//70
                        if car_lane==self.car_lane:
                            if y>0 and y<300:
                                near.add(3)
                                speed[3]=car["velocity"]
                                if y<250:
                                    near.add(8)
                                    speed[8]=car["velocity"]
                                    if y<100:
                                        return ["BRAKE"]
                            elif y<0 and y>-200:
                                near.add(13)
                                speed[13]=car["velocity"]
                        if y<80 and y>-80:
                            if car_lane==self.car_lane+2:
                                near.add(10)
                                speed[10]=car["velocity"]
                            elif car_lane==self.car_lane+1:
                                near.add(9)
                                speed[9]=car["velocity"]
                            elif car_lane==self.car_lane-1:
                                near.add(7)
                                speed[7]=car["velocity"]
                            elif car_lane==self.car_lane-2:
                                near.add(6)
                                speed[6]=car["velocity"]
                        if y > 80 and y < 250:
                            if car_lane==self.car_lane+2:
                                near.add(5)
                                speed[5]=car["velocity"]
                            elif car_lane==self.car_lane+1:
                                near.add(4)
                                speed[4]=car["velocity"]
                            elif car_lane==self.car_lane-1:
                                near.add(2)
                                speed[2]=car["velocity"]
                            elif car_lane==self.car_lane-2:
                                near.add(1)
                                speed[1]=car["velocity"]
                        if y < -80 and y > -200:
                            if car_lane==self.car_lane+2:
                                near.add(15)
                                speed[15]=car["velocity"]
                            elif car_lane==self.car_lane+1:
                                near.add(14)
                                speed[14]=car["velocity"]
                            elif car_lane==self.car_lane-1:
                                near.add(12)
                                speed[12]=car["velocity"]
                            elif car_lane==self.car_lane-2:
                                near.add(11)
                                speed[11]=car["velocity"]
            #print(near,"   ",speed)
            brake=0
            if len(near)==0:
                self.next=self.car_lane
            else:
                if 3 not in near:
                    self.next=self.car_lane
                else:
                    if 8 in near:
                        if (2 not in near) and (7 not in near) and speed[12]<=self.car_vel:  #left 1 no car
                            if  (4 not in near) and (9 not in near) and speed[14]<self.car_vel:  #right 1 no car
                                if (1 not in near) and (6 not in near) :    #left 2 no car
                                    if (5 not in near) and (10 not in near): #right 2 no car 
                                        """
                                        if random.randint(0,99)%2==1:
                                            self.next=self.car_lane+1
                                        else:
                                            self.next=self.car_lane-1
                                        """
                                        self.next=self.car_lane-1
                                    else: #right 2 has car
                                        self.next=self.car_lane-1
                                else:#left 2 has car
                                    if (5 not in near) and (10 not in near): #right 2 no car 
                                        self.next=self.car_lane+1
                                    else:   #right 2 has car
                                        """
                                        if random.randint(0,99)%2==1:
                                            self.next=self.car_lane+1
                                        else:
                                            self.next=self.car_lane-1
                                        """
                                        self.next=self.car_lane-1
                            else:   #right 1 has car 
                                self.next=self.car_lane-1
                        else: #left 1 has car
                            if  (4 not in near) and (9 not in near) and speed[14]<=self.car_vel:  #right 1 no car
                                self.next=self.car_lane+1
                            else:   # right1 has car
                                print("hi")
                                if (7 not in near) and speed[12]<=self.car_vel: #left middle no car and back is slow
                                    if (9 not in near) and speed[14]<=self.car_vel: #right  middle no car and back is slow
                                        #if random.randint(0,99)%2==1:
                                        #    self.next=self.car_lane+1
                                        #else:
                                        #    self.next=self.car_lane-1
                                        self.next=self.car_lane+1
                                    else: #right middle has car or back is fast
                                        self.next=self.car_lane-1
                                else: #left middle has car or back is fast
                                    if (9 not in near) and speed[14]<=self.car_vel: #right  middle no car and back is slow
                                        self.next=self.car_lane+1
                                    else:   #right middle has car or back is fast
                                        if (7 not in near) and (9 not in near):
                                            """
                                            if random.randint(0,99)%2==1:
                                                self.next=self.car_lane+1
                                            else:
                                                self.next=self.car_lane-1
                                            """
                                            self.next=self.car_lane-1
                                        elif 7 not in near:
                                            self.next=self.car_lane-1
                                        elif 9 not in near:
                                            self.next=self.car_lane+1
                                        else:
                                            brake=1
                    else:
                         if (2 not in near) and (7 not in near) and speed[12]<=self.car_vel:  #left 1 no car
                            if  (4 not in near) and (9 not in near) and speed[14]<self.car_vel:  #right 1 no car
                                if (1 not in near) and (6 not in near) :    #left 2 no car
                                    if (5 not in near) and (10 not in near): #right 2 no car 
                                        """
                                        if random.randint(0,99)%2==1:
                                            self.next=self.car_lane+1
                                        else:
                                            self.next=self.car_lane-1
                                        """
                                        self.next=self.car_lane-1
                                    else: #right 2 has car
                                        self.next=self.car_lane-1
                                else:#left 2 has car
                                    if (5 not in near) and (10 not in near): #right 2 no car 
                                        self.next=self.car_lane+1
                                    else:   #right 2 has car
                                        """
                                        if random.randint(0,99)%2==1:
                                            self.next=self.car_lane+1
                                        else:
                                            self.next=self.car_lane-1
                                        """
                                        self.next=self.car_lane-1
                            else:   #right 1 has car 
                                self.next=self.car_lane-1
                         else: #left 1 has car
                            if  (4 not in near) and (9 not in near) and speed[14]<=self.car_vel:  #right 1 no car
                                self.next=self.car_lane+1
                            else:   # right1 has car
                                print("hi")
                                if (7 not in near) and speed[12]<=self.car_vel: #left middle no car and back is slow
                                    if (9 not in near) and speed[14]<=self.car_vel: #right  middle no car and back is slow
                                        #if random.randint(0,99)%2==1:
                                        #    self.next=self.car_lane+1
                                        #else:
                                        #    self.next=self.car_lane-1
                                        self.next=self.car_lane+1
                                    else: #right middle has car or back is fast
                                        self.next=self.car_lane-1
                                else: #left middle has car or back is fast
                                    if (9 not in near) and speed[14]<=self.car_vel: #right  middle no car and back is slow
                                        self.next=self.car_lane+1
                                    else:   #right middle has car or back is fast
                                        if (7 not in near) and (9 not in near):
                                            """
                                            if random.randint(0,99)%2==1:
                                                self.next=self.car_lane+1
                                            else:
                                                self.next=self.car_lane-1
                                            """
                                            self.next=self.car_lane-1
                                        elif 7 not in near:
                                            self.next=self.car_lane-1
                                        elif 9 not in near:
                                            self.next=self.car_lane+1
                                        else:
                                            brake=1
                        
            if self.next<0:
                self.next=0
            print(near,"   ",self.next)
            if (self.car_lane!= before) or self.car_pos[0]!=self.lanes[before]:
                print("not yet")
                if self.next==self.car_lane:
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                elif self.next==self.car_lane+1:
                    return ["SPEED","MOVE_RIGHT"]
                elif self.next==self.car_lane-1:
                    return ["SPEED","MOVE_LEFT"]
            if brake==1:
                return ["BRAKE"]
            elif self.next==self.car_lane:
                if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                else :return ["SPEED"]
            elif self.next==self.car_lane+1:
                return ["SPEED","MOVE_RIGHT"]
            elif self.next==self.car_lane-1:
                return ["SPEED","MOVE_LEFT"]
                                            
        #return ["MOVE_LEFT", "MOVE_RIGHT", "SPEED", "BRAKE"]


    def reset(self):
        """
        Reset the status
        """
        pass
