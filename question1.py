from manim import * 
from manim_slides.slide import Slide
from functions import * 
import functools
import math as maths

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
