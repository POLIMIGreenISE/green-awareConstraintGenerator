import yaml
from collections import defaultdict

# Parse the yaml infrastructure file
def handleInfrastructure(yamlFile):
    # Open the file
    with open(yamlFile, "r") as file:
        data = yaml.safe_load(file)

    # Parse the dictionary
    def parseNestedDict(data, parent_key=""):
        fields = []
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                fields.extend(parseNestedDict(value, full_key))
            else:
                fields.append((full_key, value))
        return fields

    fields = parseNestedDict(data['nodes'])

    # Initialize defaultdict
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()

    # Populate the dictionary
    for field_name, field_value in fields:
        keys = field_name.split('.')
        d = data
        for key in keys[:-1]:
            d = d[key]
        d[keys[-1]] = field_value

    # Convert back to a regular dict
    data = dict(data)
    return data