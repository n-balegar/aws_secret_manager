import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
import sam

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

session = boto3.Session(
aws_access_key_id='',
aws_secret_access_key=''
)

#Creating S3 Resource From the Session.
s3 = session.resource('s3')

#Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
copy_source = {
    'Bucket': 'cda-source',
    'Key': 'manifest.json'
}

bucket = s3.Bucket('cda-ace-target')

bucket.copy(copy_source, 'manifest.json')

# Printing the Information That the File Is Copied.
print('Single File is copied')

res=sam.get_secret("aws_murthy","us-east-2","secretsmanager",glueContext)
print("inside function ",res) 

job.commit()
