# sPYnning
Source code for animating a spinning globe, consisting of hexagons. This can be used to generate images similar to the ones in [the original twitter tweet](https://twitter.com/cmmndy/status/1281187892845588480). Below are some images that are created in the Jupyter notebook.

## How To?

### Locally
Clone the repository and run through the cells of `visworld.ipynb` found [here](https://github.com/camminady/sPYnning/blob/master/visworld.ipynb).

If you encounter an issue with `mpl_toolkits` (I did), this [link](https://stackoverflow.com/questions/37661119/python-mpl-toolkits-installation-issue) might  help. Otherwise, try the Google Colab version.

## Google Colab
I ported the Jupyter notebook to Google Colab. In the process, I had move the `helpers.py` file in the notebook.


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
    frames.append(myplot(colors,quadrature,"tmp.png",angle=angle))

gif.save(frames,"spinning_earth.gif")
```
![Globe](https://github.com/camminady/sPYnning/blob/master/spinning_earth.gif?raw=true)
