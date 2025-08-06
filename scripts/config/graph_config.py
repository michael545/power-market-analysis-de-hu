# scripts/config/graph_config.py
#proof of conecept for now

NEIGHBORS = {
    # original with updated neighbors
    'FR': ['DE_LU', 'BE'],
    'DE_LU': ['FR', 'BE', 'PL', 'CZ', 'AT', 'NL'],
    'PL': ['DE_LU', 'CZ', 'SK'],
    'CZ': ['DE_LU', 'PL', 'SK', 'AT'],
    'SK': ['PL', 'CZ', 'HU', 'AT'],
    'HU': ['SK', 'AT', 'HR', 'SI', 'RO'],
    'AT': ['DE_LU', 'CZ', 'SK', 'HU', 'SI'],
    
    # new added
    'BE': ['FR', 'DE_LU', 'NL'],
    'NL': ['DE_LU', 'BE'],
    'SI': ['AT', 'HU', 'HR'],
    'HR': ['HU', 'SI'],
    'RO': ['HU', 'BG'],
    'BG': ['RO'],
}

# goegraphy (latitude, longitude) for plots 
NODE_POSITIONS = {
    # Original nodes
    'DE_LU': (51.1657, 10.4515),
    'HU': (47.1625, 19.5033),
    'FR': (46.6033, 1.8883),
    'PL': (51.9194, 19.1451),
    'CZ': (49.8175, 15.4730),
    'SK': (48.6690, 19.6990),
    'AT': (47.5162, 14.5501),
    'BE': (50.5039, 4.4699),
    'SI': (46.1512, 14.9955),
    'NL': (52.1326, 5.2913),
    'HR': (45.1, 15.2),

    'RO': (45.9432, 24.9668),
    'BG': (42.7339, 25.4858),
}