import os
os.chdir('C:/Users/lenovo/Desktop/Game 2048')
def load_data():
    filename = 'data.txt'

    file_info = {}
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.strip().split('=', 1)
                file_info[key.strip()] = value.strip()
        return file_info
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found!")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
data = load_data()
print("Loaded data:", data)
