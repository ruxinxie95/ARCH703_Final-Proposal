import rhinoscriptsyntax as rs
import math
import random as rnd
import Rhino.Geometry as rg


class Apollonian():
    def __init__(self, CIRCLE, RADIUS):
        self.C1 = CIRCLE
        self.r1 = RADIUS
        
        self.drawC1()

    def drawC1(self):
        rs.AddCircle(self.C1, self.r1)
        self.pickC2()
    
    def pickC2(self):
        t = 2*math.pi*rnd.random()

        r = rnd.random() * self.r1

        x2 = self.C1[0] + r * math.cos(t)
        y2 = self.C1[1] + r * math.sin(t)
        print(x2, y2, 0)

        C2 = (x2, y2 ,0)
        rs.AddPoint(C2)

        self.drawC2(C2)

    def drawC2(self, C2):
        dist = rs.Distance(self.C1, C2)
        r2 = self.r1 - dist
        
        rs.AddCircle(C2, r2)
        x1 = self.C1[0]
        y1 = self.C1[1]
        x2 = C2[0]
        y2 = C2[1]

        self.pickC3(dist, x1, x2, y1, y2)
    
    def pickC3(self, dist, x1, x2, y1, y2):
        r3 = dist

        angle = math.atan((y2 - y1)/ float(x1-x2))
        x3 = self.r1 * math.cos(angle) + x2
        y3 = y2 - self.r1 * math.sin(angle)

        C3 = (x3, y3, 0)
        rs.AddPoint(C3)

        rs.AddCircle(C3, r3)



def main():
    
    C1 = rs.GetPoint("select a starting point")
    r1 = rs.GetInteger("enter C1 radius", 7)
    if C1 is not None:

        Apollonian(C1, r1)


main()
