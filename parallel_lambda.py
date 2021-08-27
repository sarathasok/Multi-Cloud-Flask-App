#!/usr/bin/env python3
import time
import string
import boto3
import pandas as pd
import numpy as np
import math
from math import pi
import random
import http.client
from concurrent.futures import ThreadPoolExecutor
# creates a list of values as long as the number of things we want
# in parallel so we could associate an ID to each

def lamda_estimation(shots, rates, parallel, digits):
  global nshots, nrates, nparallel, ndigits, count, runs ,v
  time_dur = 0
  nparallel = parallel
  nshots = int(shots/nparallel)
  #print("Number of shots after splitting:",nshots)
  nrates = rates
  ndigits = digits
  runs=[value for value in range(parallel)]
  count = 1000
  th=1 #Setting a threshold to avoid running forever
  df = pd.DataFrame()
  pi_values = []
  result_incircle = []
  result_rates = []
  
  while(th<=20):
    start = time.time()
    results= (list(getpages()))
    end = time.time()
    time_dur = time_dur + (end - start)
    #print("results:", results)
    df = df.append(pd.DataFrame(results, columns=["incircle list", "shots list"]), ignore_index=True)
    
    for k in range(0,int(nshots/rates)):
      incircle_sum=0
      rate_sum=0
      est_pi=0
      for i,j in enumerate(results):
        incircle_sum=incircle_sum+j[0][k]
        rate_sum=rate_sum+j[1][k]
        est_pi=4*(incircle_sum/rate_sum)
      pi_values.append(est_pi)
      result_incircle.append(incircle_sum)
      result_rates.append(rate_sum)   
      
      #print("Dur", td) 
    if ((truncate(pi_values[(int(nshots/rates))-1],digits))==(truncate(pi,digits))):
       status="Got a matching value of pi"
       break
    else:
       status = "Did not get the precise pi value with the given digits"
       th=th+1   
  cost_est = float((time_dur * (0.00001667)) + (.2* (nparallel*(1/1000000))))   
  data_string=str(shots)+","+str(nrates)+","+str(ndigits)+","+str(parallel)+","+str('1')+","+str(pi_values[(int(nshots/rates))-1])+","+str(cost_est) 
  s3bucket(data_string)
  #print("Duration", time_dur)
 
  print("price", cost_est)
  #print(result_incircle)
  return df,pi_values,pi_values[(int(nshots/rates))-1],rates, status, cost_est
  
def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def getpage(id):
  try:
   total_duration=0
   c = http.client.HTTPSConnection("hgbkjemg68.execute-api.us-east-1.amazonaws.com")
   v = str(nrates) + "," + str(nshots)
   print(v)
   json='{ "key1":"'+v+'"}'
   c.request("POST", "/default/pi_calculation", json)
   response = c.getresponse()
   data2 = response.read()
   data2=data2.decode("utf-8")
   x = processor(data2)
  	
  except IOError:
   print( 'Failed to open ', host ) # Is the Lambda address correct?
   print(data+" from "+str(id)) # May expose threads as completing in a different order
  return x

def processor(data_out):
    data_out=data_out[2:-2]
    data_out=data_out.split('"')
    data_out.remove(', ')
    rate=data_out[1][1:-1]
    incircles=data_out[0][1:-1]
    rate=rate.split(",")
    incircles=incircles.split(",")
    rate=[int(i) for i in rate]
    incircles=[int(i) for i in incircles]
    final_out=rate,incircles
    return final_out


def getpages():

  with ThreadPoolExecutor() as executor:
    results=executor.map(getpage, runs)
    return results
    
def s3bucket(st):
   
    c = http.client.HTTPSConnection("adr001h1gb.execute-api.us-east-1.amazonaws.com") 
 
    json= '{ "key1":"'+st+'"}'
    c.request("POST", "/default/hist_storage", json)
    response = c.getresponse()
    data2 = response.read()
    data2=data2.decode("utf-8")
    print("Bucket output",data2)
    return data2
    
if __name__ == '__main__':
  main(12000,1000,4,2)
  #start = time.time()
  #results = getpages()
  #print( "Elapsed Time: ", time.time() - start)
