#This the function used for EC2
from flask import Flask
from flask import request
import math
import random
import json
app=Flask(__name__)
@app.route('/')
def calculate():
    pi_value=[]
    shots_value=[]
    Q=int(request.args.get('Q'))

    S=int(request.args.get('S'))

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

    return_value=incircle_list,shots_value
    return_value=json.dumps(return_value)
    return return_value

if __name__ == "__main__":
    app.run()
