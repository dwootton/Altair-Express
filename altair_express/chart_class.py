class ALXChart():
    def __init__(self, *args, **kwargs):
        self.generators = []
        chart = kwargs.pop('chart', None)

        self.chart = chart
        super().__init__(*args, **kwargs)
      
        # # Initialize the chart only if it hasn't been set previously.
        # if not hasattr(self, 'chart') or self.chart is None:
        #     # Set the generators list to manage dynamic elements related to the chart
        #     object.__setattr__(self, "generators", [])
        #     # Extract the chart from kwargs or set to None if not provided
        #     chart = kwargs.pop('chart', None)
        #     object.__setattr__(self, "chart", chart)
        #     print('set chart',chart)
            
        # else:
        #     # If the chart is already set, indicate that reinitialization is not performed
        #     print("Skipping initialization as 'chart' is already set.")

    def add_generator(self, generator):
        # Add a generator to the list of generators
        self.generators.append(generator)

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
        if name == 'chart':
            # Return the chart attribute directly
            return self.__dict__['chart']
        elif name == 'generators':
            # Return the generators attribute directly
            return self.__dict__['generators']
        else:   
            return getattr(self.__dict__['chart'], name)
        # # Custom attribute access method
        # if name in self.__dict__:
        #     # Return attribute directly if it exists in the instance dictionary
        #     return self.__dict__[name]
        # elif 'chart' in self.__dict__ and hasattr(self.__dict__['chart'], name):
        #     # If the attribute belongs to the chart, delegate access to the chart
            
        # else:
        #     # Raise attribute error if the attribute is not found
        #     raise AttributeError(f"'ALXChart' object has no attribute '{name}'")

    def _repr_mimebundle_(self, include, exclude):
        # Return an empty MIME bundle; customization could be added for rich display in Jupyter
        return {}

    def __repr__(self) -> str:
        # Return a simple string representation
        #self.display()
        return str()

    def _repr_html_(self):
        # Display method for HTML representation, typically used in Jupyter notebooks
        self.display()
        return str()

    def display(self):
        # Custom display logic to handle the visualization
        # Example patch data for demonstration purposes
        new_patches = self.compile_generators_to_patch(self.generators)
        patches = [{
            "path": "/signals",
            "op": "add",
            "value": []
        }]
        patches.extend(new_patches)
        # Call the original display function with the patched output
        return self.chart.display(validate=False, renderer='svg', patch=patches)

    def compile_generators_to_patch(self, generators):
        # Logic to compile data patches from generators; this is a placeholder
        patches = []

        print('generators',generators)

        for generator in generators:
            # Assume each generator can contribute a part of the data patch
            part_of_patch = generator.generate_patch()

            # flatten the append patches 
            patches.extend(part_of_patch)

        return patches
    

