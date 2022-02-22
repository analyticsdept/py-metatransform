import json
from functools import reduce

class MetaTransform():
    """
    Transform methods class
    """
    def __init__(self):
        pass

    def transform(self, data, chain, subroutines = {}):

        _data = data if isinstance(data, list) else [data]

        try:
            results = [self.run_transform_chain(__data, chain, subroutines) for __data in _data]
        except Exception as e: raise Exception(f'{type(e).__name__} :: {str(e)}')
        else:
            _merged = []
            _targets = []
            _results = list(filter(None, results))
            for _d in _results:
                if isinstance(_d, dict):
                    _data = _d.get('data', _d)
                    _target_list = _d.get('targets', [])
                    if isinstance(_data, list):
                        for d in _data:
                            _merged.append(d)
                    else:
                        _merged.append(_data)
                    _targets += _target_list
                else:
                    _merged = _d
            _return = {"data": _merged, "targets": _targets}
            return _return

    def run_transform_chain(self, input, chain, subroutines = {}):

        try: subroutine_keys = {k: idx for idx, k in enumerate([list(routine.keys())[0] for routine in subroutines])}
        except: subroutine_keys = []

        for transform in chain:

            transform_key = list(transform.keys())[0] if type(transform) == dict else transform
            
            if transform_key == "chain":
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.run_transform_chain(input[idx], transform[transform_key], subroutines)
                    else: input = self.run_transform_chain(input, transform[transform_key], subroutines)
                except Exception as e: raise Exception(f"could not run subchain: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "process_by_field_value":
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.process_by_field_value(input[idx], transform[transform_key], subroutines, subroutine_keys)
                    else: input = self.process_by_field_value(input, transform[transform_key], subroutines, subroutine_keys)
                except Exception as e: raise Exception(f"could not run subchain: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "process_by_field_key":
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.process_by_field_key(input[idx], transform[transform_key], subroutines, subroutine_keys)
                    else: input = self.process_by_field_key(input, transform[transform_key], subroutines, subroutine_keys)
                except Exception as e: raise Exception(f"could not run subchain: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "type_cast": # Only done during remapping - remove
                try: input = self.type_cast(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not cast: {type(e).__name__} >> {str(e)}")
                else: continue

            if transform_key == "remap_fields":
                data = input
                try:
                    if type(input) == list:
                        data = []
                        for idx, value in enumerate(input):
                            data.append(self.remap_fields(input[idx], transform[transform_key]))
                        input = data
                    else: input = self.remap_fields(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not remap: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "filter_subset":
                try:
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.filter_subset(input[idx], transform[transform_key])
                    else: input = self.filter_subset(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not filter: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "filter_subset_blacklist":
                try:
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.filter_subset_blacklist(input[idx], transform[transform_key])
                    else: input = self.filter_subset_blacklist(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not filter: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "flatten":
                _delimiter = transform[transform_key].get('delimiter', "_-_") if isinstance(transform[transform_key], dict) else transform[transform_key]
                _exclude = transform[transform_key].get('exclude', []) if isinstance(transform[transform_key], dict) else []
                _include = transform[transform_key].get('include', []) if isinstance(transform[transform_key], dict) else []
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.flatten_dict(input[idx], delimiter=_delimiter, exclude=_exclude, include=_include)
                    else: 
                        input = self.flatten_dict(input, delimiter=_delimiter, exclude=_exclude, include=_include)
                except Exception as e: raise Exception(f"could not flatten: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "filter_field_value":
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = input[idx] if self.filter_field_value(input[idx], transform[transform_key]) else None
                    else: input = input if self.filter_field_value(input, transform[transform_key]) else None
                except Exception as e: raise Exception(f"could not filter: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: 
                    if input:
                        if type(input) == list:
                            input = list(filter(None, input))
                        continue 
                    else:
                        break

            if transform_key == "lift_value":
                try: 
                    if type(input) == list:
                        data = []
                        for idx, value in enumerate(input):
                            data.append(self.lift_value(input[idx], transform[transform_key]))
                        input = data
                    else: input = self.lift_value(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not lift value: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "key_value_collapse":
                try:
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            input[idx] = self.key_value_collapse(input[idx], transform[transform_key])
                    else: input = self.key_value_collapse(input, transform[transform_key])
                except Exception as e: raise Exception(f"could not collapse: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "unnest_to_row":
                try:
                    if type(input) == list:
                        _input = []
                        for idx, value in enumerate(input):
                            _unnest = self.unnest_to_row(input[idx], transform[transform_key])
                            if _unnest and _unnest != []:
                                _input.append(_unnest)
                            else: 
                                _input.append(value)
                        input = _input
                    else:
                        _unnest = self.unnest_to_row(input, transform[transform_key])
                        if _unnest and _unnest != []:
                            input = _unnest
                except Exception as e: raise Exception(f"could not unnest to row: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key in subroutine_keys:
                try: input = self.run_transform_chain(input, subroutines[subroutine_keys[transform_key]][transform_key], subroutines)
                except Exception as e: raise Exception(f"could not run subroutine: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: continue

            if transform_key == "set_target_by_field_value":
                _targets = []
                try: 
                    if type(input) == list:
                        for idx, value in enumerate(input):
                            result = self.set_target_output(input[idx], transform[transform_key])
                            _targets.append(result)
                    else: 
                        result = self.set_target_output(input, transform[transform_key])
                        _targets.append(result)
                except Exception as e: raise Exception(f"could not run subchain: {type(e).__name__} >> {str(e)} ({transform_key})")
                else: 
                    return {"data": input, "targets": _targets}

        return input

    def lowercase(self, input):
        if type(input) == str:
            return input.lower()
        else:
            return None

    def uppercase(self, input):
        if type(input) == str:
            return input.upper()
        else:
            return None

    def cast_bool(self, input):
        try: _bool = bool(input)
        except: return None
        else: return _bool

    def cast_string(self, input):
        """
        Return string, or empty string if not possible
        """
        if type(input) in [str, int, float]:
            return str(input)
        elif type(input) == list:
            return ",".join((str(value) for value in input))
        elif type(input) == dict:
            return str(",".join([f"{key}:{input[key]}" for key in input]))
        elif type(input) == bool:
            return self.lowercase(str(input))
        else:
            return str()

    def cast_int(self, input):
        """
        Return integer, or empty integer if not possible
        """
        if type(input) in (str, int, float, bool):
            try: integer = int(input)
            except: return None
            else: return integer
        else:
            return int()

    def cast_float(self, input):
        if type(input) in (str, int, float, bool):
            try: integer = float(input)
            except: return None
            else: return integer
        else:
            return None

    def cast_list(self, input, delimiter = None):
        if delimiter:
            try: _list = input.split(delimiter)
            except: return [input]
            else: return _list
        else:
            return [input]

    def cast_dict(self, input, list_delimiter = None, key_delimiter = None):
        if type(input) == dict:
            return input
        if list_delimiter and key_delimiter:
            try: _dict = {k:v for (k,v) in (item.split(key_delimiter) for item in [item for item in input.split(list_delimiter)])}
            except: return {}
            else: return _dict
        if list_delimiter and not key_delimiter:
            try: _dict = {k:v for (k,v) in enumerate(input.split(","))}
            except: return {}
            else: return _dict
        if type(input) == list:
            try: _dict = {k:v for (k,v) in enumerate(input)}
            except: return {}
            else: return _dict
        if type(input) in [str, int, float, bool]:
            return {"0": input}

    def type_cast(self, input, type):
        if type == "string":
            return self.cast_string(input)
        elif type == "int":
            return self.cast_int(input)
        elif type == "float":
            return self.cast_float(input)
        elif type == "bool":
            return self.cast_bool(input)
        elif type == "list":
            return self.cast_list(input)
        elif type == "dict":
            return self.cast_dict(input)
        else:
            return input

    def remap_fields(self, data, _map):
        def remap(data, _map):
            _nmap = json.loads(json.dumps(_map))
            if isinstance(data, dict) and isinstance(_map, dict):
                for k in _nmap.keys():
                    if isinstance(_nmap[k], dict):
                        if '_name' in _nmap[k].keys() and k in data.keys():
                            data[_map[k]['_name']] = data[k] if '_type' not in _nmap[k].keys() else self.type_cast(data[k], _nmap[k]['_type'])
                            del data[k]
                            _map_path = _nmap[k]['_name']
                            _map[_map_path] = _map.pop(k)
                            del _map[_map_path]['_name']
                        elif '_type' in _nmap[k].keys() and k in data.keys():
                            data[k] = self.type_cast(data[k], _nmap[k]['_type'])
                        elif '_default' in _nmap[k].keys() and k not in data.keys():
                            data[k] = _nmap[k].get('_default', None)
                            
            _event = json.loads(json.dumps(data))
            if isinstance(_event, dict) and isinstance(_map, dict):
                for key in _event.keys():
                    if key in _map:
                        if isinstance(_map[key], dict):
                            remap(data[key], _map[key])
                        else:
                            data[_map[key]] = data[key]
                            del data[key]

            if isinstance(_event, list):
                for index, item in enumerate(_event):
                    _locked_map = json.loads(json.dumps(_map))
                    remap(data[index], _locked_map['_list'] if '_list' in _locked_map else _locked_map)

        _data = json.loads(json.dumps(data))
        __map = json.loads(json.dumps(_map))
        remap(_data, __map)
        return _data
        
    def filter_subset(self, input, subset):
        if type(input) == list:
            return [{key:value for key, value in item.items() if key in subset} for item in input]
        elif type(input) == dict:
            return {key:value for key, value in input.items() if key in subset}
        else:
            return input

    def flatten_dict(self, input, path = None, delimiter = "_-_", exclude = [], include = []):
        def build_path(path, next_path):
            if path != None:
                return f"{path}{delimiter}{str(next_path)}"
            else:
                return str(next_path)
        flattened = {}
        if type(input) == list:
            if len(input) > 0:
                for idx, item in enumerate(input):
                    if item in exclude:
                        flattened[path] = item
                        continue
                    if len(include) > 0 and item not in include:
                        flattened[path] = item
                        continue
                    if type(input) == list or type(input) == dict:
                        flattened.update(self.flatten_dict(item, build_path(path, idx), delimiter))
                    else:
                        flattened[path] = item
            else:
                flattened[path] = []
        elif type(input) == dict:
            if len(input.keys()) > 0:
                for key, value in input.items():
                    if key in exclude:
                        flattened[key] = value
                        continue
                    if len(include) > 0 and key not in include:
                        flattened[key] = value
                        continue
                    flattened.update(self.flatten_dict(value, build_path(path, key), delimiter))
            else:
                flattened[path] = {}
        else:
            flattened[path] = input
        return flattened

    def filter_field_value(self, input, field):
        def _filter(input, field):
            if type(input) not in (dict, list) and type(field) not in (dict, list):
                if input == field:
                    return True
                else:
                    return False
            elif type(input) == dict and type(field) == dict:
                if "_filter" in field.keys():
                    list_results = []
                    for key in field['_filter']:
                        if key in input:
                            list_results.append(self.filter_field_value(input[key], field['_filter'][key]))
                    return reduce((lambda x, y: x * y), list_results)
                else:
                    for key in field.keys():
                        if key in input:
                            return self.filter_field_value(input[key], field[key])
            elif type(input) == list:
                list_results = []
                for idx, value in enumerate(input):
                    if type(field) == list:
                        list_results.append(self.filter_field_value(input[idx], field[0]))
                    else:
                        list_results.append(self.filter_field_value(input[idx], field))
                return True if True in list_results else False
            else:
                return False

        if type(field) == list:
            list_results = []
            for idx, value in enumerate(field):
                list_results.append(_filter(input, field[idx]))
            return reduce((lambda x, y: x * y), list_results)
        else: return _filter(input, field)

    def process_by_field_value(self, input, transform, subroutines = {}, subroutine_keys = {}):
        def test(input, field, value):
            if type(input) == dict and type(field) == dict:
                for key in field.keys():
                    if key in input:
                        return test(input[key], field[key], value)
            elif type(input) == dict and type(field) not in (dict, list):
                if field in input:
                    return test(input[field], field, value)
            elif type(input) == list:
                for idx, value in enumerate(input):
                    if type(field) == list:
                        return test(input[idx], field[0], value)
                    else:
                        return test(input[idx], field, value)
            if type(input) not in (dict, list) and type(field) not in (dict, list):
                if input == value:
                    return True
                else:
                    return False
        
        values = {idx: key['value'] for idx, key in enumerate([value for value in transform['values']])}

        for idx, value in enumerate(values.values()):
            if test(input, transform['field'], value):
                if "subroutine" in transform['values'][idx]:
                    chain = transform['values'][idx]['subroutine'] if type(transform['values'][idx]['subroutine']) == list else [transform['values'][idx]['subroutine']]
                else:
                    chain = None

                if chain != None and chain != []:
                    result = self.run_transform_chain(
                        input, 
                        chain, 
                        subroutines
                    )
                else:
                    result = input
                return result

            if value == "*":
                return input

    def process_by_field_key(self, input, transform, subroutines = {}, subroutine_keys = {}):
        def test(input, field, value):
            if type(input) == dict and type(field) == dict:
                for key in field.keys():
                    if key in input:
                        return test(input[key], field[key], value)
            # elif type(input) == dict and type(field) not in (dict, list):
            #     if field in input:
            #         return test(input[field], field, value)
            elif type(input) == list:
                for idx, value in enumerate(input):
                    if type(field) == list:
                        return test(input[idx], field[0], value)
                    else:
                        return test(input[idx], field, value)
            if isinstance(input, dict) and (isinstance(field, str) or isinstance(field, set)):
                field = list(field)[0] if isinstance(field, set) else field
                if field in input:
                    return True
                else:
                    return False
        
        values = {idx: key['value'] for idx, key in enumerate([value for value in transform['values']])}

        for idx, value in enumerate(values.values()):
            if test(input, transform['field'], value):
                if "subroutine" in transform['values'][idx]:
                    chain = transform['values'][idx]['subroutine'] if type(transform['values'][idx]['subroutine']) == list else [transform['values'][idx]['subroutine']]
                else:
                    chain = None

                if chain != None and chain != []:
                    result = self.run_transform_chain(
                        input, 
                        chain, 
                        subroutines
                    )
                else:
                    _result = input
                return result

            if value == "*":
                return input

    def set_target_output(self, input, transform):
        def test(input, field, value):
            if type(input) == dict and type(field) == dict:
                for key in field.keys():
                    if key in input:
                        return test(input[key], field[key], value)
            elif type(input) == dict and type(field) not in (dict, list):
                if field in input:
                    return test(input[field], field, value)
            elif type(input) == list:
                for idx, value in enumerate(input):
                    if type(field) == list:
                        return test(input[idx], field[0], value)
                    else:
                        return test(input[idx], field, value)
            if type(input) not in (dict, list) and type(field) not in (dict, list):
                if input == value:
                    return True
                else:
                    return False
        
        values = {idx: key['value'] for idx, key in enumerate([value for value in transform['values']])}

        for idx, value in enumerate(values.values()):
            if test(input, transform['field'], value):
                return transform['values'][idx]['target'] if 'target' in transform['values'][idx] else None
            if value == "*":
                return transform['values'][idx]['target'] if 'target' in transform['values'][idx] else None

    def filter_subset_blacklist(self, input, subset):
        if type(input) == list:
            return [{key:value for key, value in item.items() if key not in subset} for item in input]
        elif type(input) == dict:
            return {key:value for key, value in input.items() if key not in subset}
        else:
            return input

    def unnest_to_row(self, input, field):
        def get_items(input, field):
            if isinstance(input, dict) and isinstance(field, dict):
                for key in field.keys():
                    if key in input:
                        return get_items(input[key], field[key])
            if isinstance(input, list) and isinstance(field, list):
                for idx, item in enumerate(input):
                    return get_items(input[idx], field[0])
            if isinstance(input, dict) and (isinstance(field, str) or isinstance(field, set)):
                field = list(field)[0] if isinstance(field, set) else field
                if field in input:
                    return input.pop(field)

        def insert_items(input, item, field):
            if isinstance(input, dict) and isinstance(field, dict):
                for key in field.keys():
                    if key in input:
                        return insert_items(input[key], item, field[key])
            if isinstance(input, list) and isinstance(field, list):
                for idx, _item in enumerate(input):
                    return insert_items(input[idx], item, field[0])
            if isinstance(input, dict) and (isinstance(field, str) or isinstance(field, set)):
                field = list(field)[0] if isinstance(field, set) else field
                if field in input and isinstance(input[field], list):
                    input[field] = item
                else: input[field] = input[field]

        _input = json.loads(json.dumps(input))
        
        items = get_items(_input, field)
        if items is not None and items != None:
            _rows = []
            for item in items:
                _input = json.loads(json.dumps(input))
                insert_items(_input, item, field)
                _rows.append(_input)
            return _rows
        else:
            return []

    def lift_value(self, input, field):
        def lift(input, field):
            _input = json.loads(json.dumps(input))
            if isinstance(_input, dict) and isinstance(field, dict):
                for key in field.keys():
                    if key in _input.keys():
                        if isinstance(field[key], dict) and "_lift" in field[key]:
                            input[key] = _input[key][field[key]["_lift"]]
                            # _lift_field = _input.get(key, {}).get(field[key]["_lift"], None)
                            # if isinstance(_lift_field, str):
                            #     input[key] = _input[key][_lift_field] if _lift_field in _input[key].keys() else None
                            # if isinstance(_lift_field, list):
                            #     _lift_values = [_input[key][_field] for _field in _lift_field if _field in _input[key].keys()]
                            #     _lift_values = ''.join(list(filter(None, _lift_values)))
                            #     input[key] = _lift_values
                            #     print("I[k]: ", input[key], _lift_values, _lift_field)
                        else:
                            lift(input[key], field[key])
            elif isinstance(_input, list) and isinstance(field, list):
                for idx, item in enumerate(_input):
                    lift(input[idx], field[0])
        
        _input = json.loads(json.dumps(input))
        _field = json.loads(json.dumps(field))
        lift(_input, _field)
        return _input

    def key_value_collapse(self, input, transform):
        def get_value(input, path):
            def _get_value(input, path, output=[]):
                if isinstance(input, dict) and isinstance(path, dict):
                    for key in path:
                        if key in input:
                            _get_value(input[key], path[key], output)
                if isinstance(input, list) and isinstance(path, list):
                    for idx, value in enumerate(input):
                        _get_value(input[idx], path[0], output)
                if isinstance(input, dict) and (isinstance(path, str) or isinstance(path, set)):
                    field = list(path)[0] if isinstance(path, set) else path
                    if field in input:
                        output.append(input.pop(field))
            output = []
            _get_value(input, path, output)
            return output

        def insert(input, path, data, has_target = True):
            if isinstance(input, dict) and isinstance(path, dict):
                for key in path:
                    if key in input:
                        return insert(input[key], path[key], data, has_target)
                    else:
                        input[key] = {}
                        return insert(input[key], path[key], data)
            if isinstance(input, list) and isinstance(path, list):
                for idx, value in enumerate(input):
                    return insert(input[idx], path[0], data, has_target)
            if isinstance(input, dict) and (isinstance(path, str) or isinstance(path, set)):
                field = list(path)[0] if isinstance(path, set) else path
                if field != "*":
                    if field in input:
                        if isinstance(input[field], dict) and isinstance(data, dict):
                            input[field] = {**input[field], **data}
                        elif isinstance(input[field], list) and isinstance(data, list):
                            input[field].update(data)
                        else:
                            input[field] = data
                    elif has_target == False:
                        input.update(data)
                    else:
                        input[field] = data
                else:
                    input.update(data)

        f_key = transform.get("key_field", None)
        f_target = transform.get("target_field", None)
        f_val = transform.get("value_field", None)

        keys = get_value(input, f_key)
        values = get_value(input, f_val)
        data = {key: value for (key, value) in zip(keys, values)}
        if f_target:
            insert(input, f_target, data)
        else:
            insert(input, f_key, data, False)
        return input
