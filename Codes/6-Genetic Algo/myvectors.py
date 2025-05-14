from math import sqrt


class Vec: 
    ### vectors will be couples (x,y) (positions, velocity, acceleration)
    def __init__(self,v):
        self.x = v[0]
        self.y = v[1]

    def print(self):
        print(f" my coordinates are {self.x} and {self.y}")

    def vadd(self,other): 
        self.x = self.x + other.x
        self.y = self.y + other.y 
      
    def vtimes(self,s):
        ## multiplication by a scalar
        self.x = self.x * s
        self.y = self.y * s

    def vnorm(self,ampl=1):
        n = max(sqrt(self.x * self.x  + self.y * self.y) / ampl,1)
        self.x = self.x / n
        self.y = self.y / n

    def size(self):
        print(sqrt(self.x**2 + self.y**2))

    def vdist(self,other): 
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)