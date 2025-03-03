"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: Thirsty Crow
*  MODULE: Task1.1
*  Filename: detect.py
*  Version: 1.0.0  
*  Date: October 31, 2018
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""



'''
* Team Id : 2149
* Author List : Anirudh S,Rahul Kr ,Kishan S
* Filename: GLteapot.py
* Theme: Thirsty Crow
* Functions:getCameraMatrix,init_gl,find_object,resize,drawGLScene,detect_markers
draw_background,init_object_texture,overlay
* Global Variables:wp, rock
'''




### NOTE THAT ALL THESE FUNCTIONS ARE IMPORTED TO shortestpath.py###






import numpy as np
import cv2
import scipy.misc

import cv2.aruco as aruco
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame
from objloader import *



texture_object = None
texture_background = None
camera_matrix = None
dist_coeff = None
cap = cv2.VideoCapture(1)
water_pitcher = None
pebble_full = None
pebble_half=None
INVERSE_MATRIX = np.array([[ 1.0, 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [ 1.0, 1.0, 1.0, 1.0]])
 

################## Define Utility Functions Here #######################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('System.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]



########################################################################

############# Main Function and Initialisations ########################
"""
Function Name : main()
Input: None
Output: None
Purpose: Initialises OpenGL window and callback functions. Then starts the event
         processing loop.
"""        
def main():
        global rock#for aruco marker object("full" or "half")
        global wp #texture for water pitcher("low or high")
        wp="low" #inital declaration
        
        rock="full"
        glutInit()
        getCameraMatrix()
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(625, 100)
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        window_id = glutCreateWindow("OpenGL")
        init_gl()
        glutDisplayFunc(drawGLScene)
        glutIdleFunc(drawGLScene)
        glutReshapeFunc(resize)
        glutMainLoop()



"""
Function Name : init_gl()
Input: None
Output: None
Purpose: Initialises various parameters related to OpenGL scene.
"""  
def init_gl():
        global texture_object, texture_background
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        
        
        global water_pitcher
        global pebble_full
        global pebble_half
        global texture_object, texture_background
       
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        texture_background = glGenTextures(1)
        texture_object = glGenTextures(1)
        water_pitcher = OBJ('water_pitcher.obj', swapyz=True)
        pebble_full= OBJ('ey1.mtl.obj', swapyz=True)
        pebble_half= OBJ('ey2.mtl.obj', swapyz=True)
        j=0
        count=0
    
"""
Function Name : find_object()
Input: water_pitcher state("high" or "low"),pebble state("half" or "full")
Output: None
Purpose: Updates the global variable wp and rock from parameters
"""
def find_object(obj1,obj2):
        
        global wp
        wp=obj1
        global rock
        rock=obj2
        


"""
Function Name : resize()
Input: None
Output: None
Purpose: Initialises the projection matrix of OpenGL scene
"""
def resize(w,h):
        ratio = 1.0* w / h
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,w,h)
        gluPerspective(45, ratio, 0.1, 100.0)

"""
Function Name : drawGLScene()
Input: None
Output: None
Purpose: It is the main callback function which is called again and
         again by the event processing loop. In this loop, the webcam frame
         is received and set as background for OpenGL scene. ArUco marker is
         detected in the webcam frame and 3D model is overlayed on the marker
         by calling the overlay() function.
"""
def drawGLScene():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        ar_list = []
        ret, frame = cap.read()
        if ret == True:
                draw_background(frame)
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                ar_list = detect_markers(frame)
                     
                for i in ar_list:
                        if i[0] == 0:#for water_pitcher
                                if(wp=="low" ):#overlays the water_picher_low texture
                                        overlay(frame, ar_list, i[0],"water_pitcher_low.png","water_pitcher")
                                elif(wp=="high"):#overlays the water_picher_high texture
                                        overlay(frame, ar_list, i[0],"water_pitcher_high.png","water_pitcher")
                                        
                        else:                
                                        
                                if(rock=="half"):#overlays the pebble half ar object
                                        overlay(frame, ar_list, i[0],"rock.jpg","pebble_half")
                                        
                                elif(rock=="full"):#overlays the pebble full ar object
                                        overlay(frame, ar_list, i[0],"rock.jpg","pebble_full")
                                        
                #else:
                #       print("lol")
                     
                                        
                cv2.imshow('frame', frame)
                
                cv2.waitKey(1)
                
        glutSwapBuffers()
        
########################################################################

