import numpy as np
from mpl_toolkits.basemap import Basemap
import reverse_geocoder as rg
import randomcolor
import json
import requests

def getlands(quadrature):
    bm = Basemap()  
    island = []
    for i,(ypt, xpt) in enumerate(zip(quadrature["lat"],quadrature["lon"])):
        land = (bm.is_land(xpt,ypt))  
        island.append(land)
    return np.array(island)
    
def colorland(state):
    return "tab:green" if state else "tab:blue"

def getcountries(quadrature):
    results = rg.search([(x,y) for x,y in zip(quadrature["lat"],quadrature["lon"])]) # default mode = 2
    countries = []
    for i in range(len(results)):
        c = results[i]["cc"]
        countries.append(c)
    return np.array(countries)


def getcountriescolors(quadrature):
    # uses reverse_geocoder
    countries = getcountries(quadrature)
    nunique = len(np.unique(countries))
    landmass = getlands(quadrature)
    
    raco = randomcolor.RandomColor()
    randomcolors = raco.generate(luminosity="dark", count=nunique) # options: https://github.com/kevinwuhoo/randomcolor-py
    colordict = dict(zip(np.unique(countries),randomcolors))
    
    countriescolors = [colordict[country] if landmass[i] else "tab:blue" for i,country in enumerate(countries) ]
    return countriescolors

def applyupdate(quadrature,rule,states):
    nextstate = np.zeros_like(states)
    for i in range(quadrature["nq"]):
        nextstate[i] = rule(i,states,quadrature)
    return nextstate



def applyupdatetwostates(quadrature,rule,states1,states2):
    nextstate1 = np.zeros_like(states1) 
    nextstate2 = np.zeros_like(states1)
    
    for i,(state1,state2, neighbours) in enumerate(zip(states1,states2,quadrature["connection"])):
        idx = neighbours[neighbours>-1]
        stateneighbours1 = states1[idx]
        stateneighbours2 = states2[idx]
        
        nextstate1[i], nextstate2[i] = rule(state1,stateneighbours1,state2,stateneighbours2)
    return nextstate1,nextstate2



def diffusion(cellid,states,quadrature):
    neighbours = quadrature["connection"][cellid]
    neighbours = neighbours[neighbours>-1]
    
    areas =[quadrature["areas"][neighbour] for neighbour in neighbours]
    area = quadrature["areas"][cellid]
    
    state = states[cellid]
    neighbourstates = [states[neighbour] for neighbour in neighbours]
    
    gamma = 0.1
    return state + (np.dot(neighbourstates,areas)- sum(areas)*state)


def identity(cellid,states,quadrature):
    return states[cellid]