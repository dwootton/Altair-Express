class ALXChart():
    def __init__(self, *args, **kwargs):
        # Initialize the chart only if it hasn't been set previously.
        if not hasattr(self, 'chart') or self.chart is None:
            # Set the generators list to manage dynamic elements related to the chart
            object.__setattr__(self, "generators", [])
            # Extract the chart from kwargs or set to None if not provided
            chart = kwargs.pop('chart', None)
            object.__setattr__(self, "chart", chart)
        else:
            # If the chart is already set, indicate that reinitialization is not performed
            print("Skipping initialization as 'chart' is already set.")

    def to_dict(self):
        # Convert the chart to a dictionary representation using Altair's to_dict method
        return self.chart.to_dict()
    
    def __setattr__(self, name, value):
        # Custom attribute setting, managing chart and generators directly
        if name in ['chart', 'generators']:
            # Set specified attributes directly on the ALXChart instance
            object.__setattr__(self, name, value)
        elif hasattr(self.chart, name):
            # Delegate attribute setting to the chart if it's a chart attribute
            setattr(self.chart, name, value)
        else:
            # Use default behavior for any other attributes
            super().__setattr__(name, value)

    def __getattr__(self, name):
        # Custom attribute access method
        if name in self.__dict__:
            # Return attribute directly if it exists in the instance dictionary
            return self.__dict__[name]
        elif 'chart' in self.__dict__ and hasattr(self.__dict__['chart'], name):
            # If the attribute belongs to the chart, delegate access to the chart
            return getattr(self.__dict__['chart'], name)
        else:
            # Raise attribute error if the attribute is not found
            raise AttributeError(f"'ALXChart' object has no attribute '{name}'")

    def _repr_mimebundle_(self, include, exclude):
        # Return an empty MIME bundle; customization could be added for rich display in Jupyter
        return {}

    def __repr__(self) -> str:
        # Return a simple string representation
        return str()

    def _repr_html_(self):
        # Display method for HTML representation, typically used in Jupyter notebooks
        self.display()
        return str()

    def display(self):
        # Custom display logic to handle the visualization
        # Example patch data for demonstration purposes
        print('generators', self.generators)
        output_of_patch = [
            {"op": "add", "path": "/data/", "value": {"name": "element_store","values":[]}},
            {"op": "add", "path": "/data/-", "value": {"name": "activate_data","values":[]}}
        ]
        # Call the original display function with the patched output
        return self.chart.display(validate=False, renderer='svg', patch=output_of_patch)

    def compile_generators_to_patch(self, generators):
        # Logic to compile data patches from generators; this is a placeholder
        patches = []
        for generator in generators:
            # Assume each generator can contribute a part of the data patch
            part_of_patch = generator.generate_patch()
            patches.append(part_of_patch)
        return patches
    
class Response():
    
class Generator():
    def __init__(self, effect, action,options=None):
        self.effect = effect
        self.action = action
        self.options = options


    def __add__(self, other):
        #chart 
        if isinstance(other,Interaction):
            return Interactions([self,other])
        if isinstance(other,Interactions):
            return Interactions([self,other.interactions])
        return add_interaction(other,self)
    def __radd__(self, other):
        return self.__add__(other)

    def set_selection(self,selection):
        self.selection = selection

    def get_selection(self):
        return getattr(self,'selection',None)

def generators_to_patches(generators):
    # Function to compile data patches from generators; this is a placeholder
    patches = []
    for generator in generators:
        # Assume each generator can contribute a part of the data patch
        part_of_patch = generator.generate_patch()
        patches.append(part_of_patch)
    return patches
