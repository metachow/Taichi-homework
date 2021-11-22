import taichi as ti
ti.init(ti.cuda)

res = 512

# integration method
# 1: symplectic euler
method = 1

N = 10

g = 9.8
pi = 3.141592653
l_1 = 0.2
l_2 = 0.2
m_1 = 1.0
m_2 = 1.0
delta = pi*2
YoungsModulus = ti.field(ti.f32, ())

h = 1.0
substepping = 500
dh = h/substepping

paused = True

center = ti.Vector([0.5, 0.5])

origin = ti.Vector.field(2, ti.f32,N)
pos_1 = ti.Vector.field(2, ti.f32, N)
pos_2 = ti.Vector.field(2, ti.f32, N)
vel_1 = ti.Vector.field(2, ti.f32, N)
vel_2 = ti.Vector.field(2, ti.f32, N)
acc_1 = ti.Vector.field(2, ti.f32, N)
acc_2 = ti.Vector.field(2, ti.f32, N)
grad_1 = ti.Vector.field(2, ti.f32, N)
grad_2 = ti.Vector.field(2, ti.f32, N)

@ti.kernel
def initialize():
    for i in range(N):
        YoungsModulus[None] = 2e4
        origin[i] = ti.Vector([0.5, 0.5])
        pos_1[i] = center + ti.Vector([l_1 * ti.sin(pi), -l_1 * ti.cos(pi)])
        pos_2[i] = pos_1[i] + ti.Vector([l_2 * ti.sin(pi - delta*i/N), -l_2 * ti.cos(pi - delta*i/N)])
        vel_1[i] *= 0
        vel_2[i] *= 0
        acc_1[i] *= 0
        acc_2[i] *= 0

@ti.kernel
def compute_gradient():
    for i in range(N):
        grad_1[i] = ti.Vector([0.0, 0.0])
        grad_2[i] = ti.Vector([0.0, 0.0])
    
    for i in range(N):
        r_1 = origin[i] - pos_1[i]
        r_2 = pos_1[i] - pos_2[i]
        l1 = r_1.norm()
        l2 = r_2.norm()

        k_1 = YoungsModulus[None]*l_1
        k_2 = YoungsModulus[None]*l_2

        gradient_1 = k_1*(l1-l_1)*r_1/l1
        gradient_2 = k_2*(l2-l_2)*r_2/l2
        
        grad_1[i] += -gradient_1
        grad_1[i] += gradient_2
        

        grad_2[i] += -gradient_2


        


@ti.kernel
def update():
    for i in range(N):
        if method == 1:
            acc_1[i] = -grad_1[i]/m_1 - ti.Vector([0.0, g])
            acc_2[i] = -grad_2[i]/m_2 - ti.Vector([0.0, g])

            vel_1[i] += dh * acc_1[i]
            vel_2[i] += dh * acc_2[i]

            pos_1[i] += dh * vel_1[i]
            pos_2[i] += dh * vel_2[i]

initialize()

gui = ti.GUI("Elastic Double Pendulums", (512, 512))

while gui.running:

    gui.clear(0x112F41)

    for e in gui.get_events(ti.GUI.PRESS):
        if e.key == ti.GUI.ESCAPE:
            exit()
        elif e.key == ti.GUI.SPACE:
            paused = not paused
        elif e.key == 'r':
            print('Reset pendulum position and velocity')
            initialize()
    
    if not paused:
        # gui.text(content="Running - SPACE to pause", pos=(0.35, 0.98), color=0x00ff00)
        compute_gradient()
        update()
    # else:
        # gui.text(content="Pause - SPACE to resume", pos=(0.35, 0.98), color=0xFF0000)
    
    gui.lines(origin.to_numpy(),pos_1.to_numpy(), color=0x068587, radius = 1)
    gui.lines(pos_1.to_numpy(),pos_2.to_numpy(), color=0x068587, radius = 1)
    gui.circles(pos_1.to_numpy(), color = 0xffffff, radius=5)
    gui.circles(pos_2.to_numpy(), color = 0xffffff, radius=5)
    gui.show()