from manim import * 
from manim_slides.slide import Slide
from functions import * 
import functools
import math as maths
import sympy as sp
import numpy as np
from scipy.misc import derivative

class CustomSlide(Slide):
    def create_partial_functions(self, functions: list[dict]):
        self.component_functions = []
        self.combined_functions = []
        
        combined_function = None
        
        for function in functions:
            partial_function = functools.partial(
                function_map[function["name"]],
                option_price=function.get("option_price"),
                strike_price=function.get("strike_price"),
            )
            self.component_functions.append(partial_function)
            
            # Define a lambda function capturing the value of `function` at this iteration
            # combined_function = lambda underlying_price, func=function: sum(
            #     pf(underlying_price) 
            #     for pf in self.component_functions[:functions.index(func)+1]
            # )
            # self.combined_functions.append(combined_function)
            
            def combined_function_builder(component_functions):
                def combined_function(underlying_price):
                    total_function = lambda underlying_price: sum(pf(underlying_price) for pf in component_functions)
                    return total_function(underlying_price = underlying_price)
                return combined_function

            # Update combined_function with new combined function

            # Append the combined function to combined_functions list
            # self.combined_functions.append(combined_function)
            components_up_to_current_index = self.component_functions.copy()
            self.combined_functions.append(combined_function_builder(components_up_to_current_index))
        
    def create_lambdas(self, partials):
        lambdas = [lambda underlying_price, pf=pf: pf(underlying_price=underlying_price) for idx, pf in enumerate(partials)]
        return lambdas

    def create_component_axes(self):
        self.axes = VGroup()
        for i in range(len(self.component_functions)):
            axis = Axes(
                x_range=[-10, 10, 1],
                y_range=[-10, 10, 1],
                axis_config={"color": WHITE},
            )
            if len(self.component_functions) > 1:
                axis.scale_to_fit_width(maths.floor((14.2-1)/len(self.component_functions)))
            else:
                axis.scale_to_fit_height(3)
                
            if i != 0:
                axis.match_y(self.axes[0])
                axis.match_x(self.axes[0])
                axis.set_x(self.axes[0].get_x()+ axis.width*i + (1/len(self.component_functions))*i)
            else:
                axis.to_edge(LEFT, buff=0.1)
                axis.to_edge(UP, buff=0.1)

            self.axes += axis

        self.axes.center()
        self.axes.to_edge(UP, buff=0)
    
    def create_final_axis(self):
        self.final_axis.center()
        self.final_axis.scale_to_fit_height(8 - self.axes[0].get_y()-1)
        self.final_axis.set_y(self.axes[0].get_y()-(self.axes[0].height)/2-(self.final_axis.height/2)-0.1)
    
    def plot_components(self):
        self.plots = [self.axes[idx].plot(lambda_function, color=RED) for idx, lambda_function in enumerate(self.component_lambdas)]
    
    def construct_component_plots(self):
        [self.play(Create(plot), Create(self.axes[idx])) for idx, plot in enumerate(self.plots)]
    
    def construct_strategy(self):
        index_range = len(self.component_functions)
        for i in range(index_range):
            self.next_slide()
            self.play(Transform(self.plots[i], self.plots[i].copy().set_color(BLUE).set_stroke(width=12)))
            self.play(Transform(self.plots[i], self.plots[i].copy().set_color(GRAY).set_stroke(width=1)))
            if i == 0:
                g = self.final_axis[0].plot(self.combined_lambdas[0], color=RED)
                self.play(Create(self.final_axis))
                self.play(Create(g))
            else:
                g2 = self.final_axis[0].plot(self.combined_lambdas[i], color=RED)
                self.play(Transform(g, g2)) 
    
    def create_arrow_animations(self):
        # Create initial arrow
        start_x = -10.0
        start_y = self.combined_functions[-1](underlying_price=start_x)
        arrow_tip = self.final_axis[0].coords_to_point(start_x, start_y)
        arrow_tip[1] = arrow_tip[1] + 0.25
        arrow_tail = np.array([arrow_tip[0], arrow_tip[1]-1.5, arrow_tip[2]])
        arrow = Arrow(start=arrow_tail, end=arrow_tip, color=WHITE, stroke_width=3)
        
        points = []

        # Calculate the gradient at each point in the range
        for x in np.arange(-10, 10, 0.1):
            x = round(x, 1)
            y = round(self.combined_functions[-1](underlying_price = x), 1)
            points.append((x, y))
        
        gradient_changes = [(start_x, start_y)]
        for idx, point in enumerate(points):
            if idx == 0:
                continue
            elif idx == 1:
                delta_old = round(points[idx-1][1] - point[1], 1)
            else:
                if round(points[idx-1][1] - point[1], 1) != delta_old:
                    delta_old = round(points[idx-1][1] - point[1], 1)
                    gradient_changes.append(points[idx])
        
        end_x = 10.0
        end_y = self.combined_functions[-1](underlying_price=end_x)
        
        gradient_changes.append((end_x, end_y))
        
        positions = [self.final_axis[0].coords_to_point(point[0], point[1]) for point in gradient_changes]   
        
        transforms = []
        arrows = [arrow]
        for idx, position in enumerate(positions):
            if idx == len(positions) -1:
                continue
            
            movement = positions[idx+1] - position
            move_right = Transform(arrow, arrow.copy().shift(movement))
            move_left = Transform(arrow, arrow.copy())
            
            transforms.append(Succession(move_right, move_left))
            arrow = arrow.copy().shift(movement)
            arrows.append(arrow)
        
        for idx, transform in enumerate(transforms):
            self.next_slide(loop=True)
            self.play(transform, run_time=4)
            self.remove(arrows[idx])
            
            
            
            

