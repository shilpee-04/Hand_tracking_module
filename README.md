# Hand_tracking_module
##### This "HandTrackingModule" is developed using mediapipe library in python. It has following three methods (might be added some more ):  
1.findHands(self,img,draw = True): Detects hand and draws the skeleton of hand  
2.findPosition(self, img, handNo=0, draw=False, id=range(21)): It return a list of len 21, each element has id and position of a landmark on hand  
3.fingersUp(self): Return which finger is up


##### I created following three projects using above module -
1.FingerCounter: counts how many fingers are up  
2.VolumeControler: Controls volume in proportion to distance between Thumb and Middle finger in real time  
3.AIVirtualMouse: It is a live performing mouse which works according to some gestures of fingers and thumb. It can perform Moving around screen, Left click, Right click, and Double click. It is awesome.   
