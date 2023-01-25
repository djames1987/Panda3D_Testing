# Creating a flat terrain of voxel cubes

# Imports
from direct.showbase.ShowBase import ShowBase
#from direct.directbase import DirectStart
from panda3d.core import Texture, GeomNode, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexFormat, GeomVertexWriter, Vec4, PointLight, AmbientLight, DirectionalLight, Vec3
import numpy as np

def CalcSufaceNormal(myVec):
    myVec.normalize()
    return myVec

def convertToRGBA(rVal, gVal, bVal, alpha):
    
    return (rVal/float(255),gVal/float(255),bVal/float(255),alpha)

class GenCube(object):
    def __init__(self, name = 'cube'):

        self.name = name
        self.done = False

        self.format = GeomVertexFormat.getV3n3c4()
        self.vData = GeomVertexData(self.name, self.format, Geom.UHStream)

        self.cube = Geom(self.vData)
        self.tris = GeomTriangles(Geom.UHStream)
        
        self.vertex = GeomVertexWriter(self.vData, 'vertex')
        self.normal = GeomVertexWriter(self.vData, 'normal')
        self.color = GeomVertexWriter(self.vData, 'color')

        self.faceCount = 0
    
    def makeFace(self, x1, y1, z1, x2, y2, z2, color):

        if x1 != x2:

            self.vertex.addData3f(x1, y1, z1)
            self.vertex.addData3f(x2, y1, z1)
            self.vertex.addData3f(x2, y2, z2)
            self.vertex.addData3f(x1, y2, z2)

            vector1 = Vec3(x1, y1, z1)
            vector2 = Vec3(x2, y1, z1)
            vector3 = Vec3(x2, y2, z2)
            
            normalVector1 = vector3-vector1
            normalVector2 = vector2-vector1
            normalVector2.cross(normalVector1)

            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))

        else:

            self.vertex.addData3f(x1, y1, z1)
            self.vertex.addData3f(x2, y2, z1)
            self.vertex.addData3f(x2, y2, z2)
            self.vertex.addData3f(x1, y1, z2)
            
            vector1 = Vec3(x1, y1, z1)
            vector2 = Vec3(x2, y2, z1)
            vector3 = Vec3(x2, y2, z2)
            
            normalVector1 = vector3-vector1
            normalVector2 = vector2-vector1
            normalVector2.cross(normalVector1)

            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))
            self.normal.addData3f(CalcSufaceNormal(normalVector2))

        RGBAVal = convertToRGBA(color[0], color[1], color[2], color[3])
        self.color.addData4f(RGBAVal[0], RGBAVal[1], RGBAVal[2], RGBAVal[3])
        self.color.addData4f(RGBAVal[0], RGBAVal[1], RGBAVal[2], RGBAVal[3])
        self.color.addData4f(RGBAVal[0], RGBAVal[1], RGBAVal[2], RGBAVal[3])
        self.color.addData4f(RGBAVal[0], RGBAVal[1], RGBAVal[2], RGBAVal[3])

        vertexId = self.faceCount * 4

        self.tris.addVertices(vertexId, vertexId + 1, vertexId + 3)
        self.tris.addVertices(vertexId + 1, vertexId + 2, vertexId + 3)

        self.faceCount += 1

    def makeFrontFace(self, x, y, z, color):
        print(x + 1, y + 1, z - 1, x, y + 1, z, color)
        self.makeFace(x + 1, y + 1, z - 1, x, y + 1, z, color)        

    def makeBackFace(self, x, y, z, color):
        self.makeFace(x, y, z - 1, x + 1, y, z, color)

    def makeRightFace(self, x, y, z, color):
        self.makeFace(x + 1, y, z - 1, x + 1, y + 1, z, color)

    def makeLeftFace(self, x, y, z, color):
        self.makeFace(x, y + 1, z - 1, x, y, z, color)

    def makeTopFace(self, x, y, z, color):
        self.makeFace(x + 1, y + 1, z, x, y, z, color)

    def makeBottomFace(self, x, y, z, color):
        self.makeFace(x, y + 1, z - 1, x + 1, y, z - 1, color)

    def getMesh(self):
        return self.cube

    def getGeomNode(self):
        if self.done == False:
            self.tris.closePrimitive()
            self.cube.addPrimitive(self.tris)
            self.done = True
        geomNode = GeomNode(self.name)
        geomNode.addGeom(self.cube)
        return geomNode

