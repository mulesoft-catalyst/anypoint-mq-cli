# MQ CLI

## Pre-Requisites

- Install memcached 
	- On MacOS: brew install memcached
	- On Linux: apt-get install memcached or yum install memcached
	- References: https://github.com/memcached/memcached/wiki/Install
- Run memcached
	- Open terminal and run memcached


## Steps

- Install python: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
- Run this command: `python get-pip.py`
- Install virtualenv: `python -m pip install virtualenv --user`
- Add virtualenv to PATH: `export PATH=$PATH:{path-to-virtualenv}` (e.g. in MacOS: `export PATH=$PATH:/Users/username/Library/Python/2.7/bin`)
- Create a virtualenv in your folder: `virtualenv venv`
- Activate the virtual environment: `. venv/bin/activate`
- Install scripts (taken from setup.py): `pip install --editable .`
- Run the CLI: `mq`
- Try operations
	- mq --help
	- mq search --help
	- mq search --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId}
	- mq find-queues --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} --name={queueName}
	- mq find-exchanges --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} --name={exchangeName}
	- mq create-queue --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myQueueName} --fifo={fifo} (optional) --lock-ttl={lockTtl} (optional) --ttl={ttl} (optional) --encrypted={encrypted} (optional) --dead-letter-queue={dlqQueueName} (optional) 
	- mq update-queue --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myQueueName} --fifo={fifo} (optional) --lock-ttl={lockTtl} (optional) --ttl={ttl} (optional) --encrypted={encrypted} (optional) --dead-letter-queue={dlqQueueName} (optional) --max-attempts={maxAttempts} (optional) --delivery-delay={deliveryDelay} (optional)
	- mq create-exchange --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myExchangeName} --encrypted={encrypted} (optional)
	- mq update-exchange --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myExchangeName} --encrypted={encrypted} (optional)
	- mq bind-queue --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} --exchange-name={myQueueName} --queue-name={myQueueName}
	- mq unbind-queue --exchange-name={myQueueName} --queue-name={myQueueName}
	- mq delete-queue --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myQueueName}
	- mq delete-exchange --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myExchangeName}
	- mq purge --username={myUsername} --password={myPassword} --region={region} --organization-id={bgId} --environment-id={envId} name={myQueueName}
- Deactivate the virtual environment: `deactivate`


## Considerations
- This tool is not officially supported by Mulesoft
