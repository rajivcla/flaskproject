from flask import Flask
from flask_restplus import Api, Resource
import csv
import re
import heapq

app = Flask(__name__)
api = Api(app)

# read csv data
vsn_data = {}
with open('vsn_data.csv') as csvfile:
     vsn_data = list(csv.DictReader(csvfile))
     i = 0
     
# setup route for api
@api.route('/<string:id>')
class VSN(Resource):
    def get(self,id):
        if self.validate_input(id):
            best_match = self.find_closest_match(id)
            if best_match != -1:
                return {"result": best_match}
            else:
                return {"result": "no match found"}
        else:
            return {"error": "input not in the correct format, 6 letters followed by 6 numbers"}

    def validate_input(self, user_vsn):
        # validates user input is in the correct form
        rex = re.compile("^[A-Z]{6}[0-9]{6}$")
        return rex.match(user_vsn)

    def find_closest_match(self, user_vsn):
        # returns the closest match or -1 if no match was found
        vsn_len = len(user_vsn)
        li = []
        heapq.heapify(li)
        for row in vsn_data:
            # store off heap value & retain db_vsn in a tuple, ie: (#,db_vsn)
            distance = self.hamming_distance(user_vsn,row['Serial Number Pattern'])
            heapq.heappush(li,(distance,row['Serial Number Pattern']))
            
        closest_match = heapq.heappop(li)
        if int(closest_match[0]) == 0:
            return closest_match[1]
        else:
            return -1

    def hamming_distance(self, user_vsn, db_vsn):
        # store wildcard distance as decimal, store hamming distance as integer
        # if there are less wildcards for same hamming distance, that value is closer
        distance =db_vsn.count('*')/100.0 # assuming 100 max matches
        L = len(db_vsn)
        for i in range(L):
            if db_vsn[i] != user_vsn[i] and db_vsn[i] != '*':
                distance += 1
                break
        return distance
            
if __name__ == "__main__":
    app.run()