######################## Aruco Detection Function ######################
"""
Function Name : detect_markers()
Input: img (numpy array)
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img):
        
        
        
        
        ######################## INSERT CODE HERE ########################
        aruco_list = []
        
        markerLength = 100
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict,parameters = parameters)
        aruco.drawDetectedMarkers(img, corners,ids)
        tvecsnp=np.empty(shape=[0,3])
        rvecsnp=np.empty(shape=[0,3])
        rvecsd=np.float32()
        rvecs, tveci,_= aruco.estimatePoseSingleMarkers(corners,markerLength, camera_matrix, dist_coeff)
        
        a=np.zeros((1,1,3))#creating a 3d np array 
        b=np.zeros((1,1,3))#creating a 3d np array
        
        
       
        
        if((ids is not None)):
                for i in range(len(ids)):
                
        
                 
                         a[0,0,0]=rvecs[i,0,0]#assigning values to the np array a
                         a[0,0,1]=rvecs[i,0,1]
                         a[0,0,2]=rvecs[i,0,2]

                         b[0,0,0]=tveci[i][0][0]#assigning values to the np array b
                         b[0,0,1]=tveci[i][0][1]
                         b[0,0,2]=tveci[i][0][2]
                 
                         aruco_list.append((ids[i][0],(int(corners[i][0][0][0]+corners[i][0][1][0]+corners[i][0][2][0]+corners[i][0][3][0])/4,int(corners[i][0][0][1]+corners[i][0][1][1]+
                         corners[i][0][2][1]+corners[i][0][3][1])/4),a,b))
                         a=np.zeros((1,1,3))#resetting the values in the array
                         b=np.zeros((1,1,3))
                 
        
                 
                 
               
                 
                

            
        return aruco_list








        
       
########################################################################


################# This is where the magic happens !! ###################
############### Complete these functions as  directed ##################
"""
Function Name : draw_background()
Input: img (numpy array)
Output: None
Purpose: Takes image as input and converts it into an OpenGL texture. That
         OpenGL texture is then set as background of the OpenGL scene
"""

def draw_background(img):
        
        
        bg_image = cv2.flip(img, 0)
        bg_image = Image.fromarray(bg_image)     
        ix = bg_image.size[0]
        iy = bg_image.size[1]
        bg_image = bg_image.tobytes('raw', 'BGRX', 0, -1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
        # create background texture
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0,GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        
        # draw background
        glBindTexture(GL_TEXTURE_2D, texture_background)
        glPushMatrix()
        glTranslatef(0.0,0.0,-9)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd( )
        
        
        glPopMatrix()
        glDeleteTextures(1)
        
        
        
        return None
         

"""
Function Name : init_object_texture()
Input: Image file path
Output: None
Purpose: Takes the filepath of a texture file as input and converts it into OpenGL
         texture. The texture is then applied to the next object rendered in the OpenGL
         scene.
"""
def init_object_texture(image_filepath):
        
         
         textureSurface = pygame.image.load(image_filepath)
         textureData = pygame.image.tostring(textureSurface,"RGBA",1)
         width = textureSurface.get_width()
         height = textureSurface.get_height()
         glEnable(GL_TEXTURE_2D)
         
         glBindTexture(GL_TEXTURE_2D, texture_object)
         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
         glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

'''
Function Name : overlay()
Input: img (numpy array), aruco_list, aruco_id, texture_file (filepath of texture file)
Output: None
Purpose: Receives the ArUco information as input and overlays the 3D Model of a teapot
         on the ArUco marker. That ArUco information is used to
         calculate the rotation matrix and subsequently the view matrix. Then that view matrix
         is loaded as current matrix and the 3D model is rendered.

         Parts of this code are already completed, you just need to fill in the blanks. You may
         however add your own code in this function.
'''         


def overlay(img, ar_list, ar_id, texture_file,obj):
        
        for x in ar_list:
                if ar_id == x[0]:
                        centre, rvec, tvecs = x[1], x[2], x[3]
               
        
        rmtx = cv2.Rodrigues(rvec)[0]
        print (tvecs[0][0][0],tvecs[0][0][1],tvecs[0][0][2])
        if(tvecs[0][0][0]<220 and tvecs[0][0][1]>-290):
        
                
       
                view_matrix = np.array([[    rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0][0]/520-1],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[0][0][1]/200.17],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],9],
                                    [0.0       ,0.0       ,0.0       ,1.0   ]])
        elif(tvecs[0][0][0]<220 and tvecs[0][0][1]<-290):
        
                
       
                view_matrix = np.array([[    rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0][0]/520-0.5],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[0][0][1]/200.17],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],9],
                                    [0.0       ,0.0       ,0.0       ,1.0   ]])

        elif(tvecs[0][0][0]>220 and tvecs[0][0][1]<-290):
        
                
       
                view_matrix = np.array([[    rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0][0]/520],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[0][0][1]/200.17+0.5],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],9],
                                    [0.0       ,0.0       ,0.0       ,1.0   ]])                
        
        else:
        
                 view_matrix = np.array([[    rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0][0][0]/520+1],
                                    [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[0][0][1]/200.17],
                                    [rmtx[2][0],rmtx[2][1],rmtx[2][2],9],
                                    [0.0       ,0.0       ,0.0       ,1.0   ]])
                 
                
         
               
                
      
                                    
                
                
        
        
        view_matrix = view_matrix * INVERSE_MATRIX
        view_matrix = np.transpose(view_matrix)
        init_object_texture(texture_file)
        
        glPushMatrix()
        glLoadMatrixd(view_matrix)
        if(obj=="water_pitcher"): 
                 glCallList(water_pitcher.gl_list)
        if(obj=="pebble_full") :
                 glCallList(pebble_full.gl_list)
        elif(obj=="pebble_half") :
                 glCallList(pebble_half.gl_list)
                
      
        glPopMatrix()
        glDeleteTextures(1)
 
      
        
        
        
        
        
    
 
        
      


########################################################################

if __name__ == "__main__":
        main()

        
