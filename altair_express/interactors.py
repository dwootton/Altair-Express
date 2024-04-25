from dataclasses import dataclass, field
from typing import Union, Callable, List, Any, Dict
from .signals import Signal
import altair as alt 

Expr = alt.Expr

@dataclass
class Processor:
    name: str
    expr: Expr

@dataclass
class Store:
    # This will be a base class for specific types of stores
    pass


from enum import Enum

class StoreTypes(Enum):
    Selection = "Selection" # any vegalite selection
    Numeric = "Numeric"
    String = "String"
    Enum = "Enum" # used for any field that has a limited set of values
    Boolean = "Boolean"
    Object = "Object"
    Array = "Array"
    DateTime = "DateTime"
    # custom stores
    XY = "XY" # used for any field that has a limited set of values
    Bin = "Bin" # {start, end, value}


class Listener : Union[alt.Selection, Signal]

# these generator classes will be the internal data representation for an interactor. 

# above will be generator factories that generate the correct generators from some spec 
    # brush() generator will take in the chart, etc and then produce the interval selection generator
    # datum_click() generator will take in the chart, etc and then produce the point selection generator

# well this should specify the properties of a selection
# specific selection details should be abstracted away. but some details might matter

# how do you guantere that a listener outputs a signal name or that the processors output the required attr?
class Generator:
    name: str
    listener: Listener
    value: Expr # Expr that evaluates to the store type
    type: StoreTypes
    processors: List[Processor]
    """Class to handle different types of generators for interaction techniques."""
    def __init__(self, listener, name = "generator", value = "", processors = [],  type=None):
        self.name = name # 
        self.value = value
        self.type = StoreTypes[type]
        self.processors = processors

        # Check if the input is an Altair selection
        if isinstance(listener, alt.Selection): 
            # note: selection can't be a listener as some details of selections are not known by defualt 
            # for example, to "make" a selection for someone, you probably need to know if you should use an encoding
            # but we don't want to require that information.
            # lets do this, lets require that the selection can be used, but certain fn will create selection for someone. 
            # ie highlight_brush() will create a selection when added to a chart.


            listener=listener.update(name="selection_"+name) # ensure name is consistent 
            self.value  = listener.name + "_tuple"
            self.type = StoreTypes.Selection
            
       
        self.listener = listener
    
    def __add__(self, other):
        # TODO: allow for multiple generators to be merged into a single generator, and the stores to be updated appropriately
        # if isinstance(other, Generator):
        #     return Interactor(self, other) # merge into multiple generators, each should then be piped to through 
        if isinstance(other, Response):
            return Interactor(self, other)
        return NotImplemented

    def __repr__(self):
        return f"Generator with selection: {self.generator.selection}"


@dataclass
class ResponseParameters:
    # Additional parameters for response function
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Response:
    ResponseFn:  Callable[[alt.Chart, Generator, ResponseParameters], alt.Chart]

# Define the ResponseFn type as a callable
@dataclass
class Interactor:
    generator: Generator
    response: Response  # Using string annotation for forward declaration

# brush = alt.selection_interval(encodings=['x'])
# generator = Generator(brush)
# response = (spec,generator) => highlight_brush(spec, generator)
# 
# by default selection store should just be params for a regualr selection object 


# 
brush = alt.selection_interval(encodings=['x']) # this is likely dependent on the spec, as how do you know if you don't want to specify x?



# TODO: go through and create some example interaction techniques for Interactors 
# TODO: create test infrastructure for a given Interactor and vis. 
# TODO Next: update the interactions.py (duplicate) to use this new structure, 
# TODO Next: verify all the same interaction techniques are transitioned over and still work
# TODO After: go through and set up signal generators. 

click = alt.selection_single(on='click')
on_hover = alt.selection_single(on='mouseover')



persistent_click = DatumClick() + Highlight()
ephemeral_hover = DatumHover() + Highlight()


persistent_click + ephemeral_hover + scatterplot


# goal: 




# I want to build a 

# VL selection on click activate 
# VL selection on hover activate 
# note: activate needs to be aware for other conditions, if a condition is already available on color encode, it needs to add to it.
# how do you handle the cases where interaction should be composable. 
# if both exist, then the one that comes after should be used. 
# I should be able to add color on hover and then also add persistence on click 
# I should be able to add a brush and then add a click to activate.
    # by default, if response encounters another condition, it should "or" conditions

    # resolution?
