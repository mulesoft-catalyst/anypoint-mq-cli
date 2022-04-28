import click
import time
import os
import requests
import json
import os
from requests.exceptions import HTTPError
import memcache


###### COMMANDS #####

@click.group()
def cli():
    """
    Simple CLI for managing queues, exchange, and fifo queues in Anypoint MQ
    """
    pass


@cli.command()
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
def search(username, password, region, orgId, envId):
    """This search and return queues, exchanges, fifo queues corresponding to the given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations to AMQ Rest API ####
    destinations_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations'
    payload = {}
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    try:
        destinations = requests.request(
        "GET", destinations_request_url, headers=headers, data=payload)
        destinations.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    queues = []
    for value in destinations.json():
        queues.append(
            {   
                "name": value.get('queueId') if value.get('queueId') != None else value.get('exchangeId'),
                "fifo": value.get('fifo') if value.get('fifo') != None else False,
                "exchange": True if value.get('type') == 'exchange' else False
            }
        )
    
    print(json.dumps(queues))

@cli.command(name="find-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
def findQueue(username, password, region, orgId, envId, name):
    """This command will try to find a queue in a given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations to AMQ Rest API ####
    destinations_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/queues/' + name
    payload = {}
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    try:
        destinations = requests.request(
        "GET", destinations_request_url, headers=headers, data=payload)
        destinations.raise_for_status()

        print(json.dumps({   
            "exists": True,
            "message": name + " already exists"
        }))
    except HTTPError as http_err:
        if http_err.response.status_code == 404:
           print(json.dumps({   
                "exists": False,
                "message": name + " does not exist"
            }))
        else:
            raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))

