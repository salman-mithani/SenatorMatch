from flask import Flask, render_template, request
import json
import requests

class Senator:
    """docstring for Senator."""
    name = "Name"
    party = "P"
    state = "State"
    idValue = "A000000"

    def __init__(self, name, party, state,idValue):
        self.name = name
        self.party = party
        self.state = state
        self.idValue = idValue

class User(object):
    """docstring for User."""
    uVotes = {}
    score = {}
    def __init__(self, Senators, UserVotes):
        #super(User, self).__init__()
        self.uVotes = UserVotes
        for key in Senators:
            self.score[key] = 0

def getSenators():
    headers = {'X-API-Key': 'Dy61pL808waBN30boujMt5352YtfipWF7fYBkSIz'}
    response = requests.get("https://api.propublica.org/congress/v1/114/senate/members.json", headers=headers)
    data = response.json()

    Senators = {}
    for i in data["results"][0]["members"]:
        Senators[i["id"]] = Senator(i["first_name"] + " " + i["last_name"], i["party"],i["state"],i["id"])

    return Senators


def getVotes(rollCall):
    headers = {'X-API-Key': 'Dy61pL808waBN30boujMt5352YtfipWF7fYBkSIz'}
    URL = "https://api.propublica.org/congress/v1/114/senate/sessions/1/votes/" + str(rollCall) + ".json"
    response  = requests.get(URL,headers=headers)
    data = response.json()
    return data

def findSenator(state, dic,idValues):
    for key in dic:
        if(dic[key].state == state):
            idValues.append(dic[key].idValue)

def findVote(votes, idValue):
    for vote in votes["results"]["votes"]["vote"]["positions"]:
        if(vote["member_id"] == idValue):
            return vote["vote_position"]


def returnSenators(state):
    senators = getSenators()
    idValues = []
    names = []
    findSenator(state, senators, idValues)
    names.append(senators[idValues[0]].name + " " + " (" + senators[idValues[0]].party + ")")
    names.append(senators[idValues[1]].name + " " + "( " + senators[idValues[1]].party + ")")
    return names

def returnVotes(state, rollCall):
    senators = getSenators()
    idValues = []
    findSenator(state, senators, idValues)
    data = getVotes(rollCall)
    choices = []
    choices.append(findVote(data,idValues[0]))
    choices.append(findVote(data,idValues[1]))
    return choices

def count(person):
    for roll in person.uVotes:
        data = getVotes(roll)
        for idValue in person.score:
            if(findVote(data,idValue) == person.uVotes[roll]):
                person.score[idValue] +=1

def maxSenators(person, senators, name):
    inverse = [(value,key) for key,value in person.score.items()]
    name.append(senators[max(inverse)[1]].name)
    party = senators[max(inverse)[1]].party
    percent = (((max(inverse)[0])/float(15.0))*float(100.0))
    return "The United States Senator whose votes your votes most closely allign with is " + name[0] + " (" + party + ") with " + str(percent)[:4] + "% of your votes being alike."

def imageSearch(name):
    URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCIRrSrC15UaQRneV4yx_ebpYdul7eWRhY&cx=009635383684542961134%3Asltokjrpsla&num=2&imgSize=medium&searchType=image&q=" + name
    response = requests.get(URL)
    data = response.json()
    img = data['items'][0]['link']
    return img

app = Flask(__name__)

state = 'blank'

@app.route('/', methods=['GET','POST'])
def homepage():
	if request.method != 'POST':
		return render_template('homepage.html')
	else:
		state = request.form['state']
		return render_template('homepage.html')

@app.route('/quiz', methods = ['GET','POST'])
def quiz():
	if request.method == 'POST':
		global state
		state = request.form['state']
		return render_template('quiz.html', state = state)

