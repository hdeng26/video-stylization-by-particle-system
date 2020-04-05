'''main algorithms'''
import cv2
import random
import numpy as np
import particle
import particleList

timestep = 0 #timestep need change later

def simulation(particle_list, beta):
    '''main simulation algorithm'''

    '''update next movement of patricles'''
    count = 0
    p = particle_list.start_node
    while p is not None:
        '''update spacing threshold'''

        space = particle_space(p)

        if p.threshold > space:
            p.threshold -= beta
        elif p.threshold < space:
            p.threshold += beta
        if p.nex is not None:
            threshold_base = (p.threshold + p.nex.threshold)/2
        elif p.prev is not None:
            threshold_base = (p.threshold + p.prev.threshold)/2
        else:
            threshold_base = p.threshold
        threshold_birth = threshold_base*1.5
        threshold_death = threshold_base*0.5
        count += 1

        if space >= threshold_death and p.birth == True:
            p.birth = False

        if space > threshold_birth:
            '''birth new particle'''
            if p.nex is not None:
                birthFromCur(particle_list, p)
                p = p.nex

        elif space < threshold_death and p.birth == False:
            '''kill p.next'''
            if p.nex is not None:
                killNext(particle_list, p)
        p = p.nex
    # clean touched particles
    coll_detect(particle_list)


def particle_space(p):
    '''space between a particle and next one'''

    if p.nex is not None:
        return abs(p.nex.vector[0] - p.vector[0])

    elif p.prev is not None:
        return abs(p.vector[0] - p.prev.vector[0])

    else:
        return 1


def killNext(particle_list, p):
    #kill next particle in the list
    if p.nex is None:
        return
    p.nex.death = True


def birthFromCur(particle_list, p):
    # birth new particle
    newBirth = particle.particle(prev=None, nex=None, vector=(((p.vector[0]+1)), p.vector[1]), bearing=0, threshold=p.threshold, direction=0)
    newBirth.birth = True
    if p.nex is not None:
        particle_list.insert_after(p, newBirth)
    else:
        particle_list.insert_after(p, newBirth)


def coll_detect(plist):
    '''delete all other particle at same location'''

    temp = plist.start_node
    while temp is not None:
        if temp.nex is None:
            return
        if temp.nex.vector[0] <= temp.vector[0]+1 and temp.nex.birth == False:
            plist.delete(temp.nex)

        temp = temp.nex


def countSize(plist):
    # count the size of the list
    p = plist.start_node
    count = 0
    while p.nex is not None:
        count = count + 1
        p = p.nex

    print("COUNTING", plist.size, count)