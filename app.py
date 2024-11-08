from flask import Flask, render_template, request, redirect, url_for, make_response
import os

app = Flask(__name__)

# Path to the file where votes are stored
VOTES_FILE = 'votes.txt'

# Initialize votes dictionary
votes = {"Option 1": 0, "Option 2": 0}

def read_votes():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                option, count = line.strip().split(':')
                votes[option] = int(count)

def write_votes():
    with open(VOTES_FILE, 'w') as file:
        for option, count in votes.items():
            file.write(f'{option}:{count}\n')

def get_total_votes():
    return sum(votes.values())

@app.route('/', methods=['GET', 'POST'])
def index():
    user_vote = request.cookies.get('user_vote')
    read_votes()
    if request.method == 'POST' and not user_vote:
        option = request.form['vote']
        if option in votes:
            votes[option] += 1
            write_votes()
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('user_vote', option)
            return resp
    total_votes = get_total_votes()
    return render_template('index.html', votes=votes, user_vote=user_vote, total_votes=total_votes)

@app.route('/clear_vote')
def clear_vote():
    # Reset the votes
    global votes
    votes = {"Option 1": 0, "Option 2": 0}
    write_votes()
    # Clear the cookie
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_vote', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)