#Function for reading and writing for making history table
import json
import boto3

def lambda_handler(event, context):
    s3=boto3.client('s3')
    bucket='historystorage'
    input=(event['key1'])
    input = input.split(",")
    s=int(input[0])
    r=int(input[1])
    d=int(input[2])
    res=int(input[3])
    sel=int(input[4])
    est_pi=str(input[5])
    est_cost=float(input[6])
    if(sel==1):
        data= {"Shots":s,"Rate":r,"Digits":d,"Resources":res,"Estimated_pi":est_pi,"Cost":est_cost}
        key="store" + str(r) + str(s) + str(res) + str(d) + ".json"
        upload=bytes(json.dumps(data).encode('UTF-8'))
        s3.put_object(Bucket=bucket,Key=key,Body=upload)
    if(sel==2):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('historystorage')
        body=[]
        for obj in bucket.objects.all():
            key = obj.key
            body.append(obj.get()['Body'].read())
        return body
