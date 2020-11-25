import boto3
import time
import uuid

def push_stack(stack_name, template, parameters, capabilities, tags):
    cf = boto3.client('cloudformation')
    stack_exists = False
    try:
        description = cf.describe_stacks(StackName=stack_name)
        print('stack exists. id: {}.  attempting to update', description['Stacks'][0]['StackId'])
        stack_exists = True
    except:
        print('stack does not exist. attempting to create...')
    with open(template, 'r') as template:
            template_body = template.read()
    if capabilities is None:
        capabilities = []
    if stack_exists:
        change_set_name = stack_name + '-' + str(uuid.uuid4()).replace('-','')
        print('creating change set with name: {}'.format(change_set_name))
        create_change_response = cf.create_change_set(ChangeSetName=change_set_name,StackName=stack_name, TemplateBody=template_body, Parameters=parameters, Capabilities=capabilities, Tags=tags)
        changeset = cf.describe_change_set(ChangeSetName=create_change_response['Id'])
        while changeset['Status'] == 'CREATE_PENDING' or changeset['Status'] == 'CREATE_IN_PROGRESS':
            time.sleep(5)
            changeset = cf.describe_change_set(ChangeSetName=create_change_response['Id'])
        if changeset['Status'] == 'FAILED':
            # boy I wish there were error codes...
            if changeset['StatusReason'] == 'The submitted information didn\'t contain changes. Submit different information to create a change set.':
                print('the stack is already up to date! no changes made')
                cf.delete_change_set(ChangeSetName=create_change_response['Id'])
            else:
                print('failed to update the stack:', changeset['StatusReason'])
                cf.delete_change_set(ChangeSetName=create_change_response['Id'])
                raise Exception('failed to update the stack: {}'.format(changeset['StatusReason']))
        else:
            try:
                cf.execute_change_set(ChangeSetName=create_change_response['Id'])
            except Exception:
                updated_set = cf.describe_change_set(ChangeSetName=create_change_response['Id'])
                print('failed to execute change. change status:', updated_set['Status'])
                raise
            updated_set = cf.describe_change_set(ChangeSetName=create_change_response['Id'])
            print('change status:', updated_set['Status'])
            status = None
            status_reason = None
            while status is None or status.endswith('IN_PROGRESS'):
                time.sleep(10)
                description = cf.describe_stacks(StackName = stack_name)
                status = description['Stacks'][0]['StackStatus']
                if 'StackStatusReason' in description['Stacks'][0]:
                    status_reason = description['Stacks'][0]['StackStatusReason']
                print('stack status:', status)
            if status != 'UPDATE_COMPLETE':
                raise Exception(status_reason, 'Check Cloudformation for more information')
            print('stack updated!')
        return create_change_response['StackId']
    else:
        response = cf.create_stack(StackName=stack_name, TemplateBody=template_body, Parameters=parameters, Capabilities=capabilities, Tags=tags)
        print('created stack!')
        status = None
        status_reason = None
        while status is None or status.endswith('IN_PROGRESS'):
            time.sleep(10)
            description = cf.describe_stacks(StackName = stack_name)
            status = description['Stacks'][0]['StackStatus']
            if 'StackStatusReason' in description['Stacks'][0]:
                    status_reason = description['Stacks'][0]['StackStatusReason']
            print('stack status:', status)
        if status != 'CREATE_COMPLETE':
            raise Exception(status_reason, 'Check Cloudformation for more information')
        return response['StackId']