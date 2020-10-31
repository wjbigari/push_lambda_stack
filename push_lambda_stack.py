import boto3
import argparse
from parse_parameters import parse_parameters
from get_bucket import get_source_bucket

parser = argparse.ArgumentParser('Create a Cloudformation Stack that includes a lambda push')

parser.add_argument('template', metavar='TEMPLATE LOCATION', help='the relative path to the tempalte file (valid yml or json) for the cloudformation stack')
parser.add_argument('bucket', metavar='LAMBDA SOURCE BUCKET', help='the bucket where the lambda source zip will be pushed')
parser.add_argument('-s', dest='stack_name', metavar='STACK NAME',help='the desired name of the cloud formation stack.  default = the lambda_name value')
parser.add_argument('-z', dest='lambda_source', metavar='LAMBDA SOURCE ZIP', help='the relative location of the function\'s source zip. default = \'./function.zip\'', default='./function.zip')
parser.add_argument('-k', help='the key destination for the lambda source zip. defaults to the lambda_name value with a \'.zip\' extension')
parser.add_argument('--param', metavar='PARAMETER {key} {value}', nargs=2, action='append', dest='parameters')
parser.add_argument('-p', metavar='PARAMETER {key}={value}', action='append', dest='parameters')
parser.add_argument('--iam', dest='capabilities', action='append_const', const='CAPABILITY_IAM')
parser.add_argument('--niam', dest='capabilities', action='append_const', const='CAPABILITY_NAMED_IAM')
parser.add_argument('-v', dest='version_id_key', metavar='VERSIONID PARAMETER KEY', help='the default parameter key for the s3 object versionId to pass to the cloudformation stack.  deafult = \'VersionId\'', default='VersionId')
parser.add_argument('--blup', action='store_true', help='a flag to indicate that the lambda source bucket should be fetched from cloudformation exports.  In this case the \'LAMBDA SOURCE BUCKET\' will be used as the desired export key')
args=parser.parse_args()

# get bucket name from cloudformation if neccessary 
bucket = get_source_bucket(args.bucket, args.blup)
print('bucket:', bucket)

#TODO push the zip file to the code bucket if necessary, returning version id
version_id = 'some_version'
print('version id:', version_id)

#build parameters
parameters = parse_parameters(args.parameters, args.version_id_key, version_id)
print('parameters:', parameters)

#TODO push stack
stack_id = 'some stack id'
print(stack_id)