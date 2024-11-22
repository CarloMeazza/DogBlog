from flask import Flask, render_template, request, jsonify, abort
from json_crud import JsonCrud
from datetime import datetime
import html.parser


app = Flask(__name__)
POSTS_FOLDER = "posts"


# Classe per rimuovere i tag HTML in modo sicuro. Come se avessimo bisogno di un supereroe per questo!
class MLStripper(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return " ".join(self.fed)


# Filtri da usare nei template per rimuovere i tag HTML e formattare le date
@app.template_filter("striptags")
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


@app.template_filter("date")
def date_filter(s):
    return s.strftime("%d-%m-%Y")


# La pagina principale, dove mostriamo i sei post più recenti. Come una rivista settimanale!
@app.route("/", methods=["GET", "POST"])
def index():
    json_crud = JsonCrud(POSTS_FOLDER)
    all_posts = json_crud.read_all()
    # posts = [json.loads(p) for p in all_posts]
    for post in all_posts:
        post["dt_updated"] = datetime.fromisoformat(post["dt_updated"])
    all_posts.sort(key=lambda x: x["dt_updated"], reverse=True)

    return render_template("index.html", posts=all_posts[:6])


# La pagina "About". Per tutti coloro che vogliono sapere di più su noi (che siamo una squadra di superheroi dei JSON).
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


# Pagina del singolo post o dell'ultimo post se non viene specificato un id. Come se avessimo bisogno di un robot per fare questo lavoro!
@app.route("/post/", defaults={"id": None})
@app.route("/post/<id>", methods=["GET"])
def post(id):
    json_crud = JsonCrud(POSTS_FOLDER)
    bg_img = "/static/assets/img/post-bg.jpg"

    if id is None:
        all_posts = json_crud.read_all()
        # posts = [json.loads(p) for p in all_posts]
        for post in all_posts:
            post["dt_updated"] = datetime.fromisoformat(post["dt_updated"])
        all_posts.sort(key=lambda x: x["dt_updated"], reverse=True)
        return render_template("post.html", post=all_posts[0], bg_img=bg_img)
    else:
        post = json_crud.read_one(id)
        # post = json.loads(p)
        post["dt_updated"] = datetime.fromisoformat(post["dt_updated"])
        return render_template("post.html", post=post, bg_img=bg_img)


# La pagina di contatto. Come se avessimo bisogno di un assistente virtuale per gestire le richieste dei nostri fan!
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


# La pagina di login. Per i supereroi che vogliono accedere ai segreti della nostra squadra!
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


# La pagina amministrativa, dove possiamo gestire tutti i nostri posts come dei veri e propri direttori di giornale!
@app.route("/admin", methods=["GET"])
def admin():
    json_crud = JsonCrud(POSTS_FOLDER)
    all_posts = json_crud.read_all()
    # posts = [json.loads(p) for p in all_posts]
    for post in all_posts:
        post["dt_updated"] = datetime.fromisoformat(post["dt_updated"])
    all_posts.sort(key=lambda x: x["dt_updated"], reverse=True)
    return render_template("admin.html", posts=all_posts)


# Creazione di un nuovo post. Come se avessimo bisogno di una macchina da scrivere per farlo!
@app.route("/new_post", methods=["POST"])
def new_post():
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        abort(400, description="Invalid post data")
    post = {"title": data.get("title", ""), "content": data.get("content", "")}

    json_crud = JsonCrud(POSTS_FOLDER)
    json_crud.create(post)

    response = {"message": "Post created successfully"}
    return jsonify(response)


# Aggiornamento di un post esistente. Come se avessimo bisogno di un robot per farlo!
@app.route("/update_post", methods=["POST"])
def update_post():
    data = request.get_json()
    print(data)
    if (
        not data
        or not data.get("id")
        or (not data.get("title") and not data.get("content"))
    ):
        abort(400, description="Invalid post data")
    post_id = data.get("id")
    updated_post = {
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "dt_created": data.get("dt_created", ""),
    }

    json_crud = JsonCrud(POSTS_FOLDER)
    json_crud.update(post_id, updated_post)

    response = {"message": "Post updated successfully"}
    return jsonify(response)


# Ottieni un singolo post. Come se avessimo bisogno di una macchina del tempo per farlo!
@app.route("/get_post", methods=["POST"])
def get_post():
    data = request.get_json()
    if not data or not data.get("id"):
        abort(400, description="Invalid post ID")
    post_id = data.get("id")
    json_crud = JsonCrud(POSTS_FOLDER)
    post = json_crud.read_one(post_id)

    if not post:
        response = {"error": "Post not found"}
    else:
        response = post
    return jsonify(response)


# Ottieni tutti i posts. Come se avessimo bisogno di un elicottero per farlo!
@app.route("/get_posts", methods=["POST"])
def get_posts():
    json_crud = JsonCrud(POSTS_FOLDER)
    posts = json_crud.read_all()
    return jsonify(posts)


# Ottieni i sei post più recenti. Come se avessimo bisogno di un satellite per farlo!
@app.route("/get_latest_posts", methods=["POST"])
def get_latest_posts():
    json_crud = JsonCrud(POSTS_FOLDER)
    posts = json_crud.read_all()
    latest_posts = posts[:6]
    return jsonify(latest_posts)


# Cancellazione di un post. Come se avessimo bisogno di un robot distruttore per farlo!
@app.route("/delete_post/<id>", methods=["DELETE"])
def delete_post(id):
    json_crud = JsonCrud(POSTS_FOLDER)
    message = json_crud.delete(id)
    if "noPost-" + str(id) in message:
        response = {"error": message}
    else:
        response = {"message": "Post deleted successfully"}
    return jsonify(response)


# Avvio dell'app. Ecco, il momento che abbiamo aspettato! La nostra squadra dei supereroi è pronta!
if __name__ == "__main__":
    app.run(debug=True)
