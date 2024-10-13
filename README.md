# TrendPick - Product Recommendation System
PickSmart is a Flask-based web application designed to provide personalized product recommendations based on product content. Using machine learning techniques like TF-IDF vectorization and cosine similarity, the application suggests similar products based on user input. It also features user authentication and displays trending products with dynamic images and prices.

<h1>Features</h1>
User Authentication: Users can sign up, sign in, and sign out.
Trending Products: Displays a list of trending products on the homepage with random prices and images.
Content-Based Recommendation: Recommends similar products using TF-IDF and cosine similarity based on product tags.
Dynamic Image and Price Assignment: Each product is displayed with random images and prices for variety.

<h1>Technologies Used</h1>
<ul>
<li>Flask: Web framework for the backend.</li>
<li>MySQL: Database for storing user authentication data.</li>
<li>Pandas: Used for managing and manipulating product data.</li>
<li>Scikit-learn: For TF-IDF vectorization and cosine similarity computations.</li>
</ul>

<h1>How to Run the Project Locally</h1>
Prerequisites
<ul>
<li>Python 3.x</li>
<li>MySQL Database</li>
<li>Virtual Environment (optional but recommended)</li></ul>

<h1>Installation Steps</h1>
Clone the Repository

```bash
  git clone https://github.com/your-username/TrendPick.git
  cd TrendPick
```
Set Up a Virtual Environment (Optional)

```bash
  python3 -m venv venv
  source venv/bin/activate  # For Windows: venv\Scripts\activate
```

Install Required Packages
Install the dependencies from the requirements.txt file:

```bash
  pip install -r requirements.txt
```
<h1>Set Up MySQL Database</h1>
Create a MySQL database named TrendPick
Update the MySQL username and password in the app.config['SQLALCHEMY_DATABASE_URI'] inside main.py:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:yourpassword@localhost/picksmart"
```

<h2>Create the necessary tables for user authentication:</h2>

```bash
Copy code
flask shell
>>> from main import db
>>> db.create_all()
>>> exit()
```
<h2>Dataset Used</h2>
The product data for this project is sourced from the Walmart Product Data available on Kaggle. The dataset includes a variety of product details such as:

<h2>Product names</h2>
Tags (used for similarity calculations)
<li>Review counts</li>
<li>Ratings</li>
<li>Brand</li>
<li>Image URLs</li>
  
<h1>Prepare CSV Files</h1>
Ensure the following CSV files are placed in the models/ directory:

<li>trending_products.csv: Contains trending products data.</li>
<li>clean_data.csv: Contains product details for recommendations.</li>

<h2>Run the Flask Application</h2>

To start the Flask development server, run:

```bash
python main.py
```

Access the Application

Open your browser and go to:

```arduino
http://127.0.0.1:5000/
```

<h1>Model Used</h1>
The recommendation system is based on content-based filtering using TF-IDF vectorization to analyze the similarity between products' tags. The model then computes cosine similarity between products and suggests the top-N similar items to the user.

