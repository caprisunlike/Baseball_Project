Web VPython 3.2
import random as rand

def on_keydown(event):
    global bat
    if event.key == "left" and bat.pos.z > -1:
        bat.pos.z += 0.05
    elif event.key == "right" and bat.pos.z < 1:
        bat.pos.z -= 0.05
    elif event.key == "up" and bat.pos.y < 2:
        bat.pos.y += 0.05
    elif event.key == "down" and bat.pos.y > 0:
        bat.pos.y -= 0.05

def collision(obj1, obj2, e):
    c = obj2.pos - obj1.pos
    c_hat = norm(c)
    dist = mag(c)
    
    if dot(obj1.v-obj2.v, c_hat) < 0:
        return False
        
    v1_c = dot(obj1.v,c_hat)*c_hat
    v1_p = obj1.v - v1_c
    v2_c = dot(obj2.v,c_hat)*c_hat
    v2_p = obj2.v - v2_c
    tot_m = obj1.m + obj2.m
    
    if dist < obj1.radius + obj2.radius:
        v1 = ((obj1.m-e*obj2.m)*v1_c + (1+e)*obj2.m*v2_c) / tot_m
        v2 = ((obj2.m-e*obj1.m)*v2_c + (1+e)*obj1.m*v1_c) / tot_m
        obj1.v = v1 + v1_p
        obj2.v = v2 + v2_p
        return True
    else:
        return False

def batting(bat):
    M = bat.m
    Lrod = 1
    R = 0.03
    Laxel = 4*R
    I = (1/12)*M*Lrod**2 + (1/4)*M*R**2
    L = vec(0,0,0)

    #bat = cylinder(pos = vec(18.44,0.5,-1), radius = R, color = color.orange, axis = vec(0,0,Lrod))
    axle = cylinder(pos = vec(18.6,-0.5+Lrod/2,bat.pos.z+Lrod), radius = R/6, axis = vec(0,4*R,0), opacity = 0)

    t = 0
    dt = 0.0001

    dtheta = 0

    while t < 20:
        rate(1000)
        torque = vec(0,100,0)
        L = L + torque*dt
        omega = L/I
        omega_scalar = dot(omega, norm(axle.axis))
        dtheta = omega_scalar*dt
        bat.rotate(angle=dtheta, axis=norm(axle.axis), origin=axle.pos)
    
        if bat.pos.x < 18:
            L = vec(0,0,0)
            bat.axis = vec(0,0,Lrod)
            bat.pos = vec(18.6,0.8,0)
            swing.disabled = False
            t = 0
            break
    
        t = t+dt
        
def swing(s):
    s.disabled = True
    batting(bat)
    return s.disabled
    
def pitching(p):
    print("test")
    global velocity
    if p == fastball:
        velocity = 41.6
        theta = 90
        rpm = 2000
    if p == curvball:
        velocity = 33.3
        theta = -30
        rpm = 2500
    if p == changeup:
        velocity = 35
        theta = 90
        rpm = 1700
    if p == sliderball:
        velocity = 38
        theta = 45
        rpm = 2500
    if p == knuckleball:
        velocity = 30.5
        theta = 90
        rpm = 65
    
    ball.rot_axis = vec(0,cos(radians(theta)),sin(radians(theta)))
    ball.w = (rpm/60)*2*3.14*ball.rot_axis
    ball.alpha = (rpm/60)*2*3.14/5000*ball.rot_axis

def startbtn(b):
    b.disabled = True
    return b.disabled
    

ground = box(pos = vec(0,0,0), size = vec(120,0.01, 100), color = color.green)
mound = cylinder(pos = vec(0,0,0), axis = vec(0,1,0), radius = 2.7, length = 0.01, color = color.orange)
pitch = box(pos = vec(0,0,0), size = vec(0.15,0.1,0.61), color = color.white)
ball = sphere(pos = vec(0,1.95,0), radius = 0.037, texture = textures.rough, make_trail = False)
home = box(pos = vec(18.44,0.01,0), size = vec(0.3,0.1,0.43), color = color.white)
bat = cylinder(pos = vec(18.6,0.8,0), radius = 0.03, color = color.orange, axis = vec(0,0,1))

