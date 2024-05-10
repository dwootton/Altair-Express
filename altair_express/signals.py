from typing import Optional, Union, List, Any,Sequence
from enum import Enum
import json
from .utils import to_recursive_dict 
from pydantic import BaseModel, Field
# Assuming other types like OnEvent, Expr, Binding, Stream are defined somewhere as Python classes.
# If not, they are just named as is.

class SignalRef(BaseModel):
    def __init__(self, signal: str):
        self.signal = signal

class BaseSignal(BaseModel):
    name: Optional[str]
    on : Optional[List['OnEvent']]
    description: Optional[str]

    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None):
        self.name = name
        self.description = description
        self.on = on

class PushSignal(BaseSignal,BaseModel):
    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None):
        super().__init__(name, description, on)
        self.push = 'outer'


    
class Serializable(BaseModel):
    def to_dict(self):
        return self.__dict__
    
    def to_recursive_dict(self):
        # recurse through all keys (except for self) and then continue to recurse until the entire object is 
        return to_recursive_dict(self)

    def to_json(self):
        print('in tojson~!')
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)
    
    def __repr__(self) -> str:
        return str(self.to_dict())
        
from dataclasses import dataclass


@dataclass
class Signal(Serializable, BaseSignal, BaseModel):
    name:Optional[str]
    value: Optional[Union[
            str,
            bool,
            dict,
            None,
            float,
            Sequence[Union[dict]],
            
        ]]
    update: Optional[str]
    bind : Optional[Union['BindCheckbox', 'BindRadioSelect', 'BindRange', 'BindInput', 'BindDirect']] = Field(..., description="Can be either SelectionParameter or Signal")
    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None, value: Optional['SignalValue'] = None, react: Optional[bool] = None, update: Optional['Expr'] = None, bind: Optional['Binding'] = None):
        super().__init__(name, description, on)
        self.value = value
        self.react = react
        self.update = update
        self.bind = bind
        

class InitSignal(BaseSignal,BaseModel):
    def __init__(self, name: str, init: 'Expr', description: Optional[str] = None, on: Optional[List['OnEvent']] = None, value: Optional['SignalValue'] = None,  bind: Optional['Binding'] = None):
        super().__init__(name, description, on)
        self.value = value
        self.init = init
        self.bind = bind

#class Signal(BaseModel) : NewSignal#[NewSignal, InitSignal, PushSignal]  # This is how you represent TypeScript's type union in Python
SignalValue = Any  # In Python, 'any' is represented as 'Any' from the 'typing' module

class EventListener(BaseModel):
    scale: Optional[str]
    stream: Optional['EventStream'] # TODO BUG: fix this to be proper Stream
    signal_ref: Optional[SignalRef]

    def __init__(self, scale: Optional[str] = None, stream: Optional['EventStream'] = None, signal_ref: Optional[SignalRef] = None):
        self.scale = scale
        self.stream = stream
        self.signal_ref = signal_ref  # Example of how to handle union types differently


class EventSelector(BaseModel) : str
#class Events(BaseModel) : Union[EventSelector, EventListener]  # Another example of a union type

class Expr(BaseModel):
    def __init__(self, expr: str):
        self.expr = expr

class ExprRef(BaseModel):
    def __init__(self, expr: Expr):
        self.expr = expr

# Define SignalRef as previously done
class SignalRef(BaseModel):
    def __init__(self, signal: str):
        self.signal = signal

# Update type including Expr, ExprRef, SignalRef, and a dict type for value
class Update(BaseModel) : Union[Expr, ExprRef, SignalRef, dict]

#class Events(BaseModel) : Union[EventSelector, EventListener] = Field(..., description="Can be either EventSelector or  EventListener") # Another example of a union type

class OnEvent(Serializable,BaseModel):
    events : Union[EventSelector, EventListener, List['EventListener']] = Field(..., description="Can be either SelectionParameter or Signal")
    encode : Optional[str]
    update : str
    force : Optional[bool]

    # def __init__(self, **kwargs, events: Union[EventSelector, EventListener, List['EventListener']], encode: Optional[str] = None, update: Optional[Update] = None,  force: Optional[bool] = None):
    #     super().__init__(**data)
    #     self.encode = encode
    #     self.update = update
    #     self.events = events
    #     self.force = force


