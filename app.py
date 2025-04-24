from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'zAir_Wreck889JulyPepsiVVIIdbfen'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    flash('Please log in to access this page.')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = None
    if request.method == 'POST':
        username = request.form['username']
        login_password = request.form['login_password']

        conn = get_db_connection()
        user = conn.execute('''
            SELECT * FROM Gamers
            WHERE name = ? AND login_password = ?
        ''', (username, login_password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['name']
            return redirect(url_for('home'))
        else:
            error_msg = "Invalid username or password."

    return render_template('login.html', error_msg=error_msg)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        login_password = request.form['login_password']

        errors = []
        if not name or not age or not email or not login_password:
            errors.append("All fields are required.")
        if not age.isdigit():
            errors.append("Age must be an integer.")

        if errors:
            return render_template('add_user.html', errors=errors, name=name, age=age,
                                   email=email, login_password=login_password)

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO Gamers (name, age, email, login_password)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, login_password))
        conn.commit()
        conn.close()

        flash('User added successfully!')
        return redirect(url_for('home'))

    return render_template('add_user.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        name_of_game = request.form['name_of_game']
        year = request.form['year']
        genre = request.form['genre']
        version = request.form['version']
        age_restriction = request.form['age_restriction']
        price = request.form['price']
        did = request.form['did']
        rate = request.form['rate']

        errors = []
        if not name_of_game:
            errors.append("Name of game item is required.")
        if not year.isdigit():
            errors.append("Year must be an integer.")
        if not version.isdigit():
            errors.append("Version must be an integer.")
        if not did.isdigit():
            errors.append("ID must be an integer.")
        try:
            float(price)
        except:
            errors.append("Price must be a number.")
        try:
            float(rate)
        except:
            errors.append("Rate must be a number.")

        if errors:
            return render_template(
                'add_entry.html',
                errors=errors,
                name_of_game=name_of_game,
                year=year,
                genre=genre,
                version=version,
                age_restriction=age_restriction,
                price=price,
                did=did,
                rate=rate
            )

        user_id = session.get('user_id')
        if not user_id:
            flash('You must be logged in to add an entry.')
            return redirect(url_for('login'))

        try:
            with get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO Games (
                        user_id, name_of_game, year, genre, version,
                        age_restriction, price, did, rate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, name_of_game, year, genre, version,
                      age_restriction, price, did, rate))
                conn.commit()
            flash('Game entry added successfully!')
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('home'))

    return render_template('add_entry.html')

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if 'user_id' not in session:
        flash("You must be logged in to leave a review.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    games = conn.execute('SELECT entry_id, name_of_game FROM Games').fetchall()

    if request.method == 'POST':
        entry_id = request.form.get('entry_id')
        review_text = request.form.get('review_text')
        stars = request.form.get('stars')

        errors = []

        if not entry_id or not stars:
            errors.append("Game and star rating are required.")
        elif not stars.isdigit() or int(stars) < 1 or int(stars) > 5:
            errors.append("Stars must be an integer between 1 and 5.")

        if errors:
            return render_template('add_review.html', errors=errors, games=games,
                                   review_text=review_text, stars=stars)

        user_id = session['user_id']

        try:
            conn.execute('''
                INSERT INTO Reviews (user_id, entry_id, review_text, stars)
                VALUES (?, ?, ?, ?)
            ''', (user_id, entry_id, review_text, stars))
            conn.commit()
            flash("Review submitted successfully!")
            return redirect(url_for('list_reviews'))
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
            return render_template('add_review.html', games=games, errors=["Could not add review."])

    return render_template('add_review.html', games=games)

@app.route('/list_results')
def list_results():
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM Games').fetchall()
    conn.close()
    return render_template('list_results.html', results=entries)

@app.route('/list_reviews')
def list_reviews():
    conn = get_db_connection()

    reviews = conn.execute('''
        SELECT Reviews.review_id, Gamers.name AS reviewer_name,
               Games.name_of_game, Reviews.review_text, Reviews.stars,
               (SELECT AVG(r2.stars)
                FROM Reviews r2
                WHERE r2.entry_id = Reviews.entry_id) AS average_game_rating
        FROM Reviews
        LEFT JOIN Gamers ON Reviews.user_id = Gamers.id
        LEFT JOIN Games ON Reviews.entry_id = Games.entry_id
    ''').fetchall()

    conn.close()
    return render_template('list_reviews.html', reviews=reviews)

@app.route('/top_rated_games')
def top_rated_games():
    conn = get_db_connection()
    top_games = conn.execute('''
        SELECT Games.name_of_game, AVG(Reviews.stars) AS avg_rating
        FROM Reviews
        JOIN Games ON Reviews.entry_id = Games.entry_id
        GROUP BY Reviews.entry_id
        HAVING avg_rating >= 4
    ''').fetchall()
    conn.close()
    return render_template('top_rated_games.html', games=top_games)



@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'user_id' not in session:
        flash("You must be logged in to delete a review.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    # Only allow user to delete their own reviews
    conn.execute('DELETE FROM Reviews WHERE review_id = ? AND user_id = ?', (review_id, session['user_id']))
    conn.commit()
    conn.close()

    flash("Review deleted successfully.")
    return redirect(url_for('list_reviews'))


@app.route('/list_users')
def list_users():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Gamers').fetchall()
    conn.close()

    return render_template('list_users.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/not_found')
def not_found():
    return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)
