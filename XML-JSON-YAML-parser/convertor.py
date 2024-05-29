import json
import yaml
import xmltodict
import os

CONVERSION_FUNCTIONS = {
    ".xml": {
        "json": lambda x: json.dumps(xmltodict.parse(x), indent=4),
        "yaml": lambda x: yaml.dump(xmltodict.parse(x), indent=4, sort_keys=False),
        "yml": lambda x: yaml.dump(xmltodict.parse(x), indent=4, sort_keys=False),

    },
    ".json": {
        "yaml": lambda x: yaml.dump(json.loads(x), indent=4),
        "yml": lambda x: yaml.dump(json.loads(x), indent=4),
        "xml": lambda x: xmltodict.unparse(json.loads(x), pretty=True),
    },
    ".yaml": {
        "json": lambda x: json.dumps(yaml.safe_load(x), indent=4),
        "xml": lambda x: xmltodict.unparse(json.loads(json.dumps(yaml.safe_load(x))), pretty=True),
    },
    ".yml": {
        "json": lambda x: json.dumps(yaml.safe_load(x), indent=4),
        "xml": lambda x: xmltodict.unparse(json.loads(json.dumps(yaml.safe_load(x))), pretty=True),
    }
}

def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower()

if __name__ == "__main__":

    input_file = input("Enter the path to the file: ")

    if not os.path.isfile(input_file):
        print("Error: File not found.")
    else:
        with open(input_file, "r") as file:
            data = file.read()

        input_format = get_file_extension(input_file)

        valid_output_formats = ["json", "yaml", "yml", "xml"]
        output_format = input("Enter the desired output format (json/yaml-yml/xml): ").lower()

        if output_format not in valid_output_formats:
            print("Invalid output format. Please choose between json, yaml, or xml.")
        else:
            if input_format not in CONVERSION_FUNCTIONS:
                print("Unsupported file format.")
            else:
                if output_format not in CONVERSION_FUNCTIONS[input_format]:
                    print(f"Conversion from '{input_format}' to '{output_format}' not supported.")
                else:
                    output_data = CONVERSION_FUNCTIONS[input_format][output_format](data)
                    output_file = os.path.splitext(input_file)[0] + "." + output_format

                    with open(output_file, "w") as outfile:
                        outfile.write(output_data)

                    print(f"'{input_file}' file converted and saved to '{output_file}' successfully.")