@cli.command(name="find-exchange")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
def findExchange(username, password, region, orgId, envId, name):
    """This command will try to find an exchange in a given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations to AMQ Rest API ####
    destinations_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/exchanges/' + name
    payload = {}
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    try:
        destinations = requests.request(
        "GET", destinations_request_url, headers=headers, data=payload)
        destinations.raise_for_status()

        print(json.dumps({   
            "exists": True,
            "message": name + " already exists"
        }))
    except HTTPError as http_err:
        if http_err.response.status_code == 404:
           print(json.dumps({   
                "exists": False,
                "message": name + " does not exist"
            }))
        else:
            raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))

    

@cli.command(name="create-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
@click.option('--fifo', 'fifo', help='Specifies if it is a FIFO queue', required=False, default=False, type=bool)
#@click.option('--exchange', 'exchange', help='Specifies if it is an Exchange queue', required=False, default=False)
@click.option('--ttl', 'ttl', help='Specifies TTL configuration in ms', required=False, default=120000)
@click.option('--lock-ttl', 'lockTtl', help='Specifies Lock TTL configuration in ms', required=False, default=10000)
@click.option('--encrypted', 'encrypted', help='Specifies if queue is encrypted', required=False, default=False)
@click.option('--dead-letter-queue', 'deadLetterQueue', help='Specifies the name of the DLQ', required=False)
@click.option('--max-attempts', 'maxAttempts', help='Specifies the max deliveries attempts before DLQ redirection', required=False)
@click.option('--delivery-delay', 'deliveryDelay', help='Specifies the delivery delay time in ms', required=False)
def createQueue(username, password, region, orgId, envId, name, fifo, ttl, lockTtl, encrypted, deadLetterQueue, maxAttempts, deliveryDelay):
    """This command creates a queue (standard or FIFO) in the given region, org id and environment id """
    #### Anypoint login ####
    token = login(username, password)
### Updated by Geovani to invoke Util function instead to implement it here ####
    createQueue_util(token, region, orgId, envId, name, fifo, ttl, lockTtl, encrypted, deadLetterQueue, maxAttempts, deliveryDelay)    

    
@cli.command(name="update-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
@click.option('--fifo', 'fifo', help='Specifies if it is a FIFO queue', required=False, default=False, type=bool)
#@click.option('--exchange', 'exchange', help='Specifies if it is an Exchange queue', required=False, default=False)
@click.option('--ttl', 'ttl', help='Specifies TTL configuration in ms', required=False, default=120000)
@click.option('--lock-ttl', 'lockTtl', help='Specifies Lock TTL configuration in ms', required=False, default=10000)
@click.option('--encrypted', 'encrypted', help='Specifies if queue is encrypted', required=False, default=False)
@click.option('--dead-letter-queue', 'deadLetterQueue', help='Specifies the name of the DLQ', required=False)
@click.option('--max-attempts', 'maxAttempts', help='Specifies the max deliveries attempts before DLQ redirection', required=False)
@click.option('--delivery-delay', 'deliveryDelay', help='Specifies the delivery delay time in ms', required=False)
def updateQueue(username, password, region, orgId, envId, name, fifo, ttl, lockTtl, encrypted, deadLetterQueue, maxAttempts, deliveryDelay):
    """This command creates a queue (standard or FIFO) in the given region, org id and environment id """

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/queues/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    payload = {
      "defaultTtl" : ttl,
      "defaultLockTtl" : lockTtl,
      "encrypted" : encrypted,
      "fifo" : fifo,
      "deadLetterQueueId": deadLetterQueue,
      "maxDeliveries": maxAttempts,
      "defaultDeliveryDelay": deliveryDelay
    }


    try:
        response = requests.request(
        "PATCH", mq_request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully updated"
    }))


@cli.command(name="create-exchange")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Exchange name', required=True)
@click.option('--encrypted', 'encrypted', help='Specifies if queue is encrypted', required=False, default=False)
def createExchange(username, password, region, orgId, envId, name, encrypted):
    """This command creates an exchange in the given region, org id and environment id  """
    #### Anypoint login ####
    token = login(username, password)
### Updated by Geovani to invoke Util function instead to implement it here ####
    createExchange_util(token, region, orgId, envId, name, encrypted)
 

@cli.command(name="update-exchange")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Exchange name', required=True)
@click.option('--encrypted', 'encrypted', help='Specifies if queue is encrypted', required=False, default=False)
def updateExchange(username, password, region, orgId, envId, name, encrypted):
    """This command creates an exchange in the given region, org id and environment id  """

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/exchanges/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    payload = {
      "encrypted" : encrypted
    }

    try:
        response = requests.request(
        "PATCH", mq_request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully updated"
    }))

@cli.command(name="bind-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--exchange-name', 'name', help='Exchange name', required=True)
@click.option('--queue-name', 'queueName', help='Queue to bind to exchange. Comma-separated value', required=True)
def bindQueues(username, password, region, orgId, envId, name, queueName):
    """This command creates an exchange in the given region, org id and environment id  """
    #### Anypoint login ####
    token = login(username, password)
### Updated by Geovani to invoke Util function instead to implement it here ####
    bindQueues_util(token, region, orgId, envId, name, queueName)


@cli.command(name="unbind-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--exchange-name', 'name', help='Exchange name', required=True)
@click.option('--queue-name', 'queueName', help='Queue to unbind from exchange. Comma-separated value', required=True)
def unbindQueues(username, password, region, orgId, envId, name, queueName):
    """This command creates an exchange in the given region, org id and environment id  """

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/bindings/exchanges/' + name + '/queues/' + queueName
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}


    try:
        response = requests.request(
        "DELETE", mq_request_url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": queueName + " was successfully unbinded from " + name
    }))


@cli.command(name="delete-queue")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
def deleteQueue(username, password, region, orgId, envId, name):
    """This command purges a queue in the given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/queues/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}


    try:
        response = requests.request("DELETE", mq_request_url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### 3rd: Build payload to return ####
    
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully purged"
    }))

@cli.command(name="delete-exchange")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Exchange name', required=True)
def deleteExchange(username, password, region, orgId, envId, name):
    """This command purges a queue in the given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations DELETE to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/exchanges/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}


    try:
        response = requests.request("DELETE", mq_request_url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### 3rd: Build payload to return ####
    
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully purged"
    }))

@cli.command()
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--name', 'name', help='Queue name', required=True)
def purge(username, password, region, orgId, envId, name):
    """This command purges a queue in the given region, org id and environment id"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/queues/' + name + '/messages'
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}


    try:
        response = requests.request("DELETE", mq_request_url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### 3rd: Build payload to return ####
    
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully purged"
    }))


#### Added by Geovani Osuna - export and import commands BEGIN ####

@cli.command()
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--conf-path', 'confPath', help='Path where conf files will be generated', envvar='CONF_PATH',  required=False)

