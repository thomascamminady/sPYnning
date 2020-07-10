# sPYnning
Source code for animating a spinning globe, consisting of hexagons. This can be used to generate images similar to the ones in [the original twitter tweet](https://twitter.com/cmmndy/status/1281187892845588480). Below are some images that are created in the Jupyter notebook.

For more images and GIFs, check out https://www.camminady.org/spinningglobe

## How To?

### Locally
Clone the repository and run through the cells of `visworld.ipynb` found [here](https://github.com/camminady/sPYnning/blob/master/visworld.ipynb).

If you encounter an issue with `mpl_toolkits` (I did), this [link](https://stackoverflow.com/questions/37661119/python-mpl-toolkits-installation-issue) might  help. To deal with that issue, the Google Colab version additionally runs
```
sudo apt-get install libgeos-dev
sudo pip3 install https://github.com/matplotlib/basemap/archive/master.zip
```

### Google Colab
I ported the Jupyter notebook to Google Colab. In the process, I had move the `helpers.py` file in the notebook.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/camminady/sPYnning/blob/master/visworld_colab.ipynb)

Note that the Colab notebook is already outdated and contains only the initla animations, no diffusion or Game of Life.



## Globe
```
nq = 2252
quadrature = getquadrature(nq)
# plot the earth 
colors  = color_land(quadrature)
myplot(colors,quadrature,"earth.png")
```
![Globe](https://github.com/camminady/sPYnning/blob/master/earth.png?raw=true)


## Country colored
```
# higher resolution to plot countries
nq = 7292
quadrature = getquadrature(nq)
colors  = color_country(quadrature)
myplot(colors,quadrature,"earth_country.png")
```
![Globe](https://github.com/camminady/sPYnning/blob/master/earth_country.png?raw=true)


## Animated GIF
```
nq = 7292
quadrature = getquadrature(nq)
colors  = color_land(quadrature)

frames = []
nframes = 20 # the more, the slower 
for i,angle in enumerate(np.linspace(0,360,nframes)[:-1]):
    print(i,end=",")
    frames.append(myplot(colors,quadrature,"tmp.png",frameid = i, angle1=30,angle2=angle))

gif.save(frames,"spinning_earth.gif")
```
![Globe](https://github.com/camminady/sPYnning/blob/master/spinning_earth.gif?raw=true)


## Diffusion equation (only faked, not for scientific purposes)
We need an update rule for each time step.
```python
def diffusion(c,nextc,gamma = 0.2):
    # Not really spherical diffusion
    # because I ignore the cell size,
    # but an approximation.
    return c+gamma*(np.sum(nextc) -len(nextc)*c)
```   
Then we can update the states in every iteration
```python
# pick the number of cells on the globe from this list
# [92, 492, 1212, 2252, 3612, 5292, 7292, 9612, 12252, 15212]
nq = 9612
quadrature = getquadrature(nq)

# +1 or -1 if center of hexagon is land or not 
states = np.array([0.7 if l else -1.0 for l in get_land(quadrature)])
# if there were an eleveation profile of the earth, 
# I could insert that instead of states

frames = []   # list of frames to append to 
nframes = 200 # number of frames 
frequency = 1 # frequency with which to update the states

# make camera move around the globe and up and down
angles1 = 0.2*np.degrees( np.sin(np.linspace(0,5*2*np.pi,nframes+1)[:-1]))
angles2 = np.linspace(0,3*360,nframes+1)[:-1]

# specify the update rule
updaterule = diffusion

for i,(angle1,angle2) in enumerate(zip(angles1,angles2)):
    
    # Map from states to color 
    cmap = matplotlib.cm.get_cmap('terrain') 
    colors = [cmap(s) for s in states]

    frames.append(myplot(colors,quadrature,f"PNG/{i}.png",i,angle1=angle1,angle2=angle2))
    
    # update states according to rule 
    if i%frequency == 0:
        states = applyupdate(quadrature,updaterule,states)
     
    print(i+1,end= "," if i<nframes-1 else ". Done!")
gif.save(frames, "diffusion.gif", duration = 100)
```
![Diffusion](https://github.com/camminady/sPYnning/blob/master/diffusion.gif?raw=true)




## Game of Life
We gain need an update rule. A cell's state is updated based upon the adjacent neighbours. Here you can be creative.
```python
def gameoflife(c,nextc):
    # update the cell c based upon the neighbours nextc
    # c is true => cell alive
    # c is fale => cell dead 
    
    n = len(nextc) # is mostly 6 but for some points 5 
    nalive = sum(nextc)
    if not(c) and nalive in [1,2]:
        return True
    
    if c  and nalive in [3,4,5,6]:
        return False

    # Else, nothing changed
    return c
```
Then create the animation.
```python
# pick the number of cells on the globe from this list
# [92, 492, 1212, 2252, 3612, 5292, 7292, 9612, 12252, 15212]
nq = 5292
quadrature = getquadrature(nq)

# True or False if center of hexagon is land or not 
states = np.random.rand(nq)<0.01

frames = []   # list of frames to append to 
nframes = 100 # number of frames 
frequency = 5 # frequency with which to update the states

# make camera move around the globe and up and down
angles1 = np.degrees( np.sin(np.linspace(0,2*np.pi,nframes+1)[:-1]))
angles2 = 30+0*np.linspace(0,3*360,nframes+1)[:-1]

# specify the update rule
updaterule = gameoflife

for i,(angle1,angle2) in enumerate(zip(angles1,angles2)):
    
    # Map from states to color 
    colors = ["tab:green" if s else "k" for s in states]

    frames.append(myplot(colors,quadrature,f"PNG/{i}.png",i,angle1=angle1,angle2=angle2))
    
    # update states according to rule 
    if i%frequency == 0:
        states = applyupdate(quadrature,updaterule,states)
     
    print(i+1,end= "," if i<nframes-1 else ". Done!")
gif.save(frames, "gol.gif", duration = 100)
```
![Game of Life](https://github.com/camminady/sPYnning/blob/master/gol.gif?raw=true)

