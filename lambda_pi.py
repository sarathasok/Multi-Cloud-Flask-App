#Function for generating shots and incricle (Lambda Function)
import json

import random


#S = SHOTS
#Q= REPORTING RATE
#D=DIGITS

def lambda_handler(event, context):
    pi_value=[]
    shots_value=[]
   
    incoming= (event['key1'])
 
    incoming=incoming.split(",")
    Q=int(incoming[0])
    
    
    S=int(incoming[1])
    #Q=10
    #S=1000
    
    
    incircle=0
    incircle_list=[]
    for i in range(1,S+1):
        random1=random.uniform(-1.0,1.0)
        random2=random.uniform(-1.0,1.0)
        if (((random1*random1)+(random2*random2)) < 1):
            incircle += 1
        if i in [k for k in range(0,S+Q,Q)]:
            incircle_list.append(incircle)
            #pi_value.append(4.0 * incircle/i)
            shots_value.append(i)

    
    

    return str(shots_value),str(incircle_list)
    
    