@app.route('/results', methods = ['GET','POST'])
def results():
	if request.method == 'POST':
		global state
		state = str(state)

		global returnSenators
		global returnVotes
		names = returnSenators(state)
		s1name = names[0]
		s2name = names[1]

		q1 = request.form['q1']
		q1votes = returnVotes(state, 334)
		q1s1 = q1votes[0]
		q1s2 = q1votes[1]

		q2 = request.form['q2']
		q2votes = returnVotes(state, 331)
		q2s1 = q2votes[0]
		q2s2 = q2votes[1]

		q3 = request.form['q3']
		q3votes = returnVotes(state, 329)
		q3s1 = q3votes[0]
		q3s2 = q3votes[1]

		q4 = request.form['q4']
		q4votes = returnVotes(state, 325)
		q4s1 = q4votes[0]
		q4s2 = q4votes[1]

		q5 = request.form['q5']
		q5votes = returnVotes(state, 291)
		q5s1 = q5votes[0]
		q5s2 = q5votes[1]

		q6 = request.form['q6']
		q6votes = returnVotes(state, 239)
		q6s1 = q6votes[0]
		q6s2 = q6votes[1]

		q7 = request.form['q7']
		q7votes = returnVotes(state, 238)
		q7s1 = q7votes[0]
		q7s2 = q7votes[1]

		q8 = request.form['q8']
		q8votes = returnVotes(state, 233)
		q8s1 = q8votes[0]
		q8s2 = q8votes[1]

		q9 = request.form['q9']
		q9votes = returnVotes(state, 189)
		q9s1 = q9votes[0]
		q9s2 = q9votes[1]

		q10 = request.form['q10']
		q10votes = returnVotes(state, 132)
		q10s1 = q10votes[0]
		q10s2 = q10votes[1]

		q11 = request.form['q11']
		q11votes = returnVotes(state, 131)
		q11s1 = q11votes[0]
		q11s2 = q11votes[1]

		q12 = request.form['q12']
		q12votes = returnVotes(state, 111)
		q12s1 = q12votes[0]
		q12s2 = q12votes[1]

		q13 = request.form['q13']
		q13votes = returnVotes(state, 78)
		q13s1 = q13votes[0]
		q13s2 = q13votes[1]

		q14 = request.form['q14']
		q14votes = returnVotes(state, 44)
		q14s1 = q14votes[0]
		q14s2 = q14votes[1]

		q15 = request.form['q15']
		q15votes = returnVotes(state, 31)
		q15s1 = q15votes[0]
		q15s2 = q15votes[1]

		userVotes = {334:q1, 331:q2, 329: q3, 325:q4, 291:q5, 239:q6, 238:q7, 233:q8, 189:q9, 132:q10, 131:q11, 111:q12, 78:q13, 44:q14, 31:q15}

		global getSenators
		global maxSenators
		global imageSearch
		global count
		senators = getSenators()
		person = User(senators, userVotes)
		count(person)

		sen_name = []
		output = maxSenators(person, senators, sen_name)
		imglink = imageSearch(sen_name[0])

		return render_template('results.html', senator1 = s1name, senator2 = s2name, q1s1 = q1s1, q1s2 = q1s2, q2s1 = q2s1, q2s2 = q2s2, q3s1 = q3s1, q3s2 = q3s2, q4s1 = q4s1, q4s2 = q4s2, q5s1 = q5s1, q5s2 = q5s2, q6s1 = q6s1, q6s2 = q6s2, q7s1 = q7s1, q7s2 = q7s2, q8s1 = q8s1, q8s2 = q8s2, q9s1 = q9s1, q9s2 = q9s2, q10s1 = q10s1, q10s2 = q10s2, q11s1 = q11s1, q11s2 = q11s2, q12s1 = q12s1, q12s2 = q12s2, q13s1 = q13s1, q13s2 = q13s2, q14s1 = q14s1, q14s2 = q14s2, q15s1 = q15s1, q15s2 = q15s2, q1 = q1, q2 = q2, q3 = q3, q4 = q4, q5 = q5, q6 = q6, q7 = q7, q8 = q8, q9 = q9, q10 = q10, q11 = q11, q12 = q13, q13 = q13, q14 = q14, q15 = q15, output = output, filename = imglink)

if __name__ == '__main__':
	app.run()
