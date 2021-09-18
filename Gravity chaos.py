M1={'m':1,'r':.1,'x':-.5,'y':-.5/3**.5,'c':(228/256,98/256,250/256)} #pink
M2={'m':1,'r':.1,'x':0,'y':1/3**.5,'c':(49/256,43/256,245/256)} #indigo
M3={'m':1,'r':.1,'x':.5,'y':-.5/3**.5,'c':(73/256,195/256,1)} #blue
M4={'m':1,'r':.2,'x':1.25,'y':1,'c':(.5,1,.5)} #lime
bodies=[M1,M2,M3]

#TODO: try these optimizations: dt(g), skipping elliptical paths

import canvas,time

width=200
canvas.set_size(width,width)

G= 1
dt= 0.001
maxtime=100
corner=(-7,-7)
side=10

t0=time.time()
for i in range(width):
	for j in range(width):
		u,v=i/width*side+corner[0],j/width*side+corner[1]
		x,y=2.11, 2.67#u,v
		#investigate these crazy coordinates: (-0.7125, 0.375)
		v_x,v_y=0,0
		t=0
		
		def dist(A):return ((x-A['x'])**2+(y-A['y'])**2)**.5
		
		canvas.set_fill_color(1,0,0)
		for A in bodies:canvas.fill_pixel((A['x']-corner[0])*width/side,(A['y']-corner[1])*width/side)
		x_com=sum([A['x']*A['m'] for A in bodies])/sum([A['m'] for A in bodies])
		y_com=sum([A['y']*A['m'] for A in bodies])/sum([A['m'] for A in bodies])
		canvas.set_fill_color(0,1,0)
		canvas.fill_pixel((x_com-corner[0])*width/side,(y_com-corner[1])*width/side)
		
		if [1 for A in bodies if dist(A)<=A['r']]:
			canvas.set_fill_color(1,1,1)
		else:
			escaped=False
			while t<maxtime and not escaped and not [1 for A in bodies if dist(A)<=A['r']]:
				dx= v_x*dt
				dy= v_y*dt
				dv_x= -G*sum([A['m']*(x-A['x'])/dist(A)**3 for A in bodies])*dt
				dv_y= -G*sum([A['m']*(y-A['y'])/dist(A)**3 for A in bodies])*dt
				
				x+=dx
				y+=dy
				v_x+=dv_x
				v_y+=dv_y
				t+=dt
				
				if v_x**2+v_y**2 >= 2*G*sum([A['m']/dist(A) for A in bodies]):
					escaped=False not in [v_x*(A['x']-x)+v_y*(A['y']-y)<=0 for A in bodies]
				
				canvas.fill_pixel((x-corner[0])*width/side,(y-corner[1])*width/side)
			
			if t>=maxtime or escaped:
				canvas.set_fill_color(0,0,0)
			else:
				color_id=[dist(A)<=A['r'] for A in bodies].index(True)
				colors=bodies[color_id]['c']
				canvas.set_fill_color(colors[0],colors[1],colors[2])
		break
		canvas.fill_pixel(i,j)
	break

canvas.end_updates()
#print(time.time()-t0)
#canvas.save_png('Neat colors.png')
