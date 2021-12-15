# INDEX
- [ABOUT](#ABOUT)
- [HOWTOUSE](#HOWTOUSE)
- [ENVIRONMENT](#ABOUT)
- [INSTALATION](#INSTALATION)

# ABOUT
- Track cyclone center position.
- This project is created as [爆弾低気圧データベース](http://fujin.geo.kyushu-u.ac.jp/meteorol_bomb/algorithm/index.php) and [pytrack](https://github.com/tenomoto/pytrack)
## Algorithm

1. Find local minima by scipy.ndimage.filters.minimum_filter() assuming a cyclic boundary conditon in longitude.
2. Find the grid of the minimum closest to the initial guess in geodesic distance.
3. Generate nine point stencil with the minimum on grid at the centre
4. Interpolate for the minimum in-between grid using biquadratic interpolation. If interpolation fails use the minimum on grid



# HOWTOUSE
