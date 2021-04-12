"""This is the pentagon fractal.
"""
import rhinoscriptsyntax as rs
import math

class Fractal(object):
    def __init__(self, STRLINE, COUNT):

        self.strline = STRLINE
        self.count = COUNT

        self.FindRadius()

        
    ##Step1 - Find Radius
    def FindRadius(self):
        
        scale = 0.8
        rad36 = math.radians(36)
        radius = rs.CurveLength(self.strline)
        
        r0 = radius * (math.cos(rad36))
        L = radius * (math.sin(rad36))
        r2 = scale * L
        R = r0 + r2

        startPt = rs.CurveStartPoint(self.strline)
        endPt = rs.CurveEndPoint(self.strline)
        trans = endPt - startPt

        self.Pentagon(radius, startPt, trans)
        self.SquareCenter(R, r2, radius)
        self.SquareCenter2(R, r2, radius)
       
    def SquareCenter(self, R, r2, radius): 
        #Find the square center
        line1 = self.strline
        startPt = rs.CurveStartPoint(line1)
        rs.RotateObject(line1, startPt, 36)
        endPt = rs.CurveEndPoint(line1)



        
        trans = endPt - startPt
        direction = rs.VectorUnitize(trans)
        direction = direction * R

        newPt = rs.PointAdd(direction, startPt)
        # rs.AddPoint(newPt)
        self.NextPentagonCenter(r2, direction, newPt)

    def SquareCenter2(self, R, r2, radius): 
        #Find the square center
        line2 = self.strline
        startPt = rs.CurveStartPoint(line2)
        rs.RotateObject(line2, startPt, -72)
        endPt = rs.CurveEndPoint(line2)


        
        trans = endPt - startPt
        direction = rs.VectorUnitize(trans)
        direction = direction * R

        newPt = rs.PointAdd(direction, startPt)
        # rs.AddPoint(newPt)
        self.NextPentagonCenter(r2, direction, newPt)


        
    def NextPentagonCenter(self, r2, direction, newPt):
        #find centerpoints of new pentagons
        #Translation

        rad36 = math.radians(36)
        r3 = r2/(math.tan(rad36))
        r4 = r2/(math.sin(rad36))
        R1 = r2 + r3

        squa_direction = rs.VectorRotate(direction, 45, [0,0,1])
        rad45 = math.radians(45)
        squa_radius = r2/(math.sin(rad45))

        self.Square(squa_radius, newPt, squa_direction)
        
        rs.VectorRotate(direction, -45, [0,0,1])

        unitdirection = rs.VectorUnitize(direction)
        direction = unitdirection * R1
        newPt1 = rs.PointAdd(direction, newPt)
        # rs.AddPoint(newPt1)

        radius2 = r3/math.cos(rad36)

        newPt1_end = rs.PointAdd(unitdirection*radius2, newPt1)
        strline_new = rs.AddLine(newPt1, newPt1_end)
        rs.HideObject(strline_new)

   
        if self.count < 6:
            Fractal(strline_new, self.count + 1)
    
    def Pentagon(self, radius, centroid, vector):
        #Generate pentagons

        vector = rs.VectorUnitize(vector)
        pts = []

        for i in range(6):
            pt = rs.CopyObject(centroid, vector*radius)

            # rs.AddPoint(pt)

            rotation = 72
            vector = rs.VectorRotate(vector, rotation, [0,0,1])
            pts.append(pt)
        
        rs.AddPolyline(pts)
        rs.DeleteObjects(pts)
    
    def Square(self, radius, centroid, vector):
        #Generate squares that connect two pentagons

        vector = rs.VectorUnitize(vector)
        pts = []

        for i in range(5):
            pt = rs.CopyObject(centroid, vector*radius)

            # rs.AddPoint(pt)

            rotation = 90
            vector = rs.VectorRotate(vector, rotation, [0,0,1])
            pts.append(pt)
        
        rs.AddPolyline(pts)
        rs.DeleteObjects(pts)


def Main():
    
    #select point as center point to start

    strline = rs.GetObject("select a starting line", rs.filter.curve)
    count = rs.GetInteger("type counts", 4)

    Fractal(strline, count)
    
Main()