def export(username, password, region, orgId, envId, confPath):
    """This search and return queues, exchanges, fifo queues and bindings corresponding to the given region, org id and environment id and exports them to a json file"""

    #### Anypoint login ####
    token = login(username, password)

    #### Request destinations to AMQ Rest API ####
    destinations_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations'
    payload = {}
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    try:
        destinations = requests.request(
        "GET", destinations_request_url, headers=headers, data=payload)
        destinations.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))



    
    json_string = json.dumps(destinations.json())

    timestamp = time.strftime("%Y-%m-%d_%H%M%S")

    if (confPath != '') and (confPath != None):
        dir = confPath
    else:
        dir = timestamp
    
    print("path:" + dir)

    if not os.path.exists(dir):
        os.mkdir(dir)

    #### Build payload to return ####
    queues = []
    for value in destinations.json():
       if(value.get('type') == 'queue' ):
            print("Queue extracted: " + value.get('queueId') )
            if(str(value.get('deadLetterSources')) == 'None'):
                with open(dir + '/queue_' + value.get('queueId') + '.json', 'w') as outfile:
                    outfile.write(json.dumps(value))
            else:
                with open(dir + '/queue-dlq_' + value.get('queueId') + '.json', 'w') as outfile:
                    outfile.write(json.dumps(value))              
       else:
            exchangeId = value.get('exchangeId')
            print("Exchange with bindings extracted: " + exchangeId)
            with open(dir + '/exchange_' + exchangeId + '.json', 'w') as outfile:
                outfile.write(json.dumps(value))
            
            bindings_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
                orgId + '/environments/' + envId + '/regions/' + region + '/bindings/exchanges/' + exchangeId
            payload = {}
            headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
                    token}

            try:
                bindings = requests.request(
                "GET", bindings_request_url, headers=headers, data=payload)
                bindings.raise_for_status()
            except HTTPError as http_err:
                raise Exception('HTTP error occurred: ' + str(http_err))
            except Exception as err:
                raise Exception('Other error occurred: ' + str(err))

            json_string = json.dumps(bindings.json())   

            with open(dir + '/bindings_' + exchangeId + '.json', 'w') as outfile:
                outfile.write(json_string)

    print("Output path: " + os.path.abspath(os.getcwd()) + '/' + dir)            
    print("Export Done")


@cli.command(name="import")
@click.option('--username', 'username', help='Anypoint username',  envvar='MQ_USERNAME')
@click.option('--password', 'password', help='Anypoint password', envvar='MQ_PASSWORD', hide_input=True)
@click.option('--region','-r', help='Anypoint MQ region', envvar='MQ_REGION', type=click.Choice(["us-east-1", "us-west-2", "ca-central-1", "eu-west-1", "eu-west-2", "ap-southeast-1", "ap-southeast-2"], case_sensitive=True))
@click.option('--organization-id', 'orgId', help='Anypoint organization id (business group id)', envvar='MQ_ORG_ID')
@click.option('--environment-id', 'envId', help='Anypoint environment id', envvar='MQ_ENV_ID')
@click.option('--conf-path', 'confPath', help='Path from where to load the exported conf files', envvar='CONF_PATH')
def importConf(username, password, region, orgId, envId, confPath):
    """This search and return queues, exchanges, fifo queues and bindings corresponding to the given region, org id and environment id and exports them to a json file"""

    #### Anypoint login ####
    token = login(username, password)

#### FIRST WE GENERATE THE DLQs, AS THOSE NEED TO EXIST BEFORE ASSIGNATION TO REGULAR QUEUES AS DLQs
    print("Importing DLQs")
    for file in os.listdir("" + confPath):
     
        if file.startswith("queue-dlq_"):
                print(os.path.join("", file)) 
                with open(confPath + "/" + file) as json_file:
                    bindings_array = []
                    item = json.load(json_file)

                    if(not hasattr(item, 'deadLetterQueueId')):
                        deadLetterQueueId = ''
                    else:
                        deadLetterQueueId = item['deadLetterQueueId']
                    if(not hasattr(item, 'maxDeliveries')):
                        maxdeliv = 10
                    else:
                        maxdeliv = item['maxDeliveries']

                    result = createQueue_util(token, region, orgId, envId, item['queueId'], item['fifo'], item['defaultTtl'], item['defaultLockTtl'],  item['encrypted'], deadLetterQueueId , maxdeliv , item['defaultDeliveryDelay'])


#### THEN WE DEFINE REGULAR QUEUES
    print("Importing Queues")
    for file in os.listdir("" + confPath):
     
        if file.startswith("queue_"):
                print(os.path.join("", file)) 
                with open(confPath + "/" + file) as json_file:
                    item = json.load(json_file)
                    if(not 'deadLetterQueueId' in item):
                        deadLetterQueueId = ''
                    else:
                        deadLetterQueueId = item['deadLetterQueueId']
                    if(not 'maxDeliveries' in item):
                        maxdeliv = 10
                    else:
                        maxdeliv = item['maxDeliveries']
                    result = createQueue_util(token, region, orgId, envId, item['queueId'], item['fifo'], item['defaultTtl'], item['defaultLockTtl'],  item['encrypted'], deadLetterQueueId , maxdeliv , item['defaultDeliveryDelay'])


