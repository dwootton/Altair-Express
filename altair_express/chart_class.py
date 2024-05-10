import copy
import altair as alt
from .interactors import Adaptor
import json
def custom_serializer(obj):
    """Convert custom objects to a serializable format."""
    if isinstance(obj, alt.Parameter):
        # Assuming the Parameter class has attributes that can be serialized directly
        return {'name': obj.name, 'select': obj.select.to_dict()}  # Update according to actual attributes
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def dedupe_dicts(dict_list):
    seen = set()
    unique_dicts = []
    for d in dict_list:
        # Serialize the dictionary using the custom serializer for custom objects
        serialized_d = json.dumps(d, default=custom_serializer, sort_keys=True)
        if serialized_d not in seen:
            seen.add(serialized_d)
            unique_dicts.append(d)
    return unique_dicts

class ALXChart():
    def __init__(self, *args, **kwargs):
        self.generators = kwargs.pop('generators', [])
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
        return self.chart.to_dict(validate=False)
    
    def __or__(self,other):
        if isinstance(other,ALXChart):
            # deep clone this chart 
            copied_chart = self.chart.copy()
            #copy_chart = alt.Chart.from_json(dct=json, validate=False)

            new_chart = alt.hconcat(copied_chart, other.chart, validate=False).resolve_scale(y='independent',x='independent').resolve_axis(y='independent',x='independent')


            # merge generators 
            merged_generators = []
            # merge generators and de-dupe by "name" property 
            for generator in self.generators:
                if generator.name not in [g.name for g in merged_generators]:
                    merged_generators.append(generator)
            
            for generator in other.generators:
                if generator.name not in [g.name for g in merged_generators]:
                    merged_generators.append(generator)

            new_alx=  ALXChart(chart=new_chart, generators=merged_generators)
            return new_alx

    def __add__(self, other):
        # if an interactor is added 
        if isinstance(other,ALXChart):
            # deep clone this chart 
            copied_chart = self.chart.copy()
            #copy_chart = alt.Chart.from_json(dct=json, validate=False)

            new_chart = alt.layer(copied_chart, other.chart, validate=False)

            # merge generators 
            merged_generators = []
            # merge generators and de-dupe by "name" property 
            for generator in self.generators:
                if isinstance(generator,Adaptor):
                    if generator.input.name not in [g.name for g in merged_generators]:
                        merged_generators.append(generator.input)

                if generator.name not in [g.name for g in merged_generators]:
                    merged_generators.append(generator)
            
            for generator in other.generators:
                if isinstance(generator,Adaptor):
                    if generator.input.name not in [g.name for g in merged_generators]:
                        merged_generators.append(generator.input)
                if generator.name not in [g.name for g in merged_generators]:
                    merged_generators.append(generator)

            new_alx=  ALXChart(chart=new_chart, generators=merged_generators)
            return new_alx
            

           


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
            return getattr(self.__dict__['chart'], name,None)
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
        new_patches, params = self.compile_generators(self.generators)

        patches = []

        # for each param, add_params 
        for param in params:
            self.chart = self.chart.add_params(param)

        if str(self.chart.params) =="Undefined":
            patches.append({
                "path": "/signals",
                "op": "add",
                "value": []
            })
        

        patches.extend(new_patches)
       

        #print("full chart",self.chart.to_dict(validate=False))
        # Call the original display function with the patched output
        return self.chart.display(validate=False, renderer='svg', patch=patches)

    def compile_generators(self, generators):
        # Logic to compile data patches from generators; this is a placeholder
        patches = []
        params = []


        for generator in generators:
            # Assume each generator can contribute a part of the data patch
            if(isinstance(generator.listener,alt.Parameter)):
                params.append(generator.listener)
            
            if(isinstance(generator,Adaptor)):
                patches_to_add, params_to_add = generator.compile_adaptor()
                patches.extend(patches_to_add)
                params.extend(params_to_add)


            if(not isinstance(generator.listener,alt.Parameter)):
                part_of_patch = generator.generate_patch()
                patches.extend(part_of_patch)
                        

        # TODO FIX: de dupe any patches smartly, right now it just removes the last one
        patches = dedupe_dicts(patches)
        params = dedupe_dicts(params)


        return patches, params
    

