
import json
from dataclasses import dataclass
from models.deals import Deals
from models.users import Users
from dacite import from_dict

class Main():

    def __init__(self):
        pass
    def commission(self):
        # Opening JSON file
        f = open('data/input.json')

        # Json to dictionary
        data = json.load(f)
        output = {}
        outputList = []

        #Looping through Users
        for count, i in enumerate(data['users']):
            ###Instantiating Users to user model          #######
            user = from_dict(data_class=Users,data=i)
            dealsCount = 0
            amountSold = 0
            commission_value = 0

            #Looping through Deals
            for x in data['deals']:
                if x['user'] == i['id']: 
                    ####Instantiating Deals to deals model#######
                    deals = from_dict(data_class=Deals,data=x)
                    amountSold= amountSold + deals.amount
                    dealsCount= dealsCount+1

            ###Calculating Commission based on deal count####
            if  0 < dealsCount < 3:
                commission_value = commission_value + (0.10 * amountSold)

            if dealsCount >= 3:
                commission_value  = commission_value  + (0.20 * amountSold)

                
            if amountSold >2000:
                commission_value  = commission_value  + 500



            entry = {'user_id':user.id,'commission':commission_value}
            outputList.append(entry)

        ####Formating the result into a dictionnary (in the correct format as per the expected_output.json)##### 

        output['commissions'] = outputList

        f.close()
        ###Writing Json####
        with open('data/output.json', 'w') as outfile:
            json.dump(output, outfile)

####Defining class and making the commission method run on script load####
if __name__=="__main__": 
    Main().commission()