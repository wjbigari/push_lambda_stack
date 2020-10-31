def parse_parameters(args, bucket, version_id):
    params = args.parameters
    param_list = []
    param_list.append({
                    'ParameterKey': args.version_id_key,
                    'ParameterValue': version_id
                })
    param_list.append({
                    'ParameterKey': args.source_key_parameter,
                    'ParameterValue': args.key
                })
    param_list.append({
                    'ParameterKey': args.source_bucket_parameter,
                    'ParameterValue': bucket
                }) 
    if params is None:
        return param_list                
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

def parse_tags(tags):
    tag_list = []
    if tags is None:
        return tag_list
    for item in tags:
        if isinstance(item, str):
            try:
                split = item.split('=')
                tag_list.append({
                    'Key': split[0],
                    'Value': split[1]
                })
            except:
                raise Exception('{} is not a valid parameter string.  should be of the format {{key}}={{value}}'.format(item))
        elif isinstance(item, list):
            tag_list.append({
                'Key': item[0],
                'Value': item[1]
            })
    return tag_list
