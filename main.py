from flask import Flask, request, redirect, url_for, render_template, session
import os
import utils

port = 12345

app = Flask(__name__)

@app.route('/WarCrimes/')
def Criminal():
  result = "I am a stinky bear"
  return render_template('Bee.html', result=result)


@app.route('/WarCrimes2/')
def Criminal2():
   return render_template('crimes.html')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/results/')
def results():
    if 'data' in session:
        data = session['data']
        data2 = session['data2']
        data3 = session['data3']
        data4 = session['data4']
        topic = f"Topic: {session['topic']}"
        return render_template('results.html', generated=data, topic=topic, generated2=data2, generated3=data3, generated4=data4)
      # ['I dont care what you think about this...', 'But I do', 'I hate you']
    else:
        return render_template('results.html', generated=None, topic='')


@app.route('/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    # imagine prompt='News'
    if prompt is not None:
      try:
        output = utils.comment_generator(prompt)[0]['generated_text']
      except:
        output='fake comment'
      comment = utils.process_comment(output)
      try:
        convo = utils.convo_generator(comment)[0]['generated_text']
      except:
        convo = "The reddit bot is waking up, please refresh the page in 10 seconds"
      generated = utils.extract_comments(convo)
      print(generated)
      comment = generated[-1]
      try:
        convo = utils.convo_generator(comment)[0]['generated_text']
      except:
        convo = "The reddit bot is waking up, please refresh the page in 10 seconds"
      generated2 = utils.extract_comments(convo)
      comment = generated2[-1]
      try:
        convo = utils.convo_generator(comment)[0]['generated_text']
      except:
        convo = "The reddit bot is waking up, please refresh the page in 10 seconds"
      generated3 = utils.extract_comments(convo)
      comment = generated3[-1]
      try:
        convo = utils.convo_generator(comment)[0]['generated_text']
      except:
        convo = "The reddit bot is waking up, please refresh the page in 10 seconds"
      generated4 = utils.extract_comments(convo)
      
    session['data'] = generated
    session['data2'] = generated2
    session['data3'] = generated3
    session['data4'] = generated4
    session['topic'] = prompt
    
    return redirect(url_for('results') + '#modelresults')

# define additional routes here
# for example:
# @app.route('/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'redditbot.2023-summer-nlp.repl.co'

    print(f'Try to open\n\n    https://{website_url}' + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)




