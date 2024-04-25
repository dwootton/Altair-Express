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


class Listener : Union[alt.SelectionParameter, Signal]

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
        self.type = type
        self.processors = processors

        # Check if the input is an Altair selection
        if isinstance(listener, alt.SelectionParameter): 
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
    
    def generate_patch(self):
        patches = []

        # add the listener as a signal
        patches.append({"op":"add","path":f"/signals/-","value":self.listener})

        for processor in self.processors:
            patches.append({"op":"add","path":f"/signals/-","value":{"name":processor.name,"value":processor.expr}})
        
        patches.append({"op":"add","path":f"/signals/-","value":{"name":self.name+"_store","value":self.value}})

        return patches
        
        # add the listener as a signal
        # add each value in processor as signal 
        # then add value as signal with name = self.name+"_store"



        # use JSON patch
        


@dataclass
class ResponseParameters:
    # Additional parameters for response function
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Response:
    responseFn:  Callable[[alt.Chart, Generator, ResponseParameters], alt.Chart]
    params: Dict[str, Any] = field(default_factory=dict)

from .utils import is_encoding_meaningful,check_if_line, add_encoding,check_axis_binned, get_field_from_encoding, check_axis_aggregate, is_undefined, alt_get, extent_from_column

ALX_SELECTION_PREFIX = "ALX_SELECTION_"
ALX_SELECTION_SUFFIX= {
    "filter":"_FILTER",
    "scale_bind":"_FILTER",
    "highlight":"_FILTER",
    "group":"_GROUP",
    "label":"_FILTER" # often used as a part of a filtering operation
}
# problem: how do I create selections 
def create_selection(chart,type):
    selection = None
    
    if type == "interval":
        x_is_meaningful = is_encoding_meaningful(chart,'x')
        y_is_meaningful = is_encoding_meaningful(chart,'y')
        
        encodings =  [] # by default
        if x_is_meaningful :
            encodings.append('x')
        if y_is_meaningful:
            encodings.append('y')

        name = ALX_SELECTION_PREFIX+'drag'
        selection = alt.selection_interval(encodings=encodings, name=name)

    if type == "point":
        name = ALX_SELECTION_PREFIX+'click'

        selection = alt.selection_point(name=name)

        x_is_aggregate = check_axis_aggregate(chart,'x') 
        y_is_aggregate = check_axis_aggregate(chart,'y')

        fields = []
        if get_field_from_encoding(chart,'column'):
            fields = [get_field_from_encoding(chart,'column')]
            
        x_field = get_field_from_encoding(chart,'x')
        y_field = get_field_from_encoding(chart,'y')
        RESERVED_ALX_NAMES = ['level','jitter']
        x_is_meaningful = x_field and not any(x_field in s for s in RESERVED_ALX_NAMES) and not x_is_aggregate
        y_is_meaningful = y_field and not any(y_field in s for s in RESERVED_ALX_NAMES) and not y_is_aggregate
        
        if  x_is_meaningful and not y_is_meaningful:
            fields.append(x_field)
            # if x is aggregated (ie is a count), then add y field to selection 
            selection=alt.selection_point(name=name, encodings=['y'],fields=fields)
        elif not  x_is_meaningful and  y_is_meaningful:
            # if both of them are 
            fields.append(y_field)

            selection=alt.selection_point(name=name, encodings=['x'],fields=fields)
        elif not x_is_meaningful and not x_is_meaningful:
            selection=alt.selection_point(name=name, encodings=['x','y'],fields=fields)

    return selection 

def add_interactor(chart, interactor):
    # generate the patch for generator 
    # if interactor is a custom generator, then add generators to the ALX chart 
    if interactor.generator.type != StoreTypes.Selection:
        # custom generator, must be added to the chart later 
        chart.add_generator(interactor.generator)
    else: 
        # selection generator, add to the chart directly 
        chart = chart.add_params(interactor.generator.listener)

    return interactor.response.responseFn(chart, interactor.generator, interactor.response.params)

class Interactors: 
    def __init__(self,interactors):
        self.interactors = interactors

    def __add__(self, other):
        if isinstance(other,alt.TopLevelMixin):
            # if added to a nonalx chart convert to ALX chart
            chart = ALXChart(chart=other)
            
            for interactor in self.interactions:
                chart = add_interactor(chart,interactor)
            return chart
        #chart 
        if isinstance(other,Interactor):
            self.interactors.append(other)
        elif isinstance(other,Interactors):
            self.interactors.concat(other.interactors)
        return self
        

from .chart_class import ALXChart
@dataclass
class Interactor:
    generator: Generator
    response: Response  # Using string annotation for forward declaration

    def __add__(self, other):
        if isinstance(other,Interactor):
            return Interactors([self,other])
        elif isinstance(other,alt.TopLevelMixin):
            # cast altair chart as ALX chart as ALX cant handle signal generators
            chart = ALXChart(chart=other)
            return add_interactor(chart,self)
        elif isinstance(other,ALXChart):
            return add_interactor(other,self)
        elif isinstance(other, Interactors):
            return other + self
        
        

# brush = alt.selection_interval(encodings=['x'])
# generator = Generator(brush)
# response = (spec,generator) => highlight_brush(spec, generator)
# 
# by default selection store should just be params for a regualr selection object 



# TODO: go through and create some example interaction techniques for Interactors 
# TODO: create test infrastructure for a given Interactor and vis. 
# TODO Next: update the interactions.py (duplicate) to use this new structure, 
# TODO Next: verify all the same interaction techniques are transitioned over and still work
# TODO After: go through and set up signal generators. 



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


# Example: barchart hover highlight 

