"""
Author: Noeloikeau Charlot 2023

License: Creative Commons ► Attribution 3.0 Unported ► CC BY 3.0
https://creativecommons.org/licenses/...
"You are free to use, remix, transform, and build upon the material
for any purpose, even commercially. You must give appropriate credit."
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation,TimedAnimation,PillowWriter,FFMpegWriter
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm, ListedColormap
from numba import njit

#used for rescaling fractals
feigenbaum_constant = 4.669201609

#used for generating fractals
@njit
def weierstrass(b=5,N=100,T=10000,alpha=np.log(2),beta=-1,kappa=1,periods=1,phi=0):
    """
    广义韦尔斯特拉斯函数（或超几何/傅立叶级数）。
    复平面上T个时间点中N个向量的系列，
    可视化为箭头，尾部相连并随着半径减小和频率增加而旋转。
    b是基数（对称点/单位根）。
    beta是角频率是否切换符号（-1）。
    alpha和kappa调节半径。
    返回两个TxN矩阵：向量Z及其部分和W。
    """
    W = np.zeros((T,N),dtype=np.complex_) #partial sums
    Z = np.zeros((T,N),dtype=np.complex_) #vectors
    alphaB = float(alpha)*float(b)
    betaB = float(beta)*float(b)
    lambdaT = periods*2j*np.pi/T
    for t in range(T):
        for n in range(N):
            Z[t,n] = ((kappa*n+1)*alphaB**(-n))*np.exp(phi+t*lambdaT*betaB**n)
            W[t,n] = (Z[t,:n+1]).sum()
    return W,Z

#used for colormaps in plotting
def normalize_colors(cmap,npoints,bounds):
    if isinstance(cmap,str):
        colors = [cmap]*npoints
    else:
        t = np.linspace(bounds[0],bounds[1],npoints)
        colors = cmap(t)
    return colors

#used to color line segments individually
def color_line(x,y,colors,ax,lw):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, colors=colors[1:-1])
    lc.set_linewidth(lw)
    line = ax.add_collection(lc)
    return line

#package the fractal calculation with a plotting function
class Fractal:
    def __init__(self,
                 map = weierstrass,
                 save = False,
                 rescale = lambda n: feigenbaum_constant**n,
                 **kwargs
                 ):
        self.map = map
        self.save = save
        self.rescale = rescale
        self.evals = []
        self.keys = set(kwargs.keys())
        self.__call__(**kwargs)
        self.L = 1.05*max(self.W.max(),abs(self.W.min()))

    #store variables and parameters as instance attributes with each call
    def __call__(self,**kwargs):
        self.__dict__.update(**kwargs)
        self.W,self.Z = self.map(**{k:v for k,v in self.__dict__.items() if k in self.keys})
        self.x,self.y = self.W[:,-1].real, self.W[:,-1].imag
        if self.save:
            self.evals+=[(kwargs,self.W,self.Z)]

    #visualize the fractal modes over various times and scales
    def plot(self,
             modes = 0, #optional orbits for each harmonic number/partial sum
             times = [None,None], #time range to plot over, defaults to 0,T
             time_offset = 0, #offset indices, for animating at set time
             scales = [0], #number of fractal rescalings to plot simultaneously
             plot_points = True, #plot the orbiting bodies as points
             plot_arrows = True, #plot the arrows constructing the epicycles
             mode_cmap = plt.cm.winter, #color by harmonic number
             time_cmap = plt.cm.cool, #color by time
             mode_cmap_bounds = (0,1), #range in cmap function
             time_cmap_bounds = (0,1),
             figsize = (8,8),
             xlim = [None,None],
             ylim = [None,None],
             autoscale = False,
             axis_off = True,
             facecolor = 'black',
             lw = 0.1,
             dpi = None,
             fname = None,
             fig = None,
             ax = None,
             arrowcolor = None,
             show = True,
             skip = 1,
             tight_layout = False,
             markersize = 1,
             override_time_color = False,
             arrow_lw = None,
             arrow_alpha = 0.75,
             point_at_origin = False,
             mode_lw = None,
             mode_alpha=1,
             alpha = None,
             **kwargs
             ):
        #default colors and widths
        if mode_lw is None:
            mode_lw = lw
        if arrow_lw is None:
            arrow_lw = lw/2
        if autoscale:
            figsize = None
        if facecolor=='white':
            anticolor='black'
        else:
            anticolor='white'
        if arrowcolor is None:
            arrowcolor = anticolor
        #update if any new kwargs
        self.__call__(**kwargs)
        #artists, to be passed to animation
        if (fig is None) or (ax is None):
            fig,ax = plt.subplots(figsize=figsize,facecolor=facecolor)
        ax.set_facecolor(facecolor)
        artists = []
        #color by harmonic
        if isinstance(modes,int):
            modes = np.arange(modes)
        mode_colors = normalize_colors(mode_cmap,len(modes),mode_cmap_bounds)
        #color by time (last harmonic is the true fractal curve)
        if times[0] is None:
            times[0] = 0
        if times[1] is None:
            times[1] = self.T
        t0,t1 = times
        T = t1-t0
        time_colors = normalize_colors(time_cmap,T,time_cmap_bounds)
        #draw fractal at given scale via scaling function
        for n in scales:
            #rescale data
            scale = self.rescale(n)
            tn00 = (t0+time_offset*n)
            tn11 = (t1+time_offset*n)
            tn0 = min(tn00,tn11)
            tn1 = max(tn00,tn11)
            msize = markersize*scale
            x,y = scale*self.x[::skip][tn0:tn1], scale*self.y[::skip][tn0:tn1]
            W,Z = scale*self.W[::skip][tn0:tn1], scale*self.Z[::skip][tn0:tn1]
            #plot origin
            if plot_arrows:
                artists+=[ax.arrow(0, 0, Z[-1,0].real, Z[-1,0].imag, color=arrowcolor,
                                   lw=arrow_lw, ls='--',alpha=arrow_alpha)]
            if point_at_origin:
                artists+=[ax.plot(0, 0, color=arrowcolor,
                                        linewidth=lw, marker='*',
                                        markersize=markersize*self.rescale(n-2))[0]]
            #plot harmonics
            for i in modes:
                mcolor=mode_colors[i]
                if i==-1: #if it's the last harmonic passed explicitly, don't color by time
                    if override_time_color:
                        mcolor=anticolor
                    mlw = lw
                    malpha = alpha
                else: #lower-order harmonics
                    mlw = mode_lw
                    malpha = mode_alpha
                #orbit
                artists += [ax.plot(W[:,i].real, W[:,i].imag,
                                    color=mcolor, linewidth=mlw,alpha=malpha)[0]]
                #position
                if plot_points:
                    artists += [ax.plot(W[-1,i].real, W[-1,i].imag, color=mode_colors[i],
                                        linewidth=lw, marker='.', markersize=msize)[0]]
                #series
                if plot_arrows:
                    artists+=[ax.arrow(Z[-1,:i].real.sum(), Z[-1,:i].imag.sum(),
                                       Z[-1,i].real, Z[-1,i].imag, color=arrowcolor,
                                       lw=arrow_lw, ls='--',alpha=arrow_alpha)]

            #by default, color last mode by time as collection of ordered line segments
            if -1 not in modes:
                artists += [color_line(x,y,time_colors,ax,lw)]

        #artists and bounds
        if axis_off:
            plt.axis('off')
        if xlim[0] is None:
            xlim[0] = x.min()
        if xlim[1] is None:
            xlim[1] = x.max()
        if ylim[0] is None:
            ylim[0] = y.min()
        if ylim[1] is None:
            ylim[1] = y.max()
        if not autoscale:
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
            plt.gcf().set_size_inches(figsize)
        if tight_layout:
            fig.tight_layout()
        if fname:
            plt.savefig(fname, dpi=dpi)
        res = list(np.ravel(artists))
        if show:
            plt.show()
        else:
            return res
F = Fractal(b=5,N=100,T=100000,alpha=np.log(2),beta=-1,kappa=1,periods=2,phi=2j*np.pi/4)

figsize=(16,9)
facecolor='white'

time_cmap=plt.cm.winter
time_cmap_bounds=(0,0.4)#(0.,0.35)

#mode_cmap = plt.cm.tab20c
mode_cmap=plt.cm.winter
mode_cmap_bounds = (0.13,0.33)

bounds = np.array([-1.05*F.L,1.05*F.L])

fig,ax = plt.subplots(figsize=figsize,facecolor=facecolor)

lw = 0.11#0.11
mode_lw = 2*lw#0.15#0.17
mode_alpha = 0.5#0.8
arrowcolor='cyan'
arrow_lw = 4*lw/3
markersize=2
dpi = 600
point_at_origin = False

F.plot(modes=[0,1,2,3,4,5,-1],
       time_cmap='white',
       time_cmap_bounds = time_cmap_bounds,
       lw=lw,mode_cmap = mode_cmap, mode_cmap_bounds=mode_cmap_bounds,figsize=figsize,
       dpi=dpi,
       fname=None,
       #autscale = True,
       #tight_layout = True,
       xlim=bounds*16/9,
       ylim=bounds,
       facecolor=facecolor,axis_off=True,
       scales=[-2,-1,0,1],
       fig=fig,ax=ax,
       markersize=markersize,
       #times = [0,F.T],
       arrowcolor=arrowcolor,
       arrow_lw = arrow_lw,
       override_time_color=False,
       point_at_origin=point_at_origin,
       mode_lw = mode_lw,
       mode_alpha = mode_alpha,
       plot_points=True,plot_arrows=True)
plt.clf()
"""
figsize=(16,9)
facecolor='black'

