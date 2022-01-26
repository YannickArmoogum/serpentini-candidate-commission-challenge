
import json
from dataclasses import dataclass
from models.deals import Deals
from models.users import Users
from dacite import from_dict
 

class Main():

    def __init__(self):
        pass

    ###Method to calculate commission based on Read.me level2 instructions####
    def calculate_commission(self,objective,amountSold):
        commissionValue = 0
        if 0 < amountSold <= objective/2:
            commissionValue = amountSold * (0.05)
        
        if objective/2 < amountSold <= objective:
            commissionValue = ((objective/2 *0.05)+((amountSold-objective/2) * 0.10))
        
        if amountSold > objective:
            commissionValue = ((objective/2 * 0.05) + (objective/2 * 0.10) + (0.15*(amountSold-objective)))

        return commissionValue

    ####Method to Process the Json file and to output the result#######
    def commission(self):
        # Opening JSON file
        f = open('data/input.json')

        # a dictionary
        data = json.load(f)
        output = {}
        outputList = []

        for i in data['users']:
            ####Instantiating Users to Users Models#####
            user = from_dict(data_class=Users,data=i)
            amountSold = 0
            for x in data['deals']:
                ####Retrieving the user deals  #####
                if x['user'] == i['id']: 
                    ####Instantiating Deals to deals model #####
                    deals = from_dict(data_class=Deals,data=x)
                    amountSold = amountSold + deals.amount
            ####Calling the calculate commission method #####
            commissionValue = self.calculate_commission(user.objective,amountSold)


            ###Formatting the result######
            entry = {'user_id':user.id,'commission':commissionValue}
            print('test',entry)
            outputList.append(entry)

        output['commissions'] = outputList

        f.close()
        ###Writing to Json#####
        with open('data/output.json', 'w') as outfile:
            json.dump(output, outfile)

if __name__=="__main__": 
    Main().commission()