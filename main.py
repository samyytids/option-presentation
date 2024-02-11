from manim import *
from manim_slides import slide
from functools import partial

class PlotCombinedFunctions(slide.Slide):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-100, 100, 10],
            y_range=[-40, 40, 10],
            axis_config={"color": BLUE},
        )

        # Define constants
        option_price = 5
        strike_price = 0

        # Define functions for call and put options
        call_option_function = partial(self.call_option, option_price=option_price, strike_price=strike_price)
        put_option_function = partial(self.put_option, option_price=option_price, strike_price=strike_price)

        # Define the combined effect function
        call_option_function_g = lambda underlying_price: call_option_function(underlying_price)
        put_option_function_g = lambda underlying_price: put_option_function(underlying_price)
        combined_function = lambda underlying_price: call_option_function(underlying_price) + put_option_function(underlying_price)

        # Plot the combined function on the axes
        call = axes.plot(call_option_function_g, color=RED)
        put = axes.plot(put_option_function_g, color=RED)
        straddle = axes.plot(combined_function, color=RED)

        # Display the axes and the graph
        self.play(Create(axes), Create(call))
        self.next_slide()
        self.play(FadeOut(call))
        self.play(Create(put))
        self.play(FadeOut(put))
        self.play(Create(straddle))
        self.play(FadeOut(straddle))
        self.play(Transform(call, straddle))
        

    def call_option(self, underlying_price, option_price, strike_price):
        return -option_price if underlying_price - strike_price - option_price < -option_price else underlying_price - strike_price - option_price

    def put_option(self, underlying_price, option_price, strike_price):
        return -option_price if strike_price - underlying_price - option_price < -option_price else strike_price - underlying_price - option_price
