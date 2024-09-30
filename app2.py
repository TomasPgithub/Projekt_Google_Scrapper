from flask import Flask, request, render_template, redirect, url_for, flash, session
import json
from serpapi import GoogleSearch

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Změňte na silnější klíč pro produkci

# Předem definované uživatelské jméno a heslo
USERNAME = 'USER'
PASSWORD = 'INIZIO-projekt'

def search_google(query):
    params = {
        "q": query,
        "hl": "cs",  # Nastavení na češtinu
        "gl": "cz",  # Nastavení na Českou republiku
        "api_key": "3034cba186f6ca5b52c286ddb3fa662fcc7bbbbe6e34472ecf495911ac2f5552"  # Nahraď svým API klíčem ze SerpAPI
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Debug: Vytisknutí celé odpovědi API pro kontrolu
    print(results)

    # Zkontrolujeme, zda klíč 'organic_results' existuje
    if 'organic_results' in results:
        links = [result['link'] for result in results['organic_results']]
    else:
        links = []
        print("No organic results found.")
    
    return links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Ověření uživatele
        if username == USERNAME and password == PASSWORD:
            session['username'] = username  # Uložení uživatelského jména do session
            query = request.form.get('query')  # Získání dotazu z formuláře
            results = search_google(query) if query else []
            return render_template('index.html', results=results)
        else:
            flash('Neplatné uživatelské jméno nebo heslo!')
    
    return render_template('login.html')  # Přesměrování na přihlašovací stránku

@app.route('/logout')
def logout():
    session.pop('username', None)  # Odstranění uživatelského jména ze session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)