divCombinations = [
    [12],
    [3, 9],
    [6, 6],
    [3, 3, 6],
    [3, 6, 3],
]

rules = {
    'root': {'inOrder': True},
    'navbar': {'min': 0, 'max': 4},
    'container': {'min': 1, 'max': 3},
    'jumbotron': {'min': 2, 'max': 4},
    'row': {'combinations': divCombinations},
    'div-3': {'min': 2, 'max': 2},
    'div-6': {'min': 2, 'max': 3},
    'div-9': {'min': 2, 'max': 3},
    'div-12': {'min': 2, 'max': 2},
    'list-group': {'min': 2, 'max': 5},
    'card-div': {'inOrder': True},
    'card-body': {'inOrder': True},
    'footer': {'min': 1, 'max': 1},
}