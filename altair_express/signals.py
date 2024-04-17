from typing import Optional, Union, List, Any
from enum import Enum
import json
from .utils import to_recursive_dict 
# Assuming other types like OnEvent, Expr, Binding, Stream are defined somewhere as Python classes.
# If not, they are just named as is.

class SignalRef:
    def __init__(self, signal: str):
        self.signal = signal

class BaseSignal:
    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None):
        self.name = name
        self.description = description
        self.on = on

class PushSignal(BaseSignal):
    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None):
        super().__init__(name, description, on)
        self.push = 'outer'


    
class Serializable:
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
    
class NewSignal(Serializable, BaseSignal):
    def __init__(self, name: str, description: Optional[str] = None, on: Optional[List['OnEvent']] = None, value: Optional['SignalValue'] = None, react: Optional[bool] = None, update: Optional['Expr'] = None, bind: Optional['Binding'] = None):
        super().__init__(name, description, on)
        self.value = value
        self.react = react
        self.update = update
        self.bind = bind
        

class InitSignal(BaseSignal):
    def __init__(self, name: str, init: 'Expr', description: Optional[str] = None, on: Optional[List['OnEvent']] = None, value: Optional['SignalValue'] = None,  bind: Optional['Binding'] = None):
        super().__init__(name, description, on)
        self.value = value
        self.init = init
        self.bind = bind

Signal = Union[NewSignal, InitSignal, PushSignal]  # This is how you represent TypeScript's type union in Python
SignalValue = Any  # In Python, 'any' is represented as 'Any' from the 'typing' module

class EventListener:
    def __init__(self, scale: Optional[str] = None, stream: Optional['Stream'] = None, signal_ref: Optional[SignalRef] = None):
        self.scale = scale
        self.stream = stream
        self.signal_ref = signal_ref  # Example of how to handle union types differently


EventSelector = str
Events = Union[EventSelector, EventListener]  # Another example of a union type

class Expr:
    def __init__(self, expr: str):
        self.expr = expr

class ExprRef:
    def __init__(self, expr: Expr):
        self.expr = expr

# Define SignalRef as previously done
class SignalRef:
    def __init__(self, signal: str):
        self.signal = signal

# Update type including Expr, ExprRef, SignalRef, and a dict type for value
Update = Union[Expr, ExprRef, SignalRef, dict]

class OnEvent(Serializable):
    def __init__(self, events: Union['Events', List['EventListener']], encode: Optional[str] = None, update: Optional[Update] = None,  force: Optional[bool] = None):
        self.encode = encode
        self.update = update
        self.events = events
        self.force = force

# Binding and related classes/interfaces
class BindBase:
    def __init__(self, element: Optional[str] = None, debounce: Optional[int] = None, name: Optional[str] = None):
        self.element = element
        self.debounce = debounce
        self.name = name

class BindInput(BindBase):
    def __init__(self, element: Optional[str] = None, debounce: Optional[int] = None, name: Optional[str] = None, input: Optional[str] = None, placeholder: Optional[str] = None, autocomplete: Optional[str] = None):
        super().__init__(element, debounce, name)
        self.input = input
        self.placeholder = placeholder
        self.autocomplete = autocomplete

class BindCheckbox(BindBase):
    def __init__(self, element: Optional[str] = None, debounce: Optional[int] = None, name: Optional[str] = None):
        super().__init__(element, debounce, name)
        self.input = 'checkbox'

class BindRadioSelect(BindBase):
    def __init__(self, options: List[Any], element: Optional[str] = None, debounce: Optional[int] = None, name: Optional[str] = None, labels: Optional[List[str]] = None):
        super().__init__(element, debounce, name)
        self.input = 'radio'  # default to radio, can be set to 'select' explicitly
        self.options = options
        self.labels = labels

class BindRange(BindBase):
    def __init__(self, element: Optional[str] = None, debounce: Optional[int] = None, name: Optional[str] = None, min: Optional[int] = None, max: Optional[int] = None, step: Optional[int] = None):
        super().__init__(element, debounce, name)
        self.input = 'range'
        self.min = min
        self.max = max
        self.step = step


class BindDirect:
    def __init__(self, element: Union[str, 'EventTarget'], event: Optional[str] = 'input', debounce: Optional[int] = None):
        self.element = element
        self.event = event
        self.debounce = debounce

# Union type for Binding
Binding = Union[BindCheckbox, BindRadioSelect, BindRange, BindInput, BindDirect]

class EventTarget:
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


class StreamParameters:
    def __init__(self, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        self.between = between
        self.marktype = marktype
        self.markname = markname
        self.filter = filter
        self.throttle = throttle
        self.debounce = debounce
        self.consume = consume

class EventStream(Serializable,StreamParameters):
    def __init__(self, source=None, type=None, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.source = source
        self.type = type

class DerivedStream(StreamParameters):
    def __init__(self, stream, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.stream = stream

class MergedStream(StreamParameters):
    def __init__(self, merge, between=None, marktype=None, markname=None, filter=None, throttle=None, debounce=None, consume=None):
        super().__init__(between, marktype, markname, filter, throttle, debounce, consume)
        self.merge = merge

Stream = Union[EventStream, DerivedStream, MergedStream]