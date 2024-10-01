from flask import Flask, request, render_template
from serpapi import GoogleSearch

app = Flask(__name__)

def search_google(query):
    params = {
        "q": query,
        "hl": "cs",  # Nastavení na češtinu
        "gl": "cz",  # Nastavení na Českou republiku
        "api_key": "886fe890e1b039445ef20fc8a0869478bae1b0e424ef77127087a36a60d9a30c"  # Zadej svůj SerpAPI klíč
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Uložení výsledků do seznamu slovníků
    links = []
    if 'organic_results' in results:
        for result in results['organic_results']:
            title = result.get('title', 'Není k dispozici')
            link = result.get('link', 'Není k dispozici')
            links.append({'titulek': title, 'odkaz': link})
    else:
        print("Nebyly nalezeny žádné organické výsledky.")

    return links

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            results = search_google(query)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)