class Question1(CustomSlide):
    def construct(self):
        
        # Question 1
        
        self.graphs = [
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)
        
        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 1:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("We have a very bullish investor.").scale_to_fit_width(10).center()
        text2 = Text("Bullish means optimistic, so they think the stock price will go up...").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("A LOT").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3
        )
        text.center()
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
            
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        self.graphs = [
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)
        
        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        text1 = Text("Now, why is buying a call more bullish?").scale_to_fit_width(10).center()
        text2 = Text("The easiest way to explain that is to show you!").scale_to_fit_width(10).next_to(text1, DOWN)
        text = VGroup(
            text1, 
            text2, 
        )
        text.center()
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
            
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 2
        
        self.graphs = [
            {
                "name" : "long_stock",
                "option_price" : 0,
            },
            {
                "name" : "long_put",
                "option_price" : -1,
                "strike_price" : 0
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 2:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("We have an investor that wants to own the stock").scale_to_fit_width(10).center()
        text2 = Text("But is worried about downside risk.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("This means they are...").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("SCARED").scale_to_fit_width(10).next_to(text3, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 3
        
        self.graphs = [
            {
                "name" : "long_stock",
                "option_price" : 0,
            },
            {
                "name" : "short_call",
                "option_price" : 1,
                "strike_price" : 3
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 3:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("In the short term this investor is a little bullish.").scale_to_fit_width(10).center()
        text2 = Text("So, optimistic but not that optimistic.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("A Wuss").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 4
        
        self.graphs = [
            {
                "name" : "short_put",
                "option_price" : 1,
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 4:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("Your investor is bullish, but not that bullish.").scale_to_fit_width(10).center()
        text2 = Text("So, optimistic but not that optimistic.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("A Coward").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 5
        
        self.graphs = [
            {
                "name" : "short_stock",
                "option_price" : 0,
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 2,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 5:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("Your investor is bearish.").scale_to_fit_width(10).center()
        text2 = Text("But they are worried about downside risk.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Yellow bellied").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
    
    
        # Question 6
        
        self.graphs = [
            {
                "name" : "short_stock",
                "option_price" : 0,
            },
            {
                "name" : "short_put",
                "option_price" : 1,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 6:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("Your investor is bearish, but not too bearish.").scale_to_fit_width(10).center()
        text2 = Text("So they are expecting prices to go down, but not crash.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Insured").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 7
        
        self.graphs = [
            {
                "name" : "long_put",
                "option_price" : -1,
            },
            {
                "name" : "long_call",
                "option_price" : -1,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 7:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("Your investor thinks markets will move a lot.").scale_to_fit_width(10).center()
        text2 = Text("But they don't know in which direction.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Pause to talk about biotech again...").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 8
        
        self.graphs = [
            {
                "name" : "short_put",
                "option_price" : 1,
            },
            {
                "name" : "short_call",
                "option_price" : 1,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 8:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor thinks the market isn't going to move.").scale_to_fit_width(10).center()
        text2 = Text("So, their expectation is neither bearish nor bullish.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Pause to talk about Apple or Kellogs again...").scale_to_fit_width(10).next_to(text2, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 9
        
        self.graphs = [
            {
                "name" : "long_put",
                "option_price" : -0.5,
                "strike_price" : -1,
            },
            {
                "name" : "long_call",
                "option_price" : -0.5,
                "strike_price" : 1,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 9:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor REALLY thinks that markets are going to move a lot.").scale_to_fit_width(10).center()
        text2 = Text("So, their expectation is neither bearish nor bullish.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("They're just betting on volatility.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("Degenerate gambler").scale_to_fit_width(10).next_to(text3, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 10
        
        self.graphs = [
            {
                "name" : "short_put",
                "option_price" : 0.5,
                "strike_price" : -1,
            },
            {
                "name" : "short_call",
                "option_price" : 0.5,
                "strike_price" : 1,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 10:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor REALLY thinks that markets aren't going to move a lot.").scale_to_fit_width(10).center()
        text2 = Text("So, their expectation is neither bearish nor bullish.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("They're just betting on a lack of volatility.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("A boring degenerate gambler").scale_to_fit_width(10).next_to(text3, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 11
        
        self.graphs = [
            {
                "name" : "short_call",
                "option_price" : 1,
                "strike_price" : 2,
            },
            {
                "name" : "long_put",
                "option_price" : -1,
                "strike_price" : -2,
            },
            {
                "name" : "long_stock",
                "option_price" : 0,
            }
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 11:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor is already writing covered calls.").scale_to_fit_width(10).center()
        text2 = Text("(see question 3).").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("But, this one is specifically worried about downside risk.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("Just plain boring").scale_to_fit_width(10).next_to(text3, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 12
        
        self.graphs = [
            {
                "name" : "long_call",
                "option_price" : -2,
                "strike_price" : 1,
            },
            {
                "name" : "short_call",
                "option_price" : 1,
                "strike_price" : 3,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 12:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("The investor moderately bullish and want to make money with calls.").scale_to_fit_width(10).center()
        text2 = Text("I guess they just like calls more than puts.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("They want to speculate based on expectations of low price increases.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("I don't even have an insult for this.").scale_to_fit_width(10).next_to(text3, DOWN)
        text5 = Text("(talk about strike prices and options prices)").scale_to_fit_width(10).next_to(text4, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
            text5
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        self.graphs = [
            {
                "name" : "long_put",
                "option_price" : -2,
                "strike_price" : 1,
            },
            {
                "name" : "short_put",
                "option_price" : 3,
                "strike_price" : 3,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        self.next_slide()
        text1 = Text("You can also do this with puts.").scale_to_fit_width(10).center()
        text2 = Text("This is if you like puts more than calls I guess").scale_to_fit_width(10).next_to(text1, DOWN)
        text = VGroup(
            text1, 
            text2,  
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 13
        
        self.graphs = [
            {
                "name" : "short_call",
                "option_price" : 3,
                "strike_price" : 1,
            },
            {
                "name" : "long_call",
                "option_price" : -1,
                "strike_price" : 4,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 13:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor is mildly bearish.").scale_to_fit_width(10).center()
        text2 = Text("This one doesn't like the other strategies.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Even the ones for their expectations.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("Picky").scale_to_fit_width(10).next_to(text3, DOWN)
        text5 = Text("(talk about strike prices and options prices... again)").scale_to_fit_width(10).next_to(text4, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
            text5, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        # Question 14
        
        self.graphs = [
            {
                "name" : "short_call",
                "option_price" : 2,
                "strike_price" : 0,
            },
            {
                "name" : "short_call",
                "option_price" : 2,
                "strike_price" : 0,
            },
            {
                "name" : "long_call",
                "option_price" : -3.5,
                "strike_price" : -2,
            },
            {
                "name" : "long_call",
                "option_price" : -1.5,
                "strike_price" : 2,
            },
        ]
        
        self.final_axis = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            axis_config={"color": WHITE},
        )
        labels = self.final_axis.get_axis_labels(
            Tex("underlying price").scale(0.7), Tex("pay off").scale(0.7)
        )
        
        self.final_axis = VGroup(self.final_axis, labels)
        
        self.create_partial_functions(self.graphs)
        self.component_lambdas = self.create_lambdas(self.component_functions)
        self.combined_lambdas = self.create_lambdas(self.combined_functions)

        self.create_component_axes()
        self.create_final_axis()
        self.plot_components()
        title = Text("Question 14:").scale_to_fit_width(10).to_edge(UP)
        self.play(Create(title))
        self.next_slide()
        text1 = Text("This investor is bearish on volatility, but neutral on direction.").scale_to_fit_width(10).center()
        text2 = Text("Doesn't think stocks will move much.").scale_to_fit_width(10).next_to(text1, DOWN)
        text3 = Text("Doesn't know or care which direction they'll move either.").scale_to_fit_width(10).next_to(text2, DOWN)
        text4 = Text("Boring gambler").scale_to_fit_width(10).next_to(text3, DOWN)
        text5 = Text("(talk about strike prices and options prices... again also a very annoying strategy to describe)").scale_to_fit_width(10).next_to(text4, DOWN)
        text = VGroup(
            text1, 
            text2, 
            text3, 
            text4, 
            text5, 
        )
        text.center().next_to(title, DOWN)
        for item in text:
            self.play(Create(item), wait=True)
            self.next_slide()
        
        self.play(Uncreate(title))
        self.play(Uncreate(text))
        
        self.construct_component_plots()
        self.construct_strategy()
        self.create_arrow_animations()
        self.clear()
        
        
        title = Text("Thanks for coming!").scale_to_fit_width(10).center()
        self.play(Create(title))
        sub_title = Text("You had better appreciate how much effort I put into this").scale_to_fit_width(10).next_to(title, DOWN)
        
        self.next_slide()
        self.play(Create(sub_title))
        self.next_slide()
        self.play(Uncreate(title, sub_title))
        extra = Text("Please clap...").scale_to_fit_width(10).center()
        self.play(Create(extra))
        
        