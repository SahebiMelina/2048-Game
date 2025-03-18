def load_data(filename='data.txt'):
    game_data = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                key, value = line.strip().split(': ')
                game_data[key] = value if not value.isdigit() else int(value)
        return game_data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return {}
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return {}

def save_data(filename='data.txt', data=None):
    if data is None:
        data = {}
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for key, value in data.items():
                file.write(f'{key}: {value}\n')  # Added newline character
        print(f'Data saved successfully to {filename}!')
    except Exception as e:
        print(f"Error saving data: {str(e)}")                 


