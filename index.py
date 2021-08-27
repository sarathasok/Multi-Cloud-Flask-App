#Import libraries
import os
import boto3
import logging
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from matplotlib import style
from flask import Flask, request, render_template,redirect
import ast
from scipy import stats
import scipy as sp
from pandas import DataFrame
import seaborn as sns
import json
import queue
import threading
import multiprocessing
import ec2_run
import time
import http.client
import parallel_lambda
import math

app = Flask(__name__)

def doRender(tname, values={}):
	if not os.path.isfile( os.path.join(os.getcwd(), 'templates/'+tname) ): 
		return render_template('home.html')
	return render_template(tname, **values) 


@app.route('/form1', methods=['GET','POST'])

def calculate():
	parallel= int(request.form.get('key1'))
	shots= int(request.form.get('key2'))
	rates= int(request.form.get('key3'))
	digits= int(request.form.get('key4'))
	if (lambdaa=="Lambda"):
		df,pi_values,est_pi,rates, status, cost_est=parallel_lambda.lamda_estimation(shots, rates, parallel, digits)
	if (ec2=="EC2"):
		df,pi_values,est_pi,rates, status, cost_est=ec2_run.ec2_estimation(shots, rates, parallel, digits)	
	
	x_axis=[j for j in range(len(pi_values))]
	fixed_pie=[math.pi]*len(pi_values)
	dfhtml=[df.to_html(classes='data',escape=False)] #converting dataframe to html type
	#print(df)
	return render_template('secondpage.html',status=status,data=pi_values,fixed_pie=fixed_pie,x_axis=x_axis,est_pi=est_pi,parallel=parallel,shots=shots,r_rate=rates,digits=digits, df = dfhtml, titles = df.columns.values)


	
@app.route('/form2', methods=['GET','POST'])	

def Service():
	global ec2, lambdaa
	ec2= request.form.get('ec2')
	lambdaa = request.form.get('lambda')
	print("ssas", lambdaa)
	print("ssas", ec2)
	data=1
	print(data)
	print(ec2)
	print(lambdaa)
	return render_template('index.html')
	
	
@app.route('/bucket', methods=['GET','POST'])	

def s3_bucket():
    v=str('0')+","+str('0')+","+str('0')+","+str('0')+","+str('2')+","+str('0')+","+str('0')
    print(v)
    datahist=parallel_lambda.s3bucket(v)
    a_json=json.loads(datahist)
    final_df=pd.DataFrame()
    for i in range(0,len(a_json)):
            json_d=json.loads(a_json[i])
            dataf=pd.DataFrame(list(json_d.values()))
            dataf=dataf.T
            dataf.columns=['Shots','Rate','Digits','Resources','Pi_value_estimated','Cost in $']
            final_df=final_df.append(dataf)
            dataframe_hist=[final_df.to_html(classes='data',escape=False)]
    return render_template('history.html',history=dataframe_hist,titles=final_df.columns.values)	

@app.route('/terminate', methods=['GET','POST'])		
def terminate():
	os.environ['AWS_SHARED_CREDENTIALS_FILE']='./cred'
	ec2 = boto3.resource('ec2', 'us-east-1')
# iterate through instance IDs and terminate them
	instances = ec2.instances.filter(
    	Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in instances:
 		ec2.instances.filter(InstanceIds=ids).terminate()

	
@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')

def mainPage(path):

	return doRender(path)


@app.errorhandler(500)



def server_error(e):

	logging.exception('ERROR!')

	return """An error occurred: <pre>{}</pre>""".format(e), 500



if __name__ == '__main__':

	app.run(host='0.0.0.0',port=8080,debug=True)
