from flask import Flask, request, render_template, session, redirect, url_for
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

app.secret_key = "okimdimoskksdssdskdsd"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/picksmart"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define your model class for the 'signup' table
class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

trending_products = pd.read_csv("models/trending_products.csv")
df = pd.read_csv("models/clean_data.csv")

def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text


def content_based_recommendations(train_data, item_name, top_n=10):
    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in the training data.")
        return pd.DataFrame()
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    item_index = df[train_data['Name'] == item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n+1]
    recommended_items_indices = [x[0] for x in top_similar_items]
    recommended_items_details = df[['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']].take(recommended_items_indices)
    return recommended_items_details

random_image_urls = [
    "static/img/img9.jpeg",
    "static/img/img10.webp",
    "static/img/img_3.png",
    "static/img/img_4.png",
    "static/img/img_5.png",
    "static/img/img_6.png",
    "static/img/img_7.png",
    "static/img/img_8.png",
]

@app.route("/")
def index():
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [586, 2756, 960, 770, 1080, 1220, 1060, 500, 360, 750]
    random_prices = random.sample(price, len(trending_products))
    return render_template('index.html',
                           trending_products=trending_products.head(8),
                           truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_prices=random_prices)

@app.route('/main')
def main():
    content_based_rec = None
    message = "Welcome, to the main page"
    return render_template('main.html',content_based_rec=content_based_rec,message = message)

@app.route('/index')
def indexre():
    return render_template('index.html')

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        session['username'] = username
        content_based_rec = None
        message = "Welcome, you are successfully signed up!"

        return render_template('main.html', content_based_rec=content_based_rec, message=message)

# Route for signup page
@app.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']
        new_signup = Signin(username=username,password=password)
        db.session.add(new_signup)
        db.session.commit()
        session['username'] = username
        content_based_rec = None
        message = "Welcome, you are successfully signed in!"
        return render_template('main.html', content_based_rec=content_based_rec, message=message)

        # user = Signin.query.filter_by(username=username, password=password).first()
        # if user:
        #     session['username'] = username
        #     content_based_rec = None
        #     message = "Welcome, you are successfully signed in!"
        #     return render_template('main.html', content_based_rec=content_based_rec, message=message)
        # else:
        #     return redirect(url_for('index'))

# @app.route('/')
# def index():
#     user_authenticated = 'user' in session
#     return render_template('index.html', user_authenticated=user_authenticated)

@app.route('/home')
def home():
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [586, 2756, 960, 770, 1080, 1220, 1060, 500, 360, 750]
    random_prices = random.sample(price, len(trending_products))
    user_authenticated = 'user' in session
    return render_template('index.html',
                           user_authenticated=user_authenticated,
                           trending_products=trending_products.head(8),
                           truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_prices=random_prices
                           )

@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_rec = content_based_recommendations(df, prod, top_n=nbr)

        if content_based_rec.empty:
            message = "No recommendations available for this product."
            return render_template('main.html', message=message, content_based_rec=content_based_rec)
        else:
            # Create a list of random image URLs for each recommended product
            random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
            print(content_based_rec)
            print(random_product_image_urls)
            price = [586, 2756, 960, 770, 1080, 1220, 1060, 500, 360, 750]
            random_prices = random.sample(price, len(trending_products))
            return render_template('main.html',
                                   content_based_rec=content_based_rec,
                                   truncate=truncate,
                                   random_product_image_urls=random_product_image_urls,
                                   random_prices=random_prices
                                   )


if __name__ == '__main__':
    app.run(debug=True)

