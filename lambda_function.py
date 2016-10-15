from __future__ import print_function

from datetime import datetime

from boto3 import session
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from requests_aws_sign import AWSV4Sign

# authentication with elasticsearch based on example from https://github.com/jmenga/requests-aws-sign

# Establish credentials
session = session.Session()
credentials = session.get_credentials()
region = session.region_name or 'ap-southeast-2'

# Elasticsearch settings
service = 'es'
# note that https:// shouldn't be in the host
es_host = "es-search-domain.ap-southeast-2.es.amazonaws.com/"
auth=AWSV4Sign(credentials, region, service)
es_client = Elasticsearch(host=es_host,
                          port=443,
                          connection_class=RequestsHttpConnection,
                          http_auth=auth,
                          use_ssl=True,
                          verify_ssl=True)


def lambda_handler(event, context):
    """Events are CSP reports, to be stored in ElasticSearch"""
    result = {"report-created": False}
    if 'csp-report' in event:
	event['occurred_at'] = datetime.utcnow()

	es_client.index(index="csp", doc_type="csp", body=event)
        result["report-created"] = True
    return result
