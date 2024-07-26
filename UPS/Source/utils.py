def parse_config(cfg):
    ''' This function reads a config file
    in the format
    key: value
    It returns dictionary with the
    parameters included in the inputc config

    Parameters
    ---------
    cfg: string
        path to config file
    
    Returns
    -------
    data_dict: dictionary
             Dictionary containing
             the parameters declared
             in the input config
    '''
    # Initialize an empty dictionary
    data_dict = {}

    # Open the file for reading
    with open(cfg, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Strip whitespace from the line and split it into key and value
            key, value = line.strip().split(': ', 1)
            # Add the key-value pair to the dictionary
            data_dict[key] = value

    return data_dict
