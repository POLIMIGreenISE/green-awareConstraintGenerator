import yaml
from collections import defaultdict

# Parse the infrastructure file
def prepareInfrastructure(yamlFile):
    with open(yamlFile, "r") as file:
        data = yaml.safe_load(file)

    def parseNestedDict(data, parent_key=""):
        fields = []
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                # Recursively parse nested dictionaries
                fields.extend(parseNestedDict(value, full_key))
            else:
                # Append key and value as a tuple
                fields.append((full_key, value))
        return fields

    fields = parseNestedDict(data['nodes'])

    # Initialize a nested defaultdict
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()

    # Populate the nested dictionary
    for field_name, field_value in fields:
        keys = field_name.split('.')  # Split the field name into hierarchical levels
        d = data
        for key in keys[:-1]:  # Traverse and create intermediate levels
            d = d[key]
        d[keys[-1]] = field_value  # Set the final key's value

    # Convert back to a regular dict (optional)
    data = dict(data)
    return data