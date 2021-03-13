from sprites import Sprite, MovableSprite
import numpy as np


class Ufo(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, color, x_speed=1):
        self.initArray()
        self.height, self.width = self.array.shape[:2]
        super().__init__(x_coordinate, y_coordinate, self.width, self.height, color, x_speed)

    def initArray(self):
        ufo = """
         \\  _.-'~~~~'-._   /          
  .      .-~ \\__/  \\__/ ~-.         .
       .-~   (oo)  (oo)    ~-.         
      (_____//~~\\\\//~~\\\\______)    
 _.-~`                         `~-._   
/O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O\\ 
\\___________________________________/ 
           \\x x x x x x x/            
   .  *     \\x_x_x_x_x_x/             """

        self.array = ufo.split("\n")[1:]
        for i in range(len(self.array)):
            self.array[i] = list(self.array[i])

        self.array = np.array(self.array, dtype=object)
