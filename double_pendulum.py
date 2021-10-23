import taichi as ti

ti.init(arch=ti.cuda)

res=(512, 512)
N = 100    #Number of double pendulum
g = 9.8    
pi = 3.141592653
l_1 = 0.2  #length of the first rod
l_2 = 0.2  #length of the second rod
m_1 = 1.0  #mass of the first pendulum
m_2 = 1.0  #mass of the second pendulum
delta = 0.01  #offset of initial position
scaler = 1.0

paused = True

h = 1e-2
substepping = 100
center = ti.Vector([0.5, 0.5])
ang_0 = ti.Vector([pi, pi]) #initial position of pendulum

ang = ti.Vector.field(2, ti.f32, N) 
v_ang = ti.Vector.field(2, ti.f32, N)
a_ang = ti.Vector.field(2, ti.f32,N)

origin = ti.Vector.field(2, ti.f32,N)
pos_1 = ti.Vector.field(2, ti.f32, N)
pos_2 = ti.Vector.field(2 , ti.f32, N)

@ti.kernel
def initialize():
    for i in range(N):
        ang[i] = ang_0 + ti.Vector([0, -delta*i/N])
        origin[i] = center
        v_ang[i] *= 0.0

@ti.kernel
def set_pos():
    for i in range(N):
        pos_1[i] = center + ti.Vector([l_1 * ti.sin(ang[i][0]), -l_1 * ti.cos(ang[i][0])]) * scaler
        pos_2[i] = pos_1[i] + ti.Vector([l_2 * ti.sin(ang[i][1]), -l_2 * ti.cos(ang[i][1])]) * scaler


@ti.kernel
def compute():
    for i in range(N):
        a_ang[i] = ti.Vector([(-g*(2*m_1+m_2)*ti.sin(ang[i][0])-m_2*g*ti.sin(ang[i][0]-2*ang[i][1])-2*ti.sin(ang[i][0]-ang[i][1])*m_2*(v_ang[i][1]**2*l_2+v_ang[i][0]**2*l_1*ti.cos(ang[i][0]-ang[i][1])))/(l_1*(2*m_1+m_2-m_2*ti.cos(2*ang[i][0]-2*ang[i][1]))),\
            (2*ti.sin(ang[i][0]-ang[i][1])*(v_ang[i][0]**2*l_1*(m_1+m_2)+g*(m_1+m_2)*ti.cos(ang[i][0])+v_ang[i][1]**2*l_2*m_2*ti.cos(ang[i][0]-ang[i][1])))/(l_2*(2*m_1+m_2-m_2*ti.cos(2*ang[i][0]-2*ang[i][1])))])

@ti.kernel
def update():
    dt = h/substepping
    for i in range(N):
        v_ang[i] += a_ang[i] * dt
        ang[i] += v_ang[i] *dt
        # ang[i] %= 2*pi #Prevent value overflow after run a while

initialize()
set_pos()

gui = ti.GUI('Double Pendulum', res)

while gui.running:
# for i in range(100):
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key == ti.GUI.ESCAPE:
            exit()
        elif e.key == ti.GUI.SPACE:
            paused = not paused
            print('Pause status:',{paused})
        elif e.key == 'r':
            print('Reset pendulum position and velocity')
            initialize()
            set_pos()
    
    if not paused:
            for i in range(substepping):
                compute()
                update()   
            set_pos()
    gui.clear(0x112F41)
    gui.lines(origin.to_numpy(), pos_1.to_numpy(), color=0x068587, radius = 1)
    gui.lines(pos_1.to_numpy(), pos_2.to_numpy(), color=0x068587, radius = 1)
    gui.circles(pos_1.to_numpy(), color = 0xffffff, radius=5)
    gui.circles(pos_2.to_numpy(), color = 0xffffff, radius=5)
    gui.show()
# ti.print_kernel_profile_info('count')

# window = ti.ui.Window('Double Pendulum', res)
# canvas = window.get_canvas()

# while window.running:
#     # for i in range(substepping):
#     #     compute()
#     #     update()
#     # set_pos()

#     # canvas.set_back_ground_color(0x112F41)
#     canvas.lines(origin, width=1, color=0x068587)
#     window.show()