def parse_parameters(params):
    param_list = []
    for item in params:
        if isinstance(item, str):
            try:
                split = item.split('=')
                param_list.append({
                    'ParameterKey': split[0],
                    'ParameterValue': split[1]
                })
            except:
                raise Exception('{} is not a valid parameter string.  should be of the format {{key}}={{value}}'.format(item))
        elif isinstance(item, list):
            param_list.append({
                 'ParameterKey': item[0],
                'ParameterValue': item[1]
            })
    return param_list