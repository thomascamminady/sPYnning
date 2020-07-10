# sPYnning
Source code for animating a spinning globe, consisting of hexagons. This can be used to generate images similar to the ones in [the original twitter tweet](https://twitter.com/cmmndy/status/1281187892845588480. Below are some images that are created in the `.ipynb`.


## Globe
```
nq = 2252
quadrature = getquadrature(nq)
# plot the earth 
colors  = color_land(quadrature)
myplot(colors,quadrature,"earth.png")
```
![Globe](https://github.com/camminady/sPYnning/blob/master/earth.png?raw=true)

