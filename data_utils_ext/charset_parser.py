# charset_parser.py
import data_preprocess_options
import os

def parse_charset(charset_path, char_type):
    parsed_data = []
    try:
        charset_path = os.path.abspath(charset_path) if not os.path.isabs(charset_path) else charset_path
        
        with open(charset_path, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) == 4:
                    unicode_val, decimal_val, char_name, char = parts
                    if char_type == 'uni':
                        parsed_data.append(unicode_val)
                    elif char_type == 'dec':
                        parsed_data.append(decimal_val)
                    elif char_type == 'name':
                        parsed_data.append(char_name)
                    elif char_type == 'char':
                        parsed_data.append(char)
                    else:
                        parsed_data.append(parts)
    except FileNotFoundError:
        print(f"Error: The file {charset_path} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
    
    # print(parsed_data)
    return parsed_data

def main():
    parser = data_preprocess_options.get_data_preprocess_options()
    opts = parser.parse_args()

    parsed_data = parse_charset(opts.charset_path, opts.char_type)

if __name__ == "__main__":
    main()
