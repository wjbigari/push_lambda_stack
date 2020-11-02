import boto3
import hashlib

BUFFER_SIZE = 4096

def get_version(bucket, key, source_path):
    s3 = boto3.resource('s3')
    file_exists = False
    try:
        obj = s3.Object(bucket, key)
        obj.load()
        file_exists = True
    except:
        print('file does not exist. pushing first version...')
    if file_exists: # pulled logic out of try catch for clearer logging in nested errors
        local_hash = ''
        remote_hash = ''
        with open(source_path, 'rb') as local:
            local_hash = get_hash(local)
        response = obj.get()
        remote_hash = get_hash(response['Body'])
        if remote_hash == local_hash:
            print('source is the same. not pushing a new version')
            return obj.version_id
        else:
            print('local source is different from remote. pushing new version...'.format(local_hash, remote_hash))
    with open(source_path, 'rb') as z:
        obj.upload_fileobj(z)
    obj.load()
    print('file pushed.')
    return obj.version_id

def get_hash(f):
    file_hash = hashlib.sha256()
    fb = f.read(BUFFER_SIZE)
    while len(fb) > 0:
        file_hash.update(fb)
        fb = f.read(BUFFER_SIZE)
    return file_hash.hexdigest()