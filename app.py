from flask import Flask, request, redirect, url_for, render_template
import webbrowser

from api_requests import *
from settings import *

app = Flask(__name__)
access_token = None


def start_up():
    params = {
        'client_id': APP_ID,
        'display': 'page',
        'redirect_uri': f'{BASE_URL}/vk',
        'response_type': 'code',
        'v': '5.126',
    }
    url_with_params = VK_CODE_URL + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    webbrowser.open(url_with_params)


@app.route('/vk')
def vk_auth():
    global access_token
    access_token = get_token(request.args.get('code'))
    return redirect(url_for('main_flow'))


@app.route('/', methods=['GET', 'POST'])
def main_flow():
    if request.method == 'POST':
        data, is_success = get_group_data(access_token, request.form.get('group_id'))
        print(data)
        return render_template('main.html', data=data, is_success=is_success)

    return render_template('main.html')


start_up()

app.run()
