import boto3
import argparse
from parse import parse_parameters, parse_tags
from get_bucket import get_source_bucket
from push_source import get_version
from push_stack import push_stack

parser = argparse.ArgumentParser('Create a Cloudformation Stack that includes a lambda push')

parser.add_argument('template', help='the relative path to the tempalte file (valid yml or json) for the cloudformation stack')
parser.add_argument('bucket', help='the bucket where the lambda source zip will be pushed')
parser.add_argument('key', help='the key destination for the lambda source zip')
parser.add_argument('stack',help='the desired name of the cloud formation stack')
parser.add_argument('-z', dest='lambda_source', metavar='LAMBDA SOURCE ZIP', help='the relative location of the function\'s source zip. default = \'./function.zip\'', default='./function.zip')
parser.add_argument('--param', help='PARAMETER {key} {value}', nargs=2, action='append', dest='parameters')
parser.add_argument('-p', metavar='PARAMETER {key}={value}', action='append', dest='parameters')
parser.add_argument('--iam', dest='capabilities', action='append_const', const='CAPABILITY_IAM')
parser.add_argument('--niam', dest='capabilities', action='append_const', const='CAPABILITY_NAMED_IAM')
parser.add_argument('--aa', dest='capabilities', action='append_const', const='CAPABILITY_AUTO_EXPAND')
parser.add_argument('-v', dest='version_id_key', metavar='VERSIONID PARAMETER KEY', help='override the version id parameter key name that is passed into the cloudformation stack. default: \'VersionId\'', default='VersionId')
parser.add_argument('--blup', action='store_true', help='a flag to indicate that the lambda source bucket should be fetched from cloudformation exports.  In this case the \'LAMBDA SOURCE BUCKET\' will be used as the desired export key')
parser.add_argument('-k', dest='source_key_parameter', default='SourceKey', help='override the source key parameter key name that is passed into the cloudformation stack. default: \'SourceKey\'')
parser.add_argument('-b', dest='source_bucket_parameter', default='SourceBucket', help='override the source bucket parameter key name that is passed into the cloudformation stack. default: \'SourceBucket\'')
parser.add_argument('-t', dest='tags', action='append', help='stack tags.  {key}={value}')
parser.add_argument('--tag', dest='tags', action='append', nargs=2, help='stack tags.  {key} {value}')
args=parser.parse_args()

# get bucket name from cloudformation if neccessary 
bucket = get_source_bucket(args.bucket, args.blup)
print('bucket:', bucket)

#push the zip file to the code bucket if necessary, returning version id
version_id = get_version(bucket, args.key, args.lambda_source)
print('version id:', version_id)

#build parameters
parameters = parse_parameters(args, bucket, version_id)
tags = parse_tags(args.tags)
print('parameters:', parameters)
print('tags:', tags)

#push stack
stack_id = push_stack(args.stack, args.template, parameters, args.capabilities, tags)
print('stack id:', stack_id)