pt1 = vec(18.44,0.4,0.22)
pt2 = vec(18.44,1.2,0.22)
pt3 = vec(18.44,0.4,-0.22)
pt4 = vec(18.44,1.2,-0.22)
curve(pos = [pt1,pt2], color = color.cyan)
curve(pos = [pt1,pt3], color = color.cyan)
curve(pos = [pt3,pt4], color = color.cyan)
curve(pos = [pt2,pt4], color = color.cyan)

g = vec(0,-9.8,0)
air_rho = 1.23
cd = 0.4
cm = 0.22
A = 3.14*(ball.radius**2)
rpm = 0
theta = 90
e = 0.41
phi = rand.uniform(-10,10)
delta = rand.uniform(-10,10)

ball.m = 0.145
ball.v = vec(0,sin(radians(phi)),sin(radians(delta)))
ball.a = vec(0,0,0)
ball.rot_axis = vec(0,0,0)
ball.w = vec(0,0,0)
ball.alpha = vec(0,0,0)

wind_v = vec(0,0,0)

bat.m = 1
bat.v = vec(-36,0,0)

btn = button(text = 'Start', bind = startbtn)
swing = button(text = 'swing', bind = swing)

fastball = radio(bind = pitching, text = 'fast', name='rads')
curvball = radio(bind = pitching, text = 'curve', name='rads')
changeup = radio(bind = pitching, text = 'changeup', name='rads')
sliderball = radio(bind = pitching, text = 'slider', name='rads')
knuckleball = radio(bind = pitching, text = 'knuckle', name='rads')

t = 0
dt = 0.001

#scene.camera.follow(ball)
#scene.camera.follow(bat)
scene.camera.pos = vec(19.5,1,0)
scene.camera.axis = vec(-1,0,0)
scene.range = 1
scene.bind("keydown", on_keydown)

while t<10:
    rate(1000)
    
    if btn.disabled == True:
        
        if t<3:
            if 3-t<0.1:
                t=3
            label(pos=vec(18,2,0), text=3-t)
            t = t + dt*10
            continue
        
        ball.make_trail = True
        
        wind_v = vec(rand.uniform(-1,1),rand.uniform(-1,1),rand.uniform(-5,5))
        ball.v_w = ball.v - wind_v
        
        ball.a.x = (velocity**2)/(2*4)
        Fg = ball.m*g
        Fd = -0.5*cd*air_rho*A*(mag(ball.v_w)**2)*norm(ball.v_w)
        Fm = -0.5*cm*air_rho*A*ball.radius*mag(ball.w)*mag(ball.v)*cross(norm(ball.w),norm(ball.v))
        ball.f = ball.a*ball.m + Fg + Fd + Fm
        ball.v = ball.v + ball.f/ball.m*dt
        ball.pos = ball.pos + ball.v*dt
        
        ball.w = ball.w + ball.alpha*dt
        dtheta = mag(ball.w)*dt
        ball.rotate(angle = dtheta, axis = norm(ball.w), origin = ball.pos)
        
        if abs(ball.pos.y - bat.pos.y) < bat.radius and abs(ball.pos.x - bat.pos.x) < bat.radius:
            print("hit!")
            collision(ball, bat, e)
            ball.a.x = (bat.v.x**2)/(2*120)
            t = 0
            while t<10:
                rate(1000)
                ball.v = ball.v + ball.a*dt
                ball.pos = ball.pos - ball.v*dt
                t = t + dt
            break
        
        if ball.pos.x > 18.5 or ball.pos.y < 0:
            ball.v = vec(0,0,0)
            print(t-3)
            scene.waitfor('click')
            btn.disabled = False
            ball.pos = vec(0,1.95,0)
            ball.make_trail = False
            phi = rand.uniform(-10,10)
            delta = rand.uniform(-10,10)
            ball.v = vec(0,sin(radians(phi)),sin(radians(delta)))
            t = 0
        
        t = t + dt
