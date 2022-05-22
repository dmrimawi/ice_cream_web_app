import os
import json
import sqlite3
import subprocess
import threading
from joblib import load
import pandas as pd
from flask import Flask, render_template, request, redirect, session
import logger_control as logger


app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'


SCRIPTS_DIR = os.path.abspath(os.path.join('.', 'scripts'))
CLONE_SCRIPT = os.path.join(SCRIPTS_DIR, 'clone_new_model.sh')
PUSH_SCRIPT = os.path.join(SCRIPTS_DIR, 'push_last_updates.sh')
MACHINE_LEARNING_REPO_DIR = os.path.abspath(os.path.join('..', 'machine-learner'))
CSV_FILE_PATH = os.path.join(MACHINE_LEARNING_REPO_DIR, 'data-files', 'ice_cream_rater_data.csv')
MODEL_FILE_PATH = os.path.join(MACHINE_LEARNING_REPO_DIR, 'output-model', 'ice_cream_rater_model.joblib')
DATABASE_PATH = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", 'ingredients.db'))
LAMBDA_ML_API = "https://f2968r0sib.execute-api.us-east-1.amazonaws.com/default/ice_cream_lambda"
FIRST_SELECT_OPTION_VALUE = "--Choose new ingrediant--"
ACCEPT_RATE_VALUES = [1, 2, 3, 4, 5]
RATE_VALUES_ERR = f"The values allowed for rate are: {ACCEPT_RATE_VALUES}"


# Helper functions
def run_query(query, select=True):
    output = list()
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    if select:
        rows = cursor.fetchall()
        for row in rows:
            output.append(row[0])
    else:
        connection.commit()
    connection.close()
    return output


def update_database_record():
    current_count_value = run_query("SELECT count from rating_count")[0]
    logger.debug(f"Current Vlaues is: {current_count_value}")
    new_value = int(current_count_value) + 1
    run_query(f"UPDATE rating_count SET count={new_value} WHERE id = 1", select=False)
    return new_value


def run_cmd(cmd):
    logger.debug(f"Running command: {cmd}..")
    p = subprocess.Popen(cmd)
    out, err = p.communicate()
    logger.debug(f"Output: {out}")
    logger.debug(f"Error: {err}")
    logger.debug(f"RC = {p.returncode}")


def push_data_file():
    cmd = f"{PUSH_SCRIPT} {MACHINE_LEARNING_REPO_DIR}"
    run_cmd(cmd)


def clone_new_model():
    cmd = f"{CLONE_SCRIPT} {MACHINE_LEARNING_REPO_DIR}"
    run_cmd(cmd)
    

def call_lambda_to_run_learner():
    push_data_file()
    logger.debug("start the learner process..")
    lambda_req = requests.get(LAMBDA_ML_API)
    lambda_json = lambda_req.json()
    logger.debug(f"request output: {lambda_json}")
    logger.debug("Resetting the rating count in DB")
    run_query(f"UPDATE rating_count SET count=0 WHERE id = 1", select=False)
    logger.debug("Done launching the training..")
    x = threading.Thread(target=clone_new_model)
    x.start()
    logger.debug("Cloning new updates")


def get_selected_ing_from_post(post_data):
    selected_list = [post_data[key] for key in post_data if (key != 'rate_value' and post_data[key] != \
                        FIRST_SELECT_OPTION_VALUE)]
    selected_dict = dict()
    for key in selected_list:
        selected_dict[key] = [1]
    for key in session['ingrediant_list']:
        if key not in selected_dict:
            selected_dict[key] = [0]
    return selected_dict, selected_list


def get_all_ingrediants_names():
    ingrediant_list = run_query("SELECT * FROM Ingredients")
    ingrediant_list = list(dict.fromkeys(ingrediant_list))
    ingrediant_list = sorted(ingrediant_list)
    return ingrediant_list


def verify_rate(rate):
    return rate in ACCEPT_RATE_VALUES


# Routes
@app.route('/rate_recipe', methods=['POST'])
def rate_recipe():
    try:
        rating = float(request.form['rate_value'])
        if verify_rate(int(rating)):
            ingredient_df = pd.DataFrame.from_dict(get_selected_ing_from_post(request.form)[0])
            ingredient_df = ingredient_df.assign(rating=rating)
            old_df = pd.read_csv(CSV_FILE_PATH)
            save_df = pd.concat([old_df, ingredient_df])
            save_df.to_csv(CSV_FILE_PATH, index=False)
            count = update_database_record()
            logger.debug(f"The new count is: {count}")
            if count >= 5:
                call_lambda_to_run_learner()
        else:
            session["error_msg"] = True
    except Exception as exp:
        logger.debug(f"-E- {exp}")
        session["error_msg"] = True
        session["actual_exception"] = str(exp)
    return redirect('/rate_some_recipe#rate')


@app.route('/rate_some_recipe')
def rate_some_recipe():
    error_msg = None
    if 'ingrediant_list' not in session:
        session['ingrediant_list'] = get_all_ingrediants_names()
    if "error_msg" in session and session["error_msg"]:
        session["error_msg"] = False
        error_msg = f"{RATE_VALUES_ERR}, [{session['actual_exception']}]"
    return render_template("rate.html", ingrediant_list=json.dumps(session['ingrediant_list']), \
                            error_msg=error_msg)


@app.route('/check_rate', methods=['POST'])
def check_rate():
    session['selected_ing'], session['selected'] = get_selected_ing_from_post(request.form)
    return redirect("/#rate")


@app.route("/")
def index():
    rate = None
    selected_list = None
    if 'ingrediant_list' not in session:
        session['ingrediant_list'] = get_all_ingrediants_names()
    if 'selected_ing' in session:
        if len(session['selected_ing']):
            clf = load(MODEL_FILE_PATH)
            ingredient_df = pd.DataFrame.from_dict(session['selected_ing'])
            rate = f"{clf.predict(ingredient_df)[0]}"
            selected_list = session['selected']
        session['selected_ing'] = None
        del session['selected_ing']
        session['selected'] = None
        del session['selected']
    return render_template("index.html", ingrediant_list=json.dumps(session['ingrediant_list']), \
                            rate=rate, selected_list=selected_list)

