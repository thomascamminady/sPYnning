from numpy import loadtxt, degrees, arcsin, arctan2, sort, unique, ones, zeros_like, array
from mpl_toolkits.basemap import Basemap
import reverse_geocoder as rg
import randomcolor

def domino(lol):
    # Takes a list (length n) of lists (length 2)
    # and returns a list of indices order,
    # such that lol[order[i]] and lol[order[i+1]]
    # have at least one element in common.
    # If that is not possible, multiple
    # domino chains will be created.
    # This works in a greedy way.
    
    n = len(lol)
    order = [0] # Greedy 
    link = lol[0][-1]
    links = [lol[0][0],lol[0][1]]
    while len(order)<n:
        for i in [j for j in range(n) if not j in order]:
            if link in lol[i]: # They connect
                order.append(i) # Save the id of the "stone"
                link = lol[i][0] if not(lol[i][0]==link) else lol[i][1] # The new link is the other element 
                links.append(link)
                break
    return order,links[:-1]


def getpatches(color,quadrature):
    xyz,neighbours,triangles = quadrature["xyz"], quadrature["neighbours"], quadrature["triangles"]
    nq = len(color)
    patches = []
    for center in range(nq):
        lol = [] # list of lists
        for i in neighbours[center,:]:
            if i>-1:
                lol.append(list(sort(triangles[i,triangles[i,:] != center])))
        order,links = domino(lol)

        neighx = [xyz[j,0] for j in links]
        neighy = [xyz[j,1] for j in links]
        neighz = [xyz[j,2] for j in links]

        # Get the actual hexagon that surrounds a center point
        x = []
        y = []
        z = []
        for i in range(len(order)):
            x.append((xyz[center,0]+neighx[i]) / 2)
            x.append((xyz[center,0]+neighx[i]+neighx[(i+1)%len(order)])/3)

            y.append((xyz[center,1]+neighy[i]) / 2)
            y.append((xyz[center,1]+neighy[i]+neighy[(i+1)%len(order)])/3)

            z.append((xyz[center,2]+neighz[i]) / 2)
            z.append((xyz[center,2]+neighz[i]+neighz[(i+1)%len(order)])/3)

        verts = [list(zip(x,y,z))]
        patches.append(verts[0])
    return patches


def getquadrature(nq):

    quadrature = {}
    quadrature["nq"] = nq
    quadrature["xyz"] = loadtxt(f"quadrature/{nq}/points.txt")
    quadrature["weights"] = loadtxt(f"quadrature/{nq}/weights.txt")
    quadrature["neighbours"] = loadtxt(f"quadrature/{nq}/neighbours.txt",dtype=int)-1 # julia starts at 1
    quadrature["triangles"] = loadtxt(f"quadrature/{nq}/triangles.txt",dtype=int)-1 # julia starts at 1 
    
    # Also convert to latitute, longitude
    quadrature["lat"] = degrees(arcsin(quadrature["xyz"][:,2]/1))
    quadrature["lon"] = degrees(arctan2(quadrature["xyz"][:,1], quadrature["xyz"][:,0]))
    
    # Compute connectivity between nodes
    connection = -100*ones((quadrature["nq"],6),dtype=int)
    for qp in range(quadrature["nq"]):
        attachedtriangles = quadrature["neighbours"][qp]
        attachedtriangles = attachedtriangles[attachedtriangles>-1] # drop 
        lol = []
        for at in attachedtriangles:
            tmp = quadrature["triangles"][at]
            tmp = tmp[tmp != qp ]
            lol.append(list(tmp))

        _,x =  domino(lol)
        connection[qp,:len(x)] = x
        
    quadrature["connection"] = connection

    return quadrature


def get_land(quadrature):
    bm = Basemap()  
    island = []
    for i,(ypt, xpt) in enumerate(zip(quadrature["lat"],quadrature["lon"])):
        land = (bm.is_land(xpt,ypt))  
        island.append(land)
    return array(island)
    
def color_land(quadrature):
    island = get_land(quadrature)
    colors = ["tab:green" if land else "tab:blue" for land in island]
    return colors

def color_country(quadrature):
    # uses reverse_geocoder
    results = rg.search([(la,lo) for la,lo in zip(quadrature["lat"],quadrature["lon"])]) # default mode = 2
    countries = []
    for i in range(len(results)):
        c = results[i]["cc"]
        countries.append(c)
    nunique = len(unique(countries))
    
    raco = randomcolor.RandomColor()
    randomcolors = raco.generate(luminosity="dark", count=nunique) # options: https://github.com/kevinwuhoo/randomcolor-py
    colordict = dict(zip(unique(countries),randomcolors))
    colorland = color_land(quadrature) # so we can color the ocean also in "tab:blue"
    colorcountries = [colordict[country] if colorland[i]!="tab:blue" else "tab:blue" for i,country in enumerate(countries) ]
    return colorcountries



def applyupdate(quadrature,rule,states):
    nextstate = zeros_like(states)
    
    for i,(state, neighbours) in enumerate(zip(states,quadrature["connection"])):
        idx = neighbours[neighbours>-1]
        stateneighbours = states[idx]
        nextstate[i] = rule(state,stateneighbours)
    return nextstate