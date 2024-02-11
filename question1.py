from manim import * 
from manim_slides.slide import Slide
from functions import * 
import functools
import math as maths
import sympy as sp

def gradient_of_function(f):
    x = sp.Symbol('x')
    y = f(x)

    # Differentiate y with respect to x
    dy_dx = sp.diff(y, x)

    # Define a function that returns the gradient at a given point
    gradient_func = sp.lambdify(x, dy_dx, 'numpy')

    return gradient_func

def create_arrow_animations(x_range: tuple[int,int], partial_function: functools.partial) -> list[Succession]:
    gradients_changes = set()
    x = x_range[0]
    gradient = gradient_of_function(partial_function)
    print(gradient)
    while x < x_range[1]:
        print(gradient(x))
        if gradient(x) not in gradients_changes:
            gradients_changes.add(x)
        x += 0.1
    return gradients_changes

class CustomScene(Slide):
    def create_graphs(self, graphs):
        self.option_functions = []
        self.combined_functions = []
        for idx, graph in enumerate(graphs):
            self.option_functions.append(function_map[graph])
            if len(self.combined_functions) == 0:
                self.combined_functions.append(function_map[graph])
            else:
                functions = self.option_functions[:idx+1]
                self.combined_functions.append(
                    lambda underlying_price, option_price, strike_price, funcs=functions: sum(
                        [f(underlying_price=underlying_price, option_price=option_price, strike_price=strike_price) for f in funcs]
                    )
                )

    def create_lambdas(self, start_lambdas, option_price, strike_price):
        partial = [functools.partial(function, option_price=option_price, strike_price=strike_price) for function in start_lambdas]
        lambdas = [lambda underlying_price, pf=pf: pf(underlying_price=underlying_price) for pf in partial]
        return lambdas
    
    def highlight_and_pulsate(self, obj):
        # Define the pulsating animation
        pulsating_anim = Succession(
            ApplyMethod(obj.set_color, BLUE),
            ApplyMethod(obj.set_color, RED),
        )

        return pulsating_anim

class Question2(CustomScene):
    def construct(self):
        # Make these into dicts that contain the short value
        graphs = ["long_call_option", "long_put_option", "long_stock", "long_call_option"]
        option_price = 1
        strike_price = 0
        self.create_graphs(graphs)

        axes = VGroup()
        for i in range(len(graphs)):
            axis = Axes(
                x_range=[-10, 10, 1],
                y_range=[-10, 10, 1],
                axis_config={"color": BLUE},
            )
            axis.scale_to_fit_width(maths.floor((14.2-1)/len(graphs)))

            if i != 0:
                axis.match_y(axes[0])
                axis.match_x(axes[0])
                axis.set_x(axes[0].get_x()+ axis.width*i + (1/len(graphs))*i)
            else:
                axis.to_edge(LEFT, buff=0.1)
                axis.to_edge(UP, buff=0.1)

            axes += axis

        axes.center()
        axes.to_edge(UP, buff=0)

        final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": BLUE},
        )

        final_axis.center()
        final_axis.scale_to_fit_height(8 - axes[0].get_y()-1)
        final_axis.set_y(axes[0].get_y()-(axes[0].height)/2-(final_axis.height/2)-0.1)

        component_lambdas = self.create_lambdas(self.option_functions, option_price=option_price, strike_price=strike_price)
        combined_lambdas = self.create_lambdas(self.combined_functions, option_price=option_price, strike_price=strike_price)

        plots = [axes[idx].plot(lambda_function, color=RED) for idx, lambda_function in enumerate(component_lambdas)]

        [self.play(Create(plot), Create(axes[idx])) for idx, plot in enumerate(plots)]
        
        

        for idx, plot in enumerate(plots):
            self.next_slide()
            self.play(Transform(plot, plot.copy().set_color(BLUE).set_stroke(width=12)))
            self.play(Transform(plot, plot.copy().set_color(GRAY).set_stroke(width=1)))
            if idx == 0:
                g = final_axis.plot(combined_lambdas[0], color=RED)
                self.play(Create(final_axis))
                self.play(Create(g))
            else:
                g2 = final_axis.plot(combined_lambdas[idx], color=RED)
                self.play(Transform(g, g2))        
        
        underlying_price = -10
        start_x = underlying_price
        start_y = combined_lambdas[-1](underlying_price=underlying_price)
        end_y = start_y
        while start_y == end_y:
            underlying_price += 0.1
            end_y = combined_lambdas[-1](underlying_price=underlying_price)
            end_x = underlying_price
            
        start_position = final_axis.coords_to_point(start_x, start_y)
        end_position = final_axis.coords_to_point(end_x, end_y)
        movement = end_position - start_position
        
        start = [start_position[0], start_position[1]-2, start_position[2]+2]
        end = [start_position[0], start_position[1]-0.15, start_position[2]+2]
        
        arrow = Arrow(start=start, end=end, color=WHITE, stroke_width=3)
        self.play(Create(arrow))
        
        right = movement
        move_right = Transform(arrow, arrow.copy().shift(right))
        move_left = Transform(arrow, arrow.copy())
        
        loop_animation = Succession(move_right, move_left)
        self.next_slide(loop=True)
        self.play(loop_animation, run_time=2)
        
        
        positions = create_arrow_animations((-10, 10), combined_lambdas[-1])
        print(positions)
        