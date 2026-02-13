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

def ode_solution_points(function,state0, time, dt=0.01):
    solution = solve_ivp(
      function,
      t_span=(0, time),
      y0=state0,
      t_eval=np.arange(0,time,dt)  
    )
    return solution.y.T

class LorentzInteractive(Scene):
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

        #self.play(Create(axes))

        #Display lorenz system state evolution
        state0 =  [10,10,10]
        points = ode_solution_points(lorenz_system, state0, 100)
        normalized_points = axes.c2p(points)

        curve = OpenGLVMobject().set_points_smoothly(normalized_points)
        curve.color = BLUE
        self.play(Create(curve), run_time=8)
        self.wait()
        self.interactive_embed()
