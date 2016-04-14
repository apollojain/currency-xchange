from flask import Flask, render_template, request, redirect
import max_exchange
from max_exchange import *
from graph import *

app = Flask(__name__)

@app.route('/')
def index():
	# print render_template('index.html')
	return render_template('index.html')

@app.route('/submission', methods=['POST'])
def submission():
	form_from = request.form['from']
	form_to = request.form['to']
	print form_from + " -> " + form_to
	rate = str(max_exchange(form_from, form_to))
  	graph = get_order(form_from, form_to)
	create_dag(form_from, form_to, graph)
	return render_template('submission.html', fr=form_from, to=form_to, rate=rate, graph=str(graph))

if __name__ == '__main__':
# 	print ("wtf")
	app.run() 