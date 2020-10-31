import boto3

def get_source_bucket(bucket, bucket_lookup):
    if not bucket_lookup:
        return bucket
    else:
        cf = boto3.client('cloudformation')
        next_token = None
        while True:
            if next_token is None:
                result = cf.list_exports()
            else:
                result = cf.list_exports(NextToken=next_token)
            x = [y for y in result['Exports'] if y['Name'] == bucket]
            if len(x) == 1:
                return x[0]['Value']
            if 'NextToken' not in result or result['NextToken'] is not None:
                print('done searching')
                break
            next_token = result['NextToken']
        raise Exception('no export named \'{}\' was found in this region'.format(bucket))
