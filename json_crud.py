import json
import os
from datetime import datetime
import uuid


class JsonCrud:
    def __init__(self, folder_path):
        # Iniziamo il viaggio nel mondo dei JSON!
        self.folder_path = folder_path
        # Ecco, ora abbiamo tutti i nostri post pronti per la festa...
        self.posts = self.read_all()

    def read_all(self):
        posts = []
        # Ah ah! Stiamo cercando di rubare tutti i file JSON del nostro amico!
        for f in os.listdir(self.folder_path):
            if f.endswith(".json"):
                with open(os.path.join(self.folder_path, f), "r") as file:
                    post = json.load(file)
                    posts.append(post)
        return posts

    def read_one(self, id):
        filename = os.path.join(self.folder_path, f"{id}.json")
        # Tenta di rubare un singolo file JSON. Se non lo trova, ci scusiamo gentilmente...
        if not os.path.isfile(filename):
            return None
        with open(filename, "r") as file:
            return json.load(file)

    def create(self, post):
        post_id = str(uuid.uuid4())
        # Oh no! Abbiamo perso l'id del nostro nuovo post in mezzo al mare delle UUID...
        post["id"] = post_id
        # Ecco finalmente il timestamp della sua nascita!
        post["dt_created"] = datetime.now().isoformat()
        # Non dimentichiamo di aggiornare anche la sua data di ultima modifica, perché è importante essere in forma!
        post["dt_updated"] = datetime.now().isoformat()
        with open(os.path.join(self.folder_path, f"{post_id}.json"), "w") as file:
            json.dump(post, file, indent=4)
        # E infine lo aggiungiamo alla nostra collezione di post. È un membro della famiglia ora!
        self.posts.append(post)

    def update(self, id, post):
        post["id"] = id
        # Ooooh! Un aggiornamento per uno dei nostri cari membri! Non possiamo dimenticare di segnare la data...
        post["dt_updated"] = datetime.now().isoformat()
        filename = os.path.join(self.folder_path, f"{id}.json")
        with open(filename, "w") as file:
            json.dump(post, file, indent=4)
        # Aggiorniamo anche la nostra lista dei post in memoria per rimanere al passo con le novità!
        for i, p in enumerate(self.posts):
            if str(p["id"]) == str(id):
                self.posts[i] = post
                break

    def delete(self, id):
        filename = os.path.join(self.folder_path, f"{id}.json")
        # Oh no! Un membro della nostra famiglia sta per andare via... ci dispiace ma a volte è necessario...
        if os.path.exists(filename):
            os.remove(filename)
            for i, p in enumerate(self.posts):
                if str(p["id"]) == str(id):
                    del self.posts[i]
                    break
        else:
            # Ah ah! Lo abbiamo cercato dappertutto ma sembra che sia già scomparso senza lasciare traccia!
            return "noPost" + str(id)
