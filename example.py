from metatransform import MetaTransform
import json

def pass_in_function(data=None, *args, **kwargs):
    # data = kwargs.get('data', None)
    return f"here's your data >>> {str(data)}"

def multiply_by_x(data=None, *args, **kwargs):
    # data = kwargs.get('data', None)
    x = kwargs.get('x', 0)
    return data * x

data = [
        {'v': 'b', 'c': 'd', 'x': {'a': 10}, 'y': {'b': [1,2,3,4], 'c': {'g':'h'}, 'd': {'word': 'yo', 'xx': 'no'}}}, 
        {'v': 'e', 'c': 'f', 'z': [{'x': 5, 'y': 10}, {'x': 20, 'y': 205}]}
    ]

routines = {
        'r1': [{'function': 'rrrr', 'value': 'routine 1 rrr'}], 
        'r2': [
            {'function': 'cc', 'map': {'_c': {'__modify': True}}, 'options': {'create': True}}, 
            {'function': 'deep', 'value': 'hellooooooo', 'map': {'x': {'__modify': True}}}
        ]
    }

transforms = [
        {'function': 'r1'},
        {'function': 'r2'},
        {'function': pass_in_function, 'map': {'v': {'__modify': True}}},
        {'function': multiply_by_x, 'map': {
                'z': [{
                    'x': {'__modify': True, 'x': 10},
                    'y': {'__modify': True, 'x': 5}
                }]
            }
        },
        {'function': 'whatver', 'options': {'my_opt1': 1, 'text': 'WORDDDDD???'}},
        {'function': 'flatten', 'map': {'y': {'b': {'__modify': True}, 'c': {'__modify': True}, 'd': {'__modify': True}}}}
    ]

x = MetaTransform(transforms=transforms, routines=routines)

x.run(data)

print(json.dumps(data, indent=4))