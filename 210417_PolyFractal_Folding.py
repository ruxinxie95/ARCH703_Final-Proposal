"""Polygon fractal 3d folding script. 
ARCH703 Virtual Engagement_Final_Winter21'_MS_DMT_Taubman College, University of Michigan
Instructor: Glenn Wilcox
Students: Mehdi Shirvani, Ruxin Xie
"""
import rhinoscriptsyntax as rs
import math
import Rhino.Geometry as rg
from System.Drawing import Color


class Fractal(object):
    def __init__(self, STRLINE, COUNT, FOLDING_ANGLE, POLY_EDGES, SCALE):
        self.strline = STRLINE
        self.count = COUNT
        self.folding_angle = FOLDING_ANGLE
        self.poly_edges = POLY_EDGES
        self.scale = SCALE

        #Call the first function
        self.FindRadius()
      
    def FindRadius(self):
        #Calculate the distance between the starting point to the center of next square

        # rad45 = math.radians(45)
        angle = 360/(2*self.poly_edges)
        rad_angle = math.radians(angle)

        radius = rs.CurveLength(self.strline)
        
        r0 = radius * (math.cos(rad_angle))
        L = radius * (math.sin(rad_angle))

        r2 = self.scale * L
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

        endPt1 = rs.RotateObject(endPt, startPt, rotation)
        rs.DeleteObject(endPt1)

        trans = endPt - startPt
        # rs.VectorRotate(trans, rotation, [0,0,1])

        direction = rs.VectorUnitize(trans)

        #Get the bridge point
        bridgePt = rs.PointAdd(direction * r0, startPt)

        #Generate the point of the connection square
        squareCt = rs.PointAdd(direction * R, startPt)


        #Construct rotation plane
        vector = squareCt - bridgePt


        rot_plane = rs.PlaneFromFrame(bridgePt, [0,0,-1],  vector)
        rotAxis = rot_plane.ZAxis
        
        squareCt1 = rs.RotateObject(squareCt, bridgePt, folding_angle, rotAxis, False)
        rs.DeleteObject(squareCt1)
        squarePlaneY = squareCt - bridgePt

        self.NextPolygonCenter(r2, squarePlaneY, squareCt, rotAxis)
        squareCt = rs.AddPoint(squareCt)
        rs.DeleteObject(squareCt)

    def NextPolygonCenter(self, r2, squarePlaneY, squareCt, rotAxis):
        #Find the center points of the new Polygons

        rad45 = math.radians(45)

        angle = 360 / (2 * self.poly_edges)
        rad_angle = math.radians(angle)
        r3 = r2/(math.tan(rad_angle))
        r4 = r2/(math.sin(rad_angle))

        R1 = r2 + r3

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

        if self.poly_edges % 2 == 0:
            angle = 360 / (2 * self.poly_edges)

        else:
            angle = 360 / self.poly_edges

        rs.RotateObject(strline_new, nextStartPt, angle)


        rs.ObjectLayer(strline_new, "Construction lines")
    
        if self.count > 1:
            Fractal(strline_new, self.count - 1, self.folding_angle, self.poly_edges, self.scale)

    def VisulizeVector(self, origin, vector):
        nextPt = rs.PointAdd(origin, vector*30)
        line = rs.AddLine(origin, nextPt)
        circle = rs.AddCircle(nextPt, 5) 
 

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
        lines = []
        Polygon = rs.AddPolyline(pts)

        #Create polygon surface
        for count, value in enumerate(pts):
            if count >0:
                line = rs.AddLine(pts[count-1], pts[count])
                lines.append(line)
        srf = rs.AddPlanarSrf(lines)

        #Specify layers
        rs.ObjectLayer(srf, "Polygons")
        rs.ObjectLayer(Polygon, "Polygons")

        rs.DeleteObjects(pts)
        rs.DeleteObjects(lines)

    
    def Square(self, radius, centroid, PlaneY, PlaneX):
        #Generate squares that connect two pentagons
        PlaneY = rs.VectorUnitize(PlaneY)
        pts = []
        lines = []
        squarePlane = rs.PlaneFromFrame(centroid, PlaneX, PlaneY)
        diag_trans = PlaneX + PlaneY
        diag_trans = rs.VectorUnitize(diag_trans)

        for i in range(5):
            pt = rs.CopyObject(centroid, diag_trans*radius)

            # rs.AddPoint(pt)

            rotation = 90
            diag_trans = rs.VectorRotate(diag_trans, rotation, squarePlane.ZAxis)
            pts.append(pt)
        
        square = rs.AddPolyline(pts)

        #Create polygon surface
        for count, value in enumerate(pts):
            if count >0:
                line = rs.AddLine(pts[count-1], pts[count])
                lines.append(line)
        srf = rs.AddPlanarSrf(lines)

        #Specify layers
        rs.ObjectLayer(srf, "Connection Squares")
        rs.ObjectLayer(square, "Connection Squares")

        rs.DeleteObjects(pts)
        rs.DeleteObjects(lines)


def Main():

    #Setup the input param
    
    strline = rs.GetObject("Select a starting line for the Polygon fractal", rs.filter.curve)
    frac_count = rs.GetInteger("Type in the fractal recursion counts", 2)
    frac_count += 1
    poly_edges = rs.GetInteger("How many sides of the polygon?", 6)
    scale = rs.GetReal("The scale of the squares compared with the polygon: ", 0.8, 0.1, 1)    
    ask = rs.GetInteger("Do you want 2d or 3d folding?, type '2' or 3'", 3)
    if ask == 2:
        folding_angle = 0
    else:
        folding_angle = rs.GetInteger("What is the folding angle then?", -90)
    
    #Creat layers to collect the result/ construction lines
    rs.AddLayer("Polygons",Color.Yellow)
    rs.AddLayer("Connection Squares", Color.Blue)
    rs.AddLayer("Construction lines", Color.DarkSeaGreen)

    #Call Fractal class
    if strline is not None:
        rs.EnableRedraw(False)
        Fractal(strline, frac_count, folding_angle, poly_edges, scale)
        rs.EnableRedraw(True)
        if rs.LayerVisible("Construction lines") == True:
            rs.LayerVisible("Construction lines", False)

    
Main()