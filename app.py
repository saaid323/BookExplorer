from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_books(query, start_index=0, max_results=38):
      """
      sends request to google books api.
      """
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
FANTASY = get_books("Fantasy")
FICTION = get_books("Fiction")


@app.route('/index')
def index():
    """
    This looks bad but i did this because i wanted
    everything to be in one page.
    """
    # POETRY query result
    items = POETRY
    page = request.args.get('page', 1, type=int)
    per_page = 6
    total_pages = len(items) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    all_items = items[start:end]

    # query the search
    q = request.args.get('q')
    results = get_books(q)[:6]
    
    # Programming query result
    items_1 = PROGRAMMING
    page_1 = request.args.get('page_1', 1, type=int)
    per_page_1 = 6
    total_pages_1 = len(items_1) // per_page_1
    start_1 = (page_1 - 1) * per_page_1
    end_1 = start_1 + per_page_1
    all_items_1 = items_1[start_1:end_1]

    # fantasy query result
    items_2 = FANTASY
    page_2 = request.args.get('page_2', 1, type=int)
    per_page_2 = 6
    total_pages_2 = len(items_2) // per_page_2
    start_2 = (page_2 - 1) * per_page_2
    end_2 = start_2 + per_page_2
    all_items_2 = items_2[start_2:end_2]

    # fiction query result
    items_3 = FICTION
    page_3 = request.args.get('page_3', 1, type=int)
    per_page_3 = 6
    total_pages_3 = len(items_3) // per_page_3
    start_3 = (page_3 - 1) * per_page_3
    end_3 = start_3 + per_page_3
    all_items_3 = items_3[start_3:end_3]

    return render_template("index.html", per_page=per_page, total_pages=total_pages,
                            all_items=all_items, page=page, page_1=page_1, per_page_1=per_page_1,
                            total_pages_1=total_pages_1, all_items_1=all_items_1, results=results,
                            per_page_2=per_page_2, total_pages_2=total_pages_2, all_items_2=all_items_2,
                            page_2=page_2, per_page_3=per_page_3, total_pages_3=total_pages_3,
                            all_items_3=all_items_3, page_3=page_3)


@app.route("/")
def home():
     """
     Home page
     """
     return render_template("home.html")     

