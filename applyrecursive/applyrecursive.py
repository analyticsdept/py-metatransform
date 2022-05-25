#!/usr/bin/env python

from functools import reduce

class ApplyRecursive():
    """
    Iterate recursively through a map and iterable until a trigger condition is met, then call a function

    `func` the function to call

    `func_args` tuple of positional arguments to pass to the function

    `func_kwargs` dictionary of keyword arguments to pass to the function

    `func_kwargs_data` name of the function's data input keyword argument

    @Version: 1.0
    @Author: Rob (analyticsdept)
    @Links: https://github.com/analyticsdept

    """

    def __init__(self, func, func_args=None, func_kwargs=None, func_kwargs_data=None) -> None:
        self.func = func
        self.func_args = func_args if func_args != None else ()
        self.func_kwargs = func_kwargs if func_kwargs != None else {}
        self.func_kwargs_data = func_kwargs_data
    
    def apply(self, map, trigger, iterable, create=False):
        """
        Recurse through the iterable until trigger condition is met, then call the function passed in the constructor

        `Map` should follow the structure of the expected iterable

        `Trigger` should match a key in the `Map` structure

        `Iterable` should be an iterable of `list` or `dict` type

        `Create` will create fields that don't exist
        """

        def recurse(map, trigger, iterable, create):

            if iterable == None:
                try: return self.logic(map, trigger, iterable)
                except: return iterable

            elif isinstance(iterable, list):
                if isinstance(map, list):
                    recurse(map[0], trigger, iterable, create)
                elif trigger in map.keys():
                    return self.logic(map, trigger, iterable)
                else:
                    for idx, item in enumerate(iterable):
                        if isinstance(map, dict):
                            iterable[idx] = recurse(map, trigger, iterable[idx], create)
                        elif isinstance(map, list):
                            recurse(map[0], trigger, iterable[idx], create)

            elif isinstance(iterable, dict):
                if trigger in map.keys():
                    return self.logic(map, trigger, iterable)
                else:
                    for idx, item in map.items():
                        if idx in iterable.keys():
                            iterable[idx] = recurse(map[idx], trigger, iterable[idx], create)
                        elif create:
                            iterable[idx] = recurse(map[idx], trigger, iterable, create)
                        else: continue

            elif not {list, dict} <= {type(iterable)} and isinstance(map, dict):
                return self.logic(map, trigger, iterable)

            return iterable

        return recurse(map, trigger, iterable, create)

    def logic(self, map, trigger, data):
        """
        Run the function on the data

        `map` the mapping object (merged into keyword arguments passed to the function)

        `trigger` field that triggers the modification

        `data` payload to be modified
        """
        if trigger in map.keys():
            _kwargs = {self.func_kwargs_data: data}
            _kwargs = {**_kwargs, **self.func_kwargs, **map}
            return self.func(*self.func_args, **_kwargs)