import tkinter as tk

root = tk.Tk()

COLS_COUNT = 4

STATES_COLORS = dict({
    'gut': 'green',
    'schlecht': 'red',
    'repair': 'yellow'
})


def create_grid_from_list(data):
    """
    Creates a multi-dimensional array from a flat array,
    used for visualizing a grid
    :param data: One dimensional array
    :return: Multi dimensional array
    """
    rows = (len(data) // COLS_COUNT) + 1
    values = []
    for i in range(rows):
        values.append([])
        for j in range(COLS_COUNT):
            index = i * COLS_COUNT + j
            if index >= len(data):
                break
            if data[index]['state']:
                values[i].append(data[index])
            else:
                values[i].append(data[index])
    return values


def start_grid_vis(data):
    """
    Function to create grid and start tkinter
    :param data: One dimensional array with results from classifier
    :return: None
    """
    values = create_grid_from_list(data)
    for i in range(len(values)):
        for j in range(len(values[i])):
            state = values[i][j]['state']
            meta = values[i][j]['tool']
            button = tk.Button(root, text=state, bg=STATES_COLORS[state], padx=40, pady=40)
            button.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
    root.mainloop()


def start_grid_vis_val(data, real_data):
    """
    Function to create grid and start tkinter
    :param data: One dimensional array with results from classifier
    :return: None
    """
    values = create_grid_from_list(data)
    label = tk.Label(root, text='Predictions').grid(row=0, sticky="ew")
    for i in range(len(values)):
        for j in range(len(values[i])):
            state = values[i][j]['state']
            meta = values[i][j]['tool']
            button = tk.Button(root, text=str(i + 1), bg=STATES_COLORS[state], padx=40, pady=40)
            button.grid(row=i + 1, column=j, padx=10, pady=10, sticky="nsew")
    real_values = create_grid_from_list(real_data)
    label = tk.Label(root, text='Labels').grid(row=len(values), sticky="ew")
    for i in range(len(real_values)):
        for j in range(len(real_values[i])):
            state = real_values[i][j]['state']
            meta = real_values[i][j]['tool']
            button = tk.Button(root, text=str(i + 1 + len(real_values)), bg=STATES_COLORS[state], padx=40, pady=40)
            button.grid(row=i + 1 + len(real_values), column=j, padx=10, pady=10, sticky="nsew")
    root.mainloop()