duration = 30
frames = 60#1800
fps = 60#frames/duration
dpi = 300
interval = 1

#time_cmap=plt.cm.jet
#time_cmap_bounds=(0,1)

#mode_cmap = plt.cm.tab20c
#mode_cmap_bounds = (0.30,0.60)
#mode_cmap=plt.cm.jet
#mode_cmap_bounds = (0.1,0.33)


plot_zoom = dict(
    modes=[0,1,2,3,4,5,-1],
    time_cmap=time_cmap,
    time_cmap_bounds = time_cmap_bounds,
    lw=lw,
    mode_lw=mode_lw,
    arrow_lw=arrow_lw,
    arrowcolor=arrowcolor,
    markersize=markersize,
    mode_cmap = mode_cmap, mode_cmap_bounds=mode_cmap_bounds,figsize=figsize, dpi=dpi,
    fname=None,
    tight_layout = True,
    facecolor=facecolor,axis_off=True,
    scales=[-2,-1,0,1],
    show=False,
    point_at_origin=point_at_origin,
    override_time_color=False,
    plot_points=True,
)
animation_zoom = dict(
    interval=interval,
    blit=False,
    frames=frames,
    repeat=False,
    cache_frame_data = False,
    save_count=frames
)
save_zoom = dict(
    filename="zoomtest.mp4",
    dpi=dpi,
    writer=FFMpegWriter(fps=fps),
)

fig,ax = plt.subplots(figsize=figsize,facecolor=facecolor)
bounds_rule = lambda i: F.L*(1.5-(i+1)/frames)
arrows_rule = lambda i: True if i<frames//2 else False
def animate(i):
    ax.clear()
    bound = bounds_rule(i)
    bounds = np.array([-bound, bound])
    artists=F.plot(xlim=bounds*figsize[0]/figsize[1],
                   ylim=bounds,
                   plot_arrows=arrows_rule(i),
                   times=[0,(F.T)*i//frames+1],
                   fig=fig,ax=ax,**plot_zoom)
    return artists
ani = FuncAnimation(fig, animate, **animation_zoom)
 ani.save(**save_zoom)"""