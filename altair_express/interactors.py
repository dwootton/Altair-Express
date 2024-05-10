from dataclasses import dataclass, field
from typing import Union, Callable, List, Any, Dict, Optional
from .signals import Signal, Expr
import altair as alt 
from pydantic import BaseModel, Field



@dataclass
class Processor(BaseModel):
    name: str
    expr: Expr

@dataclass
class Store:
    # This will be a base class for specific types of stores
    pass


from enum import Enum

class StoreTypes(Enum):
    Selection = "Selection" # any vegalite selection
    Parameter = "Parameter"
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


# class SelectionParameter(BaseModel):
#     test:str

class Listener(BaseModel) : Union[alt.SelectionParameter, Signal]

# these generator classes will be the internal data representation for an interactor. 

# above will be generator factories that generate the correct generators from some spec 
    # brush() generator will take in the chart, etc and then produce the interval selection generator
    # datum_click() generator will take in the chart, etc and then produce the point selection generator

# well this should specify the properties of a selection
# specific selection details should be abstracted away. but some details might matter
# class Listener(BaseModel) : Union[SelectionParameter, Signal]
from typing import Literal, Sequence

@dataclass
class SelectionParameter(BaseModel) : 
        name: Optional[str]
        select: Union[
            dict,  Literal["point", "interval"], 
        ] 
        bind: Optional[Union[str, dict]]
        value: Optional[Union[
            str,
            bool,
            dict,
            None,
            float,
            Sequence[Union[dict]],
        ]]


class Generator(BaseModel):
    name: str
    #listener: Listener
    listener: Union[Signal,alt.SelectionParameter, alt.Parameter] = Field(..., description="Can be either SelectionParameter or Signal")
    value: Union[str,Expr] # Expr that evaluates to the store type
    type: StoreTypes
    processors: List[Processor]
    """Class to handle different types of generators for interaction techniques."""
    def __init__(self, listener, name = "generator", value = "", processors = [],  type_param=None):
        init_data = {
            "name": name,
            "value": value,
            "processors": processors if processors is not None else [],
            "type": type_param,
            "listener": listener
        }
        if hasattr(listener,'param_type') and listener['param_type'] =='select':
            #listener.name = "selection_" + name  # ensure name is consistent 
            init_data["value"] = listener.name #+ "_tuple"
            init_data["type"] = StoreTypes.Selection
        # Properly initialize Pydantic model
        super().__init__(**init_data)


    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types

    def __add__(self, other):
        # TODO: allow for multiple generators to be merged into a single generator, and the stores to be updated appropriately
        # if isinstance(other, Generator):
        #     return Interactor(self, other) # merge into multiple generators, each should then be piped to through 
        if isinstance(other, Response):
            return Interactor(generator=self, response=other)
        return NotImplemented

    def __repr__(self):
        return f"{self.__dict__}"
    
    def generate_patch(self):
        patches = []

        # add the listener as a signal
        patches.append({"op":"add","path":f"/signals/-","value":self.listener.to_recursive_dict()})

        for processor in self.processors:
            patches.append({"op":"add","path":f"/signals/-","value":{"name":processor.name,"value":processor.expr}})
        

        patches.append({"op":"add","path":f"/signals/-","value":{"name":self.name+"_store","value":self.value}})

        return patches
        
        # add the listener as a signal
        # add each value in processor as signal 
        # then add value as signal with name = self.name+"_store"



        # use JSON patch
        


@dataclass
class ResponseParameters(BaseModel):
    # Additional parameters for response function
    params: Dict[str, Any] = field(default_factory=dict)

class Response(BaseModel):
    responseFn: Callable[[alt.Chart, 'Generator', 'ResponseParameters'], alt.Chart]
    params: Optional[Dict[str, Any]] = Field(default=None, description="Parameters for a response function")

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
    
    # Commenting out as we should move all generator compilation down
    # if not isinstance(interactor.generator.listener,alt.Parameter): # is listener 
    #     # custom generator, must be added to the chart later 
    #     chart.add_generator(interactor.generator)
    # else: 
    #     # selection generator, add to the chart directly 
    #     chart.chart=chart.chart.add_params(interactor.generator.listener)

    chart.add_generator(interactor.generator)
    changed_chart = chart.chart.copy(deep=True)
    changed_chart = interactor.response.responseFn(changed_chart, interactor.generator, interactor.response.params)
    chart.chart = changed_chart
    return chart

# adaptors should take in a input_technique and then produce a signal, with an update that corresponds to evaluate the input to 
# a given (adapted) output 
class Adaptor(BaseModel):
    def __init__(self, input, name, params=None):
        self.input = input
        self.params = params
        self.update = input.name
        self.name = name
        # this should have all of the same properties as a generator, but should be a signal that is updated by the input technique

    # if any function is called on adaptor that is not defined, then it should be passed to the input technique
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return getattr(self.input, name)

    def compile_adaptor(self):
        input_patches =[]
        params = []

        if(not isinstance(self.input.listener,alt.Parameter)):
            input_patches = self.input.generate_patch()
        else: 
            params = [self.input.listener]

        input_patches.append({"op":"add","path":f"/signals/-","value":{"name":self.name,"update":self.update}})
        return input_patches,params
    
    def __repr__(self):
        return f"{self.__dict__}"


        




class Interactors(BaseModel): 
    interactors: List['Interactor']

    def __add__(self, other):
        if isinstance(other,alt.TopLevelMixin):
            # if added to a nonalx chart convert to ALX chart
            chart = ALXChart(chart=other)
            print('self',self)
            
            for interactor in self.interactors:
                chart = add_interactor(chart,interactor)
            return chart
        #chart 
        if isinstance(other,Interactor):
            self.interactors.append(other)
        elif isinstance(other,Interactors):
            self.interactors.concat(other.interactors)
        return self



from .chart_class import ALXChart
class Interactor(BaseModel):
    generator: Generator
    response: Response  # Using string annotation for forward declaration

    def __add__(self, other):
        if isinstance(other,Interactor):
            return Interactors(interactors=[self,other])
        elif isinstance(other,alt.TopLevelMixin):
            # cast altair chart as ALX chart as ALX cant handle signal generators
            alx_chart = ALXChart(chart=other)
            return add_interactor(alx_chart,self)
        elif isinstance(other,ALXChart):
            return add_interactor(other,self)
        elif isinstance(other, Interactors):
            return other + self
        
        

# brush = alt.selection_interval(encodings=['x'])
# generator = Generator(brush)
# response = (spec,generator) => highlight_brush(spec, generator)
# 
# by default selection store should just be params for a regualr selection object 
# from .signals import OnEvent
# listen = Signal(
#     name="zoom",
#     value=10,
#     on=[OnEvent(
#         events=["wheel"],
#         update="zoom + event.deltaY",
#         force=True
#     )]
# )
# Generator(listener=listen, name="zoom_store", value="zoom", type=StoreTypes.Numeric)

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

