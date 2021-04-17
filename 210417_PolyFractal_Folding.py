"""Polygon fractal 3d folding script. 
ARCH703 Virtual Engagement_Final_Winter21'_MS_DMT_Taubman College, University of Michigan
Instructor: Glenn Wilcox
Students: Mehdi Shirvani, Ruxin Xie
"""
import rhinoscriptsyntax as rs
import math

class Fractal(object):
    def __init__(self, STRLINE, COUNT, FOLDING_ANGLE, POLY_EDGES):
        self.strline = STRLINE
        self.count = COUNT
        self.folding_angle = FOLDING_ANGLE
        self.poly_edges = POLY_EDGES

        #Call the first function
        self.FindRadius()
      
    def FindRadius(self):
        #Calculate the distance between the starting point to the center of next square
        scale = 0.65
        # rad45 = math.radians(45)
        angle = 360/(2*self.poly_edges)
        rad_angle = math.radians(angle)

        radius = rs.CurveLength(self.strline)
        
        r0 = radius * (math.cos(rad_angle))
        L = radius * (math.sin(rad_angle))

        r2 = scale * L
        R = r0 + r2

        startPt = rs.CurveStartPoint(self.strline)
        endPt = rs.CurveEndPoint(self.strline)
        trans = endPt - startPt

        self.Polygon(radius, startPt, trans)
        
        self.SquareCenter(R, r2, r0, radius, self.folding_angle , angle)
        self.SquareCenter(R, r2, r0, radius, self.folding_angle , angle*(-2)+(-1)*angle)

       
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

        self.NextPolygonCenter(r2, squarePlaneY, squareCt, rotAxis)


    def NextPolygonCenter(self, r2, squarePlaneY, squareCt, rotAxis):
        #Find the center points of the new Polygons

        rad45 = math.radians(45)
        angle = 360/(2*self.poly_edges)
        rad_angle = math.radians(angle)

        r3 = r2/(math.tan(rad_angle))
        r4 = r2/(math.sin(rad_angle))
        R1 = r2 + r3

        # squa_direction = rs.VectorRotate(direction, 45, [0,0,1])

        squa_radius = r2/(math.cos(rad45))

        self.Square(squa_radius, squareCt, squarePlaneY, rotAxis)

        #Draw the next Polygon center
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

        radius2 = r3/math.cos(rad_angle)

        newPt1_end = rs.PointAdd(unitdirection*radius2, nextStartPt)


        strline_new = rs.AddLine(nextStartPt, newPt1_end)
        rs.RotateObject(strline_new, nextStartPt, angle)

        rs.HideObject(strline_new)
        


        if self.count < 8:
            Fractal(strline_new, self.count + 1, self.folding_angle, self.poly_edges)

    def VisulizeVector(self, origin, vector):
        nextPt = rs.PointAdd(origin, vector*3000)
        line = rs.AddLine(origin, nextPt)
        circle = rs.AddCircle(nextPt, 500) 


    def Polygon(self, radius, centroid, vector):
        #Generate Polygons

        vector = rs.VectorUnitize(vector)
        pts = []

        for i in range(self.poly_edges + 1):
            pt = rs.CopyObject(centroid, vector*radius)

            # rs.AddPoint(pt)

            rotation = 360 / (self.poly_edges)
            vector = rs.VectorRotate(vector, rotation, [0,0,1])
            pts.append(pt)
        
        Polygon = rs.AddPolyline(pts)
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

    strline = rs.GetObject("Select a starting line for the Polygon fractal", rs.filter.curve)
    count = rs.GetInteger("Type the fractal recursion counts", 4)
    poly_edges = rs.GetInteger("How many sides of the polygon ", 6)    
    ask = rs.GetInteger("Do you want 2d or 3d folding?, type '2' or 3'", 3)
    print(ask)
    if ask == 2:
        folding_angle = 0
    else:
        folding_angle = rs.GetInteger("What is the folding angle then?", 90)

    Fractal(strline, count, folding_angle, poly_edges)
    
Main()