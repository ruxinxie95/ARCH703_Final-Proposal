"""This is the hexagon fractal. 
"""
import rhinoscriptsyntax as rs
import math
import Rhino.Geometry as rg  

class Fractal(object):
    def __init__(self, STRLINE, COUNT):

        self.strline = STRLINE
        self.count = COUNT

        self.FindRadius()

        
    def FindRadius(self):
        
        scale = 0.75
        rad30 = math.radians(30)
        radius = rs.CurveLength(self.strline)
        
        r0 = radius * (math.cos(rad30))
        L = radius * (math.sin(rad30))
        r2 = scale * L
        R = r0 + r2

        startPt = rs.CurveStartPoint(self.strline)
        endPt = rs.CurveEndPoint(self.strline)
        trans = endPt - startPt

        self.Hexagon(radius, startPt, trans)
        self.SquareCenter(R, r2, radius, r0)
        self.SquareCenter2(R, r2, radius)
       
    def SquareCenter(self, R, r2, radius, r0): 
        #Find the square center
        line1 = self.strline
        startPt = rs.CurveStartPoint(line1)
        rs.RotateObject(line1, startPt, 30)
        endPt = rs.CurveEndPoint(line1)

        
        trans = endPt - startPt
        direction = rs.VectorUnitize(trans)
        direction = direction * R

        #Create the new point        
        newPt = rs.PointAdd(direction, startPt)
        # rs.AddPoint(newPt)

        #Create the rotation plane
        x_dir = direction
        y_dir = (0,0,1)
        origin = rs.PointAdd(startPt, direction * r0)
        # rot_plane = rs.PlaneFromFrame(origin, x_dir, y_dir)
        rot_plane = rs.CurvePerpFrame(line1, 0.5)

        #Rotate the square point based on rotation plane
        rot_axis = rot_plane.ZAxis
        print(rot_axis)

        rad45 = math.radians(45)
        rs.RotateObject(newPt, origin, 90.0, rot_plane, copy=True)
        rs.AddPoint(newPt)

        #New direction for square
        direction = rs.VectorCreate(origin, newPt)

        self.NextHexagonCenter(r2, direction, newPt)

    def SquareCenter2(self, R, r2, radius): 
        #Find the square center
        line2 = self.strline
        startPt = rs.CurveStartPoint(line2)
        rs.RotateObject(line2, startPt, -120)
        endPt = rs.CurveEndPoint(line2)


        
        trans = endPt - startPt
        direction = rs.VectorUnitize(trans)
        direction = direction * R

        newPt = rs.PointAdd(direction, startPt)
        rs.AddPoint(newPt)
        self.NextHexagonCenter(r2, direction, newPt)


        
    def NextHexagonCenter(self, r2, direction, newPt):
        #find centerpoints of new hexagons
        #Translation

        rad30 = math.radians(30)
        r3 = r2/(math.tan(rad30))
        r4 = r2/(math.sin(rad30))
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

        radius2 = r3/math.cos(rad30)

        newPt1_end = rs.PointAdd(unitdirection*radius2, newPt1)
        strline_new = rs.AddLine(newPt1, newPt1_end)
        rs.RotateObject(strline_new, newPt1, 30)
        rs.HideObject(strline_new)
        


        if self.count < 8:
            Fractal(strline_new, self.count + 1)
    
    def Hexagon(self, radius, centroid, vector):
        #Generate Hexagons

        vector = rs.VectorUnitize(vector)
        pts = []

        for i in range(7):
            pt = rs.CopyObject(centroid, vector*radius)

            # rs.AddPoint(pt)

            rotation = 60
            vector = rs.VectorRotate(vector, rotation, [0,0,1])
            pts.append(pt)
        
        hexagon = rs.AddPolyline(pts)
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

    strline = rs.GetObject("select a starting line for the hexagon fractal", rs.filter.curve)
    count = rs.GetInteger("type counts", 7)

    Fractal(strline, count)
    
Main()