class Chunk(object):

    chunkSize = 0
    chunkX=0
    chunkY=0
    chunkZ=0

    def __init__(self, world):

        self.worldRef = world

    def GenerateMesh(self, renderNode):

        self.cubeModel = GenCube("Chunk"+str(self))

        r = 13
        g = 102
        b = 24
        counter = 0
        for x in range(0, self.chunkSize):
            for y in range(0, self.chunkSize):
                for z in range(0, self.chunkSize):
                    

                    if(self.Block(x,y,z) != 1):
                        #block is a solid
                        if(self.Block(x,y+1,z) == 1):
                            self.cubeModel.makeFrontFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

                        if(self.Block(x,y-1,z) == 1):
                            self.cubeModel.makeBackFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

                        if(self.Block(x+1,y,z) == 1):
                            self.cubeModel.makeRightFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

                        if(self.Block(x-1,y,z) == 1):
                            self.cubeModel.makeLeftFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

                        if(self.Block(x,y,z+1) == 1):
                            counter+=1
                            self.cubeModel.makeTopFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

                        if(self.Block(x,y,z-1) == 1):
                            self.cubeModel.makeBottomFace(x+self.chunkX,y+self.chunkY,z+self.chunkZ, [r,g,b,1])

        #print("Made Chunk with: "+str(counter)+" faces")
        self.np = renderNode.attachNewNode(self.cubeModel.getGeomNode())
        self.np.setTwoSided(True)

    def Block(self,x,y,z):
        return self.worldRef.Block(x+self.chunkX,y+self.chunkY,z+self.chunkZ)


class GenMap(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.cam.setPos(64, -128, 75)
        self.cam.setHpr(0, -25, 0)
        self.world_x = 128
        self.world_y = 128
        self.world_z = 2
        self.chunkSize = 16 
        self.chunks = None

        self.data = np.zeros([self.world_x, self.world_y, self.world_z], dtype=int)
    
    def Block(self, x, y, z):
        if (x >= self.world_x or x < 0 or y >= self.world_y or y < 0 or z >= self.world_z or z < 0):
            return 1
        else:
            return self.data[x][y][z]
    def gen_map(self):

        self.chunks = np.empty([self.world_x, self.world_y, self.world_z], dtype=Chunk)

        xCord = self.world_x // self.chunkSize
        yCord = self.world_y // self.chunkSize
        zCord = self.world_z

        for x in range(0, xCord):
            for y in range(0, yCord):
                for z in range(0, zCord):
                    self.chunks[x][y][z] = Chunk(self)
                    self.chunks[x][y][z].chunkSize = self.chunkSize
                    self.chunks[x][y][z].chunkX = x * self.chunkSize
                    self.chunks[x][y][z].chunkY = y * self.chunkSize
                    self.chunks[x][y][z].chunkZ = z * self.chunkSize
                    self.chunks[x][y][z].GenerateMesh(render)

if __name__ == '__main__':
    worldTest = GenMap()
    worldTest.gen_map()

    slight = AmbientLight('alight')
    slight.setColor(Vec4(0.2, 0.2, 0.2, 1))
    slnp1 = render.attachNewNode(slight)
    render.setLight(slnp1)

    dlight = DirectionalLight('dlight')
    dlight.set_color(Vec4(0.8, 0.8, 0.5, 1))
    dlnp = render.attachNewNode(dlight)
    dlnp.setHpr(0, -180, 0)
    render.setLight(dlnp)

    dlight2 = PointLight('dlight2')
    dlight2.set_color(Vec4(0.8, 0.8, 0.5, 1))
    dlnp1 = render.attachNewNode(dlight2)
    dlnp1.setHpr(0, -180, 60)
    render.setLight(dlnp1)

    base.run()
