from corneal import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

#airfoil = naca_airfoil("0006", 20) # NACA 0012 airfoil with 20 points per side
airfoil = naca_airfoil("0012", 50) 
#airfoil = TransformedBody(airfoil, displacement=(-0.75, 0))
#airfoil = joukowski_foil(-.1,.1,.5,100)
#airfoil = van_de_vooren_foil(0.5, 0.1, 3)
#airfoil = karman_trefftz_foil(-.1,.1,1,10,32)
#airfoil = flat_plate(20)
#airfoil = cylinder(1.0,50)

#pts = airfoil.get_points()
#plt.plot(pts[:,0],pts[:,1])
#plt.axis('equal')
#plt.show()

freq = 0.3 * 2*np.pi
airfoil = Pitching(airfoil, 20, freq, phase=90)
airfoil = Heaving(airfoil, (0,0.2), freq, phase=0)

Uinfty = (1,0)
bound = BoundVortices(airfoil, Uinfty)

dt = 0.05
flow = RungeKutta4(dt, Uinfty, bound)

fig, ax = plt.subplots()
ax.axis('equal')
ax.axis([-3,5,-2,2])
#ax.axis([-4,5,-3,3])
ax.grid(True)
q = airfoil.get_points()
line, = ax.plot(q[:,0], q[:,1], '-k')
maxval = dt
pts = ax.scatter(0, 0, c=0,
                 #cmap='bwr', vmin=-maxval, vmax=maxval, edgecolors='none')
		 cmap='RdYlGn', vmin=-maxval, vmax=maxval, edgecolors='none')

def gen_points():
    flow.initialize()
    num_steps = 200
    for i in range(num_steps):
        flow.advance()
        yield airfoil.get_points(), flow.wake.positions, flow.wake.strengths

def redraw(data):
    q, xvort, gam = data
    line.set_data(q[:,0], q[:,1])
    pts.set_offsets(np.array([xvort[:,0], xvort[:,1]]).T)
    pts.set_array(gam)

movie = animation.FuncAnimation(fig, redraw, gen_points, interval=100)
#movie.save('basic_animation.mp4', writer=writer)
#fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()
