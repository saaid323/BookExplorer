from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_books(query, start_index=0, max_results=38):
      items = []
      base_url = "https://www.googleapis.com/books/v1/volumes"
      params = {
          'q': query,
          'startIndex': start_index,
          'maxResults': max_results
          }
      response = requests.get(base_url, params=params)
      if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                image_links = volume_info.get('imageLinks', {})
                small_thumbnail = image_links.get('thumbnail', None)
                if small_thumbnail is not None:
                    dic = {'title': volume_info['title'],
                            "images": small_thumbnail, 
                            "preview": item['volumeInfo']['previewLink']}
                    items.append(dic)
      return items

POETRY = get_books("poetry")
PROGRAMMING = get_books("programming")


@app.route('/index')
def index():
    items = POETRY
    page = request.args.get('page', 1, type=int)
    per_page = 6
    total_pages = len(items) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    all_items = items[start:end]

    q = request.args.get('q')
    results = get_books(q)[:6]

    items_1 = PROGRAMMING
    page_1 = request.args.get('page_1', 1, type=int)
    per_page_1 = 6
    total_pages_1 = len(items_1) // per_page_1
    start_1 = (page_1 - 1) * per_page_1
    end_1 = start_1 + per_page_1
    all_items_1 = items_1[start_1:end_1]

    return render_template("index.html", per_page=per_page, total_pages=total_pages,
                            all_items=all_items, page=page, page_1=page_1, per_page_1=per_page_1,
                            total_pages_1=total_pages_1, all_items_1=all_items_1, results=results)


@app.route("/")
def home():
     return render_template("home.html")

     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
