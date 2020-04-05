import particle
import particleList
import alg
import tkinter
import cv2
import numpy as np
import random
import time

# global variable
time_unit = 0
bearing_flag = True
outputIntensity = 5


def drawline(p1, p2, input, output):
    '''output trace of particles'''
    if p1[1] < input.shape[1] and p2[1] < input.shape[1]:
        if input[int(p1[0])][int(p1[1])] != 255 and input[int(p1[0])][int(p1[1])] != 255:
            cv2.line(output, (int(p1[1]),int(p1[0])), (int(p2[1]),int(p2[0])), (0,0,0), 1)


def newBearing(p, alpha, particle_list):
    '''smooth change bearing'''
    random_rate = 0.05
    global new_random
    global time_unit
    new_random = 0
    global bearing_flag
    if time_unit%10 == 0:
        if bearing_flag is False:
            new_random = random.random()

            bearing_flag = True

        elif bearing_flag is True:
            new_random = -random.random()

            bearing_flag = False

    new_random = new_random*7
    #make the random smoothly

    par = particle_list.start_node
    count = 0
    bearing_sum = 0
    while par is not None:
        bearing_sum += par.bearing
        count += 1
        par = par.nex
    
    bearing_average = bearing_sum/count
    if p.prev is None and p.nex is None:
        dis_prev = 1
        dis_nex = 1
    elif p.prev is None:
        dis_prev = alg.particle_space(p)
        dis_nex = alg.particle_space(p)
    else:
        dis_prev = alg.particle_space(p.prev)
        dis_nex = alg.particle_space(p)

    # keep distance
    if dis_nex == dis_prev:
        theta = None
        bearing_sig = 0
    elif  dis_nex < dis_prev:
        theta = (np.pi)-(np.pi/2)*(dis_nex/dis_prev)
        bearing_sig = -1/(1+theta*theta)
    else:
        theta = (np.pi/2)*(dis_nex/dis_prev)-(np.pi)
        bearing_sig = 1/(1+theta*theta)

    # let p smoothly close to previous particle
    if p.death is True:
        theta = (np.pi)-(np.pi/2)*(dis_nex/dis_prev)
        bearing_sig = -1/(1+theta*theta)

    bearing_new = (1-alpha)*p.bearing + alpha*(bearing_average + bearing_sig)/2

    if new_random != 0:
        # new bearing with random
        return bearing_new*(1-random_rate) + random_rate*new_random
    return bearing_new


def set_threshold(image, edge, particle_list, image_mean):

    # set new threshold for particles
    p = particle_list.start_node
    while p is not None:

        threshold_para = image[int(p.vector[0]), int(p.vector[1])]-image_mean

        p.threshold = outputIntensity + (threshold_para/255)*outputIntensity

        # minimize edge threshold
        if edge[int(p.vector[0]), int(p.vector[1])] == 255:
            p.threshold = 2

        p = p.nex


def update_BP(p, particle_list, input, output):

    '''update bearing and postion'''
    drawline(p.vector, (p.vector[0] + np.sin(p.bearing), p.vector[1] + np.cos(p.bearing)), input, output)
    p.vector = (p.vector[0] + np.sin(p.bearing), p.vector[1] + np.cos(p.bearing))

    p.bearing = newBearing(p, 0.1, particle_list)


def update(particle_list, image, edge, tb):

    '''main update for image processing'''
    canvas_height = image.shape[0]
    canvas_width = image.shape[1]
    image_mean = image.mean()
    output = np.empty(shape=(image.shape[0], image.shape[1]))
    output.fill(255)
    while True:
        p = particle_list.start_node
        particle_list.start_node.vector = 1, particle_list.start_node.vector[1]
        while p is not None:
            # out of bound
            if p.vector[0] >= canvas_height-1 or p.vector[1] >= canvas_width-1 or p.vector[0] < 0 or p.vector[1] < 0:
                particle_list.delete(p)
                if particle_list.start_node is None:
                    return output
            if p.nex is None:
                p.vector = canvas_height-1, p.vector[1]
            update_BP(p, particle_list, image, output)
            '''set all particles in one line'''

            if p.nex != None:
                if p.vector[1] > p.nex.vector[1]:
                    p = p.nex
            else:
                p = p.nex

        set_threshold(image, edge, particle_list, image_mean)

        # simulation
        alg.simulation(particle_list, tb/4)

        if particle_list.start_node is None:
            return output
        global time_unit 
        time_unit += 1
        print(time_unit)



