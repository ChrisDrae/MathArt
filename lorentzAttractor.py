from manim import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from manim import OpenGLPMobject
from manim.opengl import OpenGLVMobject


# Comman for runnning in open GL Renderer { manim -p file.py SceneName --renderer=opengl }

def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3 ):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y -beta * z
    return [dxdt, dydt, dzdt]

def rossler_system(t, state, sigma=0.2, rho=0.2, beta=5.7):
    x, y, z = state
    dxdt = -y-z
    dydt = x + sigma * y
    dzdt = rho + z * (x - beta)
    return [dxdt,dydt,dzdt]

def chen_system(t, state, sigma=35, rho= 3, beta=28):
    x, y, z = state
    dxdt = sigma*(y - x)
    dydt = (beta - sigma)*x - x*z + beta * y
    dzdt = x * y - rho * z
    return [dxdt,dydt, dzdt]


def aizawa_system(t, state, sigma=0.95, rho=0.7, beta=0.6, phi=3.5, epsilon=0.25):
    x, y, z = state
    dxdt = (z - rho)*x - phi*y
    dydt = phi*x + (z-rho)*y
    dzdt = beta + sigma*z-(z**3)/3 - ((x**2)+(y**2))*(1 + epsilon*z)
    return [dxdt,dydt,dzdt]

def ode_solution_points(function,state0, time, dt=0.01):
    solution = solve_ivp(
      function,
      t_span=(0, time),
      y0=state0,
      t_eval=np.arange(0,time,dt)  
    )
    return solution.y.T



class LorentzInteractive(Scene):
    #Storage for useful function calls
    def renderLorenzAttractor(self, axes):
        state1 = [100,20,20]
        points1 = ode_solution_points(lorenz_system,state1, 100)
        secondCurve = OpenGLVMobject().set_points_smoothly(axes.c2p(points1))
        secondCurve.color = RED
        self.play(Create(secondCurve, run_time=8))

    def renderRossler(self, axes):
        state0 =  [10,10,100]
        pointsRossler = ode_solution_points(rossler_system, state0, 100)

        curve = OpenGLVMobject().set_points_smoothly(axes.c2p(pointsRossler))
        curve.color = GREEN
        curve.shift([10,0,0])
        self.play(Create(curve), run_time=1)

    def renderChessler(self, axes, state0):
         #Render Chen Attractor 
        pointsChen = ode_solution_points(chen_system, state0, 100)

        curve = OpenGLVMobject().set_points_smoothly(axes.c2p(pointsChen))
        curve.color = RED
        curve.shift([-10,0,0])
        self.play(Create(curve), run_time=1)




    def construct(self):
        #Setting up Axes
        axes = ThreeDAxes(
            x_range=(-50, 50,5),
            y_range=(-50, 50,5),
            z_range=(-0, 50,5),
            x_length=16,
            y_length=16,
            z_length=8,
        )
        axes.center()

        self.play(Create(axes))

        #Display lorenz system state evolution
        state0 =  [10,10,100]
        points = ode_solution_points(lorenz_system, state0, 100)
        normalized_points = axes.c2p(points)

        curve = OpenGLVMobject().set_points_smoothly(normalized_points)
        curve.color = BLUE
        curve.shift([20,0,0])
        self.play(Create(curve))
        
        #Render Aizawa Attractor 
        stateInit = [0.1,0,0]

        pointsAizawa = ode_solution_points(aizawa_system, stateInit, 100)
        curve = OpenGLVMobject().set_points_smoothly(pointsAizawa)
        self.play(Create(curve), run_time=10)

        self.wait()
        self.interactive_embed()
