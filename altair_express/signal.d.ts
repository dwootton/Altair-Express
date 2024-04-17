export interface SignalRef {
    signal: string;
  }
  export interface BaseSignal {
    name: string;
    description?: string;
    on?: OnEvent[];
  }
  export interface PushSignal extends BaseSignal {
    push: 'outer';
  }
  export interface NewSignal extends BaseSignal {
    value?: SignalValue;
    react?: boolean;
    update?: Expr;
    bind?: Binding;
  }
  export interface InitSignal extends BaseSignal {
    value?: SignalValue;
    init: Expr;
    bind?: Binding;
  }
  export type Signal = NewSignal | InitSignal | PushSignal;
  export type SignalValue = any;

  export type EventListener =
  | SignalRef
  | {
      scale: string;
    }
  | Stream;
  
export type EventSelector = string;
export type Events = EventSelector | EventListener;

export type Update =
  | Expr
  | ExprRef
  | SignalRef
  | {
      value: SignalValue;
    };
export type OnEvent = (
  | {
      encode: string;
    }
  | {
      update: Update;
    }
) & {
  events: Events | EventListener[];
  force?: boolean;
};


// EXPRESSION

export type Expr = string;
export interface ExprRef {
  expr: Expr;
}


// BINDING
export type Element = string;
export interface BindBase {
  /**
   * An optional CSS selector string indicating the parent element to which
   * the input element should be added. By default, all input elements are
   * added within the parent container of the Vega view.
   */
  element?: Element;
  /**
   * If defined, delays event handling until the specified milliseconds have
   * elapsed since the last event was fired.
   */
  debounce?: number;
  /**
   * By default, the signal name is used to label input elements.
   * This `name` property can be used instead to specify a custom
   * label for the bound signal.
   */
  name?: string;
}
export interface BindInput extends BindBase {
  /**
   * The type of input element to use.
   * The valid values are `"checkbox"`, `"radio"`, `"range"`, `"select"`,
   * and any other legal [HTML form input type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input).
   */
  input?: string;
  /**
   * Text that appears in the form control when it has no value set.
   */
  placeholder?: string;
  /**
   * A hint for form autofill.
   * See the [HTML autocomplete attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete) for additional information.
   */
  autocomplete?: string;
}
export interface BindCheckbox extends BindBase {
  input: 'checkbox';
}
export interface BindRadioSelect extends BindBase {
  input: 'radio' | 'select';
  /**
   * An array of options to select from.
   */
  options: any[];
  /**
   * An array of label strings to represent the `options` values. If
   * unspecified, the `options` value will be coerced to a string and
   * used as the label.
   */
  labels?: string[];
}
export interface BindRange extends BindBase {
  input: 'range';
  /**
   * Sets the minimum slider value. Defaults to the smaller of the signal value and `0`.
   */
  min?: number;
  /**
   * Sets the maximum slider value. Defaults to the larger of the signal value and `100`.
   */
  max?: number;
  /**
   * Sets the minimum slider increment. If undefined, the step size will be
   * automatically determined based on the `min` and `max` values.
   */
  step?: number;
}
export interface BindDirect {
  /**
   * An input element that exposes a _value_ property and supports the
   * [EventTarget](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget)
   * interface, or a CSS selector string to such an element. When the element
   * updates and dispatches an event, the _value_ property will be used as the
   * new, bound signal value. When the signal updates independent of the
   * element, the _value_ property will be set to the signal value and a new
   * event will be dispatched on the element.
   */
  element: Element | EventTarget;
  /**
   * The event (default `"input"`) to listen for to track changes on the
   * external element.
   */
  event?: string;
  /**
   * If defined, delays event handling until the specified milliseconds have
   * elapsed since the last event was fired.
   */
  debounce?: number;
}
export type Binding = BindCheckbox | BindRadioSelect | BindRange | BindInput | BindDirect;


// EVENT STREAMS
export type EventSource = EventStream['source'] & {};
export type EventType =
  | 'click'
  | 'dblclick'
  | 'dragenter'
  | 'dragleave'
  | 'dragover'
  | 'keydown'
  | 'keypress'
  | 'keyup'
  | 'mousedown'
  | 'mousemove'
  | 'mouseout'
  | 'mouseover'
  | 'mouseup'
  | 'mousewheel'
  | 'pointerdown'
  | 'pointermove'
  | 'pointerout'
  | 'pointerover'
  | 'pointerup'
  | 'timer'
  | 'touchend'
  | 'touchmove'
  | 'touchstart'
  | 'wheel';
export type WindowEventType =
  | EventType
  // TODO: change to `keyof HTMLBodyElementEventMap` after vega/ts-json-schema-generator#192
  | string;


  export type MarkType =
  | 'arc'
  | 'area'
  | 'image'
  | 'group'
  | 'line'
  | 'path'
  | 'rect'
  | 'rule'
  | 'shape'
  | 'symbol'
  | 'text'
  | 'trail';


export interface StreamParameters {
  between?: Stream[];
  marktype?: MarkType;
  markname?: string;
  filter?: Expr | Expr[];
  throttle?: number;
  debounce?: number;
  consume?: boolean;
}
export type EventStream = StreamParameters &
  (
    | {
        source?: 'view' | 'scope';
        type: EventType;
      }
    | {
        source: 'window';
        type: WindowEventType;
      }
  );
export interface DerivedStream extends StreamParameters {
  stream: Stream;
}
export interface MergedStream extends StreamParameters {
  merge: Stream[];
}
export type Stream = EventStream | DerivedStream | MergedStream;