# Binding and related classes/interfaces
# Base model class for common binding properties
class BindBase(BaseModel):
    element: Optional[str] = None
    debounce: Optional[int] = None
    name: Optional[str] = None

# Inherits from BindBase and adds additional properties specific to input fields
class BindInput(BindBase):
    input: Optional[str] = None
    placeholder: Optional[str] = None
    autocomplete: Optional[str] = None

# Inherits from BindBase and sets a fixed input type for checkboxes
class BindCheckbox(BindBase):
    input: str = 'checkbox'

# Inherits from BindBase and adds properties for radio/select input types
class BindRadioSelect(BindBase):
    input: str = 'radio'  # default to radio, can be explicitly set to 'select'
    options: List[str]
    labels: Optional[List[str]] = None

# Inherits from BindBase and adds properties specific to range inputs
class BindRange(BindBase):
    input: str = 'range'
    min: Optional[int] = None
    max: Optional[int] = None
    step: Optional[int] = None

# A direct bind model that might be used for simpler binding without inheritance
class BindDirect(BaseModel):
    element: Union[str, 'EventTarget']
    event: Optional[str] = 'input'
    debounce: Optional[int] = None

# Union type for Binding
class Binding(BaseModel) : Union[BindCheckbox, BindRadioSelect, BindRange, BindInput, BindDirect]

class EventTarget(BaseModel):
    # DOM EventTarget class
    pass

class EventType(Enum):
    CLICK = 'click'
    DBLCLICK = 'dblclick'
    DRAGENTER = 'dragenter'
    DRAGLEAVE = 'dragleave'
    DRAGOVER = 'dragover'
    KEYDOWN = 'keydown'
    KEYPRESS = 'keypress'
    KEYUP = 'keyup'
    MOUSEDOWN = 'mousedown'
    MOUSEMOVE = 'mousemove'
    MOUSEOUT = 'mouseout'
    MOUSEOVER = 'mouseover'
    MOUSEUP = 'mouseup'
    MOUSEWHEEL = 'mousewheel'
    POINTERDOWN = 'pointerdown'
    POINTERMOVE = 'pointermove'
    POINTEROUT = 'pointerout'
    POINTEROVER = 'pointerover'
    POINTERUP = 'pointerup'
    TIMER = 'timer'
    TOUCHEND = 'touchend'
    TOUCHMOVE = 'touchmove'
    TOUCHSTART = 'touchstart'
    WHEEL = 'wheel'

class WindowEventType(Enum):
    # This is a simplification, assuming other window event types are strings
    # In practice, this could be dynamically generated or modified to suit specific needs.
    OTHER = 'other'

class MarkType(Enum):
    ARC = 'arc'
    AREA = 'area'
    IMAGE = 'image'
    GROUP = 'group'
    LINE = 'line'
    PATH = 'path'
    RECT = 'rect'
    RULE = 'rule'
    SHAPE = 'shape'
    SYMBOL = 'symbol'
    TEXT = 'text'
    TRAIL = 'trail'


class StreamParameters(BaseModel):
    def __init__(self, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        self.between = between
        self.marktype = marktype
        self.markname = markname
        self.filter = filter
        self.throttle = throttle
        self.debounce = debounce
        self.consume = consume

class EventStream(Serializable,StreamParameters,BaseModel):
    source: str
    type: str
    between: Optional[List['EventStream']]
    marktype: Optional[str]
    markname: Optional[str]
    filter: Optional[Union[Expr,List[Expr]]] = Field(...,description="Can be singular or multiple expressions")
    throttle: Optional[int]
    debounce: Optional[int]

    def __init__(self, source=None, type=None, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.source = source
        self.type = type

class DerivedStream(StreamParameters,BaseModel):
    def __init__(self, stream, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.stream = stream

class MergedStream(StreamParameters,BaseModel):
    def __init__(self, merge, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.merge = merge

class Stream(BaseModel): Union[EventStream, DerivedStream, MergedStream]