#### THEN WE DEFINE EXCHANGES
    print("Importing Exchanges")
    for file in os.listdir("" + confPath):
     
        if file.startswith("exchange_"):
                print(os.path.join("", file)) 
                with open(confPath + "/" + file) as json_file:
                    item = json.load(json_file)
                    print(item)
                    result = createExchange_util(token, region, orgId, envId, item['exchangeId'], item['encrypted'])

#### THEN WE DEFINE THE BINDINGS
    print("Importing Bindings")
    for file in os.listdir("" + confPath):
     
        if file.startswith("bindings_"):
                print(os.path.join("", file)) 
                with open(confPath + "/" + file) as json_file:
                    bindings_array = json.load(json_file)
                    for item in bindings_array:
                        result = bindQueues_util(token, region, orgId, envId, item['exchangeId'],  item['queueId'])

    print("Import Done")
    

#### Added by Geovani Osuna - export and import commands END ####

###### COMMANDS #####

###### UTILS #####
def login(username, password):

    # Try to get token from cache # 
    cacheClient = memcache.Client(['memcached:11211'], debug=0)
    tokenResponse = cacheClient.get(username + password)

    if tokenResponse is None:
        login_url = "https://anypoint.mulesoft.com/accounts/login"

        ###### GET TOKEN ######
        payload = { "username": username, "password": password }
        headers = { 'Content-Type': 'application/json' }


        try:
            tokenHTTPResponse = requests.request("POST", login_url, headers=headers, data=json.dumps(payload))
            tokenHTTPResponse.raise_for_status()

            tokenResponse = tokenHTTPResponse.json().get('access_token')

            cacheClient.set(username + password, tokenResponse, 900)
        except HTTPError as http_err:
            raise Exception('HTTP error occurred: ' + str(http_err))
        except Exception as err:
            raise Exception('Other error occurred: ' + str(err))

    return tokenResponse   

#### Added by Geovani Osuna to reuse previously implemented functions - Util commands - bindQueues_util, createQueue_util and createExchange_util BEGIN ####

def bindQueues_util(token, region, orgId, envId, name, queueName):
    """This function creates an exchange in the given region, org id and environment id  """

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/bindings/exchanges/' + name + '/queues/' + queueName
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    payload = {}

    try:
        response = requests.request(
        "PUT", mq_request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": queueName + " was successfully binded to " + name
    })) 

def createQueue_util(token, region, orgId, envId, name, fifo=False, ttl=120000, lockTtl=10000, encrypted=False, deadLetterQueue=False, maxAttempts=False, deliveryDelay=False):
    """This function creates a queue (standard or FIFO) in the given region, org id and environment id """

    #### Request destinations PUT to AMQ Rest API ####
    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/queues/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    if ((deadLetterQueue != '') and (maxAttempts != '')) and ((deadLetterQueue != None) and (maxAttempts != None)):
        payload = {
        "defaultTtl" : ttl,
        "defaultLockTtl" : lockTtl,
        "encrypted" : encrypted,
        "fifo" : fifo,
        "deadLetterQueueId": deadLetterQueue,
        "maxDeliveries": maxAttempts,
        "defaultDeliveryDelay": deliveryDelay
        }
    else:
        payload = {
        "defaultTtl" : ttl,
        "defaultLockTtl" : lockTtl,
        "encrypted" : encrypted,
        "fifo" : fifo,
        "defaultDeliveryDelay": deliveryDelay
        }
   
    try:
        response = requests.request(
        "PUT", mq_request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully created"
    }))


def createExchange_util(token, region, orgId, envId, name, encrypted):
    """This function creates an exchange in the given region, org id and environment id  """

    #### Request destinations PUT to AMQ Rest API ####

    mq_request_url = 'https://anypoint.mulesoft.com/mq/admin/api/v1/organizations/' + \
        orgId + '/environments/' + envId + '/regions/' + region + '/destinations/exchanges/' + name
    headers = {'X-ANYPNT-ENV-ID': envId, 'Authorization': 'bearer ' +
               token}

    payload = {
      "encrypted" : encrypted
    }

    try:
        response = requests.request(
        "PUT", mq_request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except HTTPError as http_err:
        raise Exception('HTTP error occurred: ' + str(http_err))
    except Exception as err:
        raise Exception('Other error occurred: ' + str(err))


    #### Build payload to return ####
    print(json.dumps({   
        "success": True,
        "message": name + " was successfully created"
    }))

#### Added by Geovani Osuna to reuse previously implemented functions - Util commands - bindQueues_util, createQueue_util and createExchange_util END ####

###### UTILS #####
