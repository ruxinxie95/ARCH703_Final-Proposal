"""This is the quadrangle fractal 3d lamp folding. 
"""
import rhinoscriptsyntax as rs
import math

class Fractal(object):
    def __init__(self, STRLINE, COUNT, FOLDING_ANGLE):
        self.strline = STRLINE
        self.count = COUNT
        self.folding_angle = FOLDING_ANGLE

        #Call the first function
        self.FindRadius()
      
    def FindRadius(self):
        #Calculate the distance between the starting point to  the center of next square
        scale = 0.65
        rad45 = math.radians(45)
        radius = rs.CurveLength(self.strline)
        
        r0 = radius * (math.cos(rad45))
        L = radius * (math.sin(rad45))
        r2 = scale * L
        R = r0 + r2

        startPt = rs.CurveStartPoint(self.strline)
        endPt = rs.CurveEndPoint(self.strline)
        trans = endPt - startPt

        self.Quadrangle(radius, startPt, trans)
        self.SquareCenter(R, r2, r0, radius, self.folding_angle , 45.0)
        self.SquareCenter(R, r2, r0, radius, self.folding_angle , -135.0)

       
    def SquareCenter(self, R, r2, r0, radius, folding_angle, rotation): 
        #Find the square center

        line1 = self.strline
        startPt = rs.CurveStartPoint(line1)
        endPt = rs.CurveEndPoint(line1)

        #Rotate the endPt
        rs.RotateObject(endPt, startPt, rotation)
        trans = endPt - startPt
        direction = rs.VectorUnitize(trans)

        #Get the bridge point
        bridgePt = rs.PointAdd(direction * r0, startPt)

        #Generate the point of the connection square
        squareCt = rs.PointAdd(direction * R, startPt)

        #Construct rotation plane
        vector = squareCt - bridgePt
        rot_plane = rs.PlaneFromFrame(bridgePt, [0,0,-1],  vector)
        rotAxis = rot_plane.ZAxis
        
        rs.RotateObject(squareCt, bridgePt, folding_angle, rotAxis)

        squarePlaneY = squareCt - bridgePt

        # rs.AddPoint(newPt)
        self.NextQuadrangleCenter(r2, squarePlaneY, squareCt, rotAxis)



    def NextQuadrangleCenter(self, r2, squarePlaneY, squareCt, rotAxis):
        #find centerpoints of new Quadrangles
        #Translation

        rad45 = math.radians(45)
        r3 = r2/(math.tan(rad45))
        r4 = r2/(math.sin(rad45))
        R1 = r2 + r3

        # squa_direction = rs.VectorRotate(direction, 45, [0,0,1])
        rad45 = math.radians(45)
        squa_radius = r2/(math.sin(rad45))

        self.Square(squa_radius, squareCt, squarePlaneY, rotAxis)

        #Draw the next quadrangle center
        squarePlaneY = rs.VectorUnitize(squarePlaneY)
        
        bridgePt2 = rs.PointAdd(squareCt, squarePlaneY * r2)

        # self.VisulizeVector(bridgePt2, rotAxis)

        nextPlane = rs.PlaneFromFrame(bridgePt2, rotAxis, [0,0,-1])
        nextZAxis = nextPlane.ZAxis

        # self.VisulizeVector(bridgePt2, nextZAxis)
        nextZAxis = rs.VectorUnitize(nextZAxis)
        nextZAxis *= r3
        nextStartPt = rs.PointAdd(bridgePt2, nextZAxis)



        unitdirection = rs.VectorUnitize(nextZAxis)
        direction = unitdirection * R1
        newPt1 = rs.PointAdd(direction, squareCt)

        radius2 = r3/math.cos(rad45)

        newPt1_end = rs.PointAdd(unitdirection*radius2, nextStartPt)


        strline_new = rs.AddLine(nextStartPt, newPt1_end)
        rs.RotateObject(strline_new, nextStartPt, 45)
        rs.HideObject(strline_new)
        


        if self.count < 8:
            Fractal(strline_new, self.count + 1, self.folding_angle)

    def VisulizeVector(self, origin, vector):
        nextPt = rs.PointAdd(origin, vector*3000)
        line = rs.AddLine(origin, nextPt)
        circle = rs.AddCircle(nextPt, 500) 


    def Quadrangle(self, radius, centroid, vector):
        #Generate Quadrangles

        vector = rs.VectorUnitize(vector)
        pts = []

        for i in range(5):
            pt = rs.CopyObject(centroid, vector*radius)

            # rs.AddPoint(pt)

            rotation = 90
            vector = rs.VectorRotate(vector, rotation, [0,0,1])
            pts.append(pt)
        
        Quadrangle = rs.AddPolyline(pts)
        rs.DeleteObjects(pts)
    
    def Square(self, radius, centroid, PlaneY, PlaneX):
        #Generate squares that connect two pentagons

        PlaneY = rs.VectorUnitize(PlaneY)
        pts = []
        squarePlane = rs.PlaneFromFrame(centroid, PlaneX, PlaneY)
        diag_trans = PlaneX + PlaneY
        diag_trans = rs.VectorUnitize(diag_trans)

        for i in range(5):
            pt = rs.CopyObject(centroid, diag_trans*radius)

            # rs.AddPoint(pt)

            rotation = 90
            diag_trans = rs.VectorRotate(diag_trans, rotation, squarePlane.ZAxis)
            pts.append(pt)
        
        rs.AddPolyline(pts)
        rs.DeleteObjects(pts)


def Main():
    
    #select point as center point to start

    strline = rs.GetObject("select a starting line for the Quadrangle fractal", rs.filter.curve)
    count = rs.GetInteger("type counts", 4)
    folding_angle = rs.GetInteger("what is your folding angle?", 30)
    Fractal(strline, count, folding_angle)
    
Main()