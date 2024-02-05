from flask import Blueprint, json, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
import requests

auth = Blueprint('auth', __name__)

USER_AUTH_API = "http://127.0.0.1:5000/auth/login"
USER_REGISTER_API = "http://127.0.0.1:5000/auth/sign-up"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            response = requests.post(USER_AUTH_API, json={'email': email, 'password': password})
            response.raise_for_status()
            data = response.json()
            print(f'Response status code: {response.status_code}')
            print(f'Response content: {response.content}')

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('authenticated'):
                        flash('Logged in successfully!', category='success')
                        return redirect(url_for('views.home'))
                    else:
                        flash('Incorrect password, try again.', category='error')
                except json.JSONDecodeError:
                    flash('Error decoding JSON response.', category='error')
            else:
                flash(f'Error during authentication. Status Code: {response.status_code}', category='error')
            
            return jsonify({'authenticated': data.get('authenticated', False)})

    except requests.RequestException as e:
        return jsonify({'error': f'RequestException: {e}'}), 500
    except json.JSONDecodeError as e:
        return jsonify({'error': f'JSONDecodeError: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'}), 500

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        response = requests.post(USER_REGISTER_API, json={'email': email, 'first_name': first_name, 'password': password1})
        
        if response.ok:
            data = response.json()
            if data.get('registered'):
                flash('Account created!', category='success')
                
                
                return redirect(url_for('views.home'))
            else:
                flash('Email already exists or other registration error.', category='error')
        else:
            flash('Error during registration.', category='error')

    return render_template("signup.html", user=current_user)
