from flask import Flask, render_template, request, redirect, url_for,flash,session,jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_inventory.sqlite3'  
app.secret_key = 'mithra11'
conn = sqlite3.connect('user_registration.db')
cursor = conn.cursor()

# Create a table to store user registration information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        gender TEXT, 
        phone TEXT
    )
''')

conn.commit()
conn.close()
conn = sqlite3.connect('food_inventory.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        expiration_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()
conn.close()




@app.route('/',methods=['GET'])
def index():
    # Connect to the database and fetch the inventor
    # conn = sqlite3.connect('food_inventory.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM inventory')
    # inventory = cursor.fetchall()
    # conn.close()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the provided email and password match a user in the database
        conn = sqlite3.connect('user_registration.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            # User is authenticated, set up the session
            session['logged_in'] = True
            session['user_id'] = user[0]
            flash(f'Successfully you have logged in ',category='success')

            # flash('Login successful!', 'success')
            return redirect(url_for('food_inventory'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['id']
        email = request.form['email']
        password = request.form['pwd']
        confirm_password = request.form['PWD']
        gender = request.form['gender']  # Get the gender from the form
        phone  = request.form['phone']    # Get the phone number from the form

        # Check if the password and confirm password match
        if password != confirm_password:
            flash('Password and Confirm Password do not match.', 'danger')
        else:
            # Check if the email already exists in the database
            conn = sqlite3.connect('user_registration.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already exists. Please choose a different email.', 'danger')
                return redirect(url_for('register'))
            else:
                # Insert the user into the database (you should hash the password in a real application)
                cursor.execute('INSERT INTO users (name, email, password, gender, phone) VALUES (?, ?, ?, ?, ?)',
                            (name, email, password, gender, phone ))
                conn.commit()
                conn.close()

                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/food_inventory', methods=['GET', 'POST'])
def food_inventory():
    return render_template('food_inventory.html')


#from datetime import datetime


@app.route('/products')
def products():
    user_id = session.get('user_id')
    conn = sqlite3.connect('food_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE user_id=?', (user_id,))
    inventory = cursor.fetchall()
    conn.close()
    return render_template('products.html', inventory=inventory)


 
recipes = [
    {
        'name': 'Spaghetti Carbonara',
        'description': 'A classic Italian pasta dish with creamy sauce and crispy bacon.',
        'instructions': [
            'Cook spaghetti according to package instructions.',
            'Fry pancetta or bacon until crispy; remove from heat.',
            'In a bowl, whisk eggs and mix in grated cheeses and minced garlic.',
            'Drain cooked spaghetti, add egg mixture, and toss until creamy.',
            'Stir in crispy pancetta or bacon. Serve hot.'
        ]
    },
    {
        'name': 'Chicken Alfredo',
        'description': 'Creamy and delicious chicken Alfredo pasta.',
        'instructions': [
            'Cook fettuccine pasta according to package instructions.',
            'Season chicken breasts with salt and pepper, then grill or pan-fry until cooked through. Slice into strips.',
            'In a saucepan, melt butter and sauté garlic until fragrant. Add heavy cream and Parmesan cheese, stirring until the sauce thickens.',
            'Toss cooked pasta with the Alfredo sauce and top with sliced chicken. Serve hot.'
        ]
    },
    {
        'name': 'Vegetable Stir-Fry',
        'description': 'A quick and healthy vegetable stir-fry with a savory soy-based sauce.',
        'instructions': [
            'Heat vegetable oil in a wok or large skillet over high heat. Add garlic and stir-fry for 30 seconds.',
            'Add broccoli, bell pepper, carrot, snap peas, and mushrooms. Stir-fry for 3-5 minutes until vegetables are tender-crisp.',
            'In a small bowl, whisk together soy sauce and honey. Pour over the vegetables and stir-fry for an additional 2 minutes.',
            'Serve the vegetable stir-fry over cooked rice or noodles.'
        ]
    },
    {
        'name': 'Chocolate Chip Cookies',
        'description': 'Classic chocolate chip cookies that are soft and chewy.',
        'instructions': [
            'Preheat the oven to 350°F (175°C) and line baking sheets with parchment paper.',
            'In a large bowl, cream together butter, granulated sugar, and brown sugar until light and fluffy.',
            'Beat in eggs one at a time, then stir in vanilla.',
            'In a separate bowl, whisk together flour, baking soda, and salt. Gradually add the dry ingredients to the wet ingredients and mix until just combined.',
            'Stir in the chocolate chips.',
            'Drop rounded tablespoons of cookie dough onto the prepared baking sheets and bake for 10-12 minutes until golden brown.',
            'Allow the cookies to cool on the baking sheets for a few minutes before transferring them to wire racks to cool completely.'
        ]
    },
    {
        'name': 'Caesar Salad',
        'description': 'A refreshing Caesar salad with crisp lettuce, croutons, and a creamy Caesar dressing.',
        'instructions': [
            'Tear the lettuce into bite-sized pieces and place in a large salad bowl.',
            'Add croutons and grated Parmesan cheese to the lettuce.',
            'In a small bowl, whisk together mayonnaise, lemon juice, Dijon mustard, and minced garlic to make the dressing.',
            'Drizzle the dressing over the salad and toss to coat.',
            'Serve the Caesar salad with additional Parmesan cheese and freshly ground black pepper.'
        ]
    },
    {
        'name': 'Tomato Basil Pasta',
        'description': 'A simple and flavorful pasta dish with fresh tomatoes, basil, and garlic.',
        'instructions': [
            'Cook your favorite pasta according to package instructions.',
            'In a pan, heat olive oil and sauté minced garlic until fragrant.',
            'Add diced tomatoes and cook for a few minutes until they soften.',
            'Toss the cooked pasta with the tomato mixture and fresh basil leaves.',
            'Season with salt, pepper, and grated Parmesan cheese.',
            'Serve the tomato basil pasta with a drizzle of olive oil.'
        ]
    },

    
    {
        'name': 'Chicken Tikka Masala',
        'description': 'A flavorful Indian dish with marinated chicken in a creamy tomato sauce.',
        'instructions': [
            'Marinate chicken pieces in yogurt and spices for at least 30 minutes.',
            'Grill or broil the chicken until cooked and slightly charred.',
            'In a separate pan, heat oil and sauté onions and garlic until soft.',
            'Add tomato sauce, heavy cream, and spices to make the sauce.',
            'Simmer the sauce and add grilled chicken. Serve with rice or naan.'
        ]
    },
    {
        'name': 'Caprese Salad',
        'description': 'A simple Italian salad with fresh tomatoes, mozzarella, basil, and balsamic glaze.',
        'instructions': [
            'Slice fresh tomatoes and mozzarella cheese into rounds.',
            'Layer tomato, mozzarella, and fresh basil leaves on a plate.',
            'Drizzle with balsamic glaze and a sprinkle of salt and pepper.',
            'Serve as an appetizer or side dish.'
        ]
    },
    {
        'name': 'Grilled Salmon',
        'description': 'Healthy and delicious grilled salmon with lemon and herbs.',
        'instructions': [
            'Season salmon fillets with salt, pepper, and fresh herbs (e.g., dill or rosemary).',
            'Grill salmon on medium-high heat for 4-5 minutes per side until it flakes easily with a fork.',
            'Squeeze fresh lemon juice over the grilled salmon before serving.'
        ]
    },

    {
        'name': 'Mushroom Risotto',
        'description': 'A creamy and comforting Italian rice dish with mushrooms and Parmesan cheese.',
        'instructions': [
            'Sauté sliced mushrooms and onions in butter until they are soft and golden.',
            'Add Arborio rice and stir until it coated with butter.',
            'Gradually add warm chicken or vegetable broth, stirring continuously until absorbed.',
            'Finish with grated Parmesan cheese and a drizzle of truffle oil if desired.'
        ]
    },
    {
        'name': 'Greek Salad',
        'description': 'A refreshing salad with cucumbers, tomatoes, olives, feta cheese, and Greek dressing.',
        'instructions': [
            'Dice cucumbers, tomatoes, and red onions and place them in a bowl.',
            'Add Kalamata olives and crumbled feta cheese.',
            'Drizzle with Greek dressing (olive oil, lemon juice, garlic, and oregano).',
            'Toss and serve as a side dish or light meal.'
        ]
    },
    
    {
        'name': 'Beef Stroganoff',
        'description': 'A rich and creamy Russian dish with tender beef and mushrooms.',
        'instructions': [
            'Sauté sliced onions and mushrooms in butter until they are tender.',
            'Add thinly sliced beef and cook until browned.',
            'Stir in sour cream, Dijon mustard, and beef broth.',
            'Simmer until the sauce thickens, and serve over egg noodles or rice.'
        ]
    },
    {
        'name': 'Vegetarian Chili',
        'description': 'A hearty and flavorful chili made with beans, vegetables, and spices.',
        'instructions': [
            'Sauté onions, bell peppers, and garlic in olive oil until softened.',
            'Add canned tomatoes, kidney beans, black beans, and spices.',
            'Simmer for 30 minutes until flavors meld together.',
            'Serve with shredded cheese, sour cream, and chopped cilantro.'
        ]
    },
    {
        'name': 'Homemade Pizza',
        'description': 'Create your pizza masterpiece with fresh dough and your favorite toppings.',
        'instructions': [
            'Preheat your oven to 475°F (245°C) and place a pizza stone or baking sheet inside.',
            'Roll out pizza dough into a circle and transfer it to a floured pizza peel or baking sheet.',
            'Spread tomato sauce, cheese, and your choice of toppings on the dough.',
            'Bake for 10-12 minutes until the crust is golden and the cheese is bubbly.'
        ]
    },
    {
        'name': 'Thai Green Curry',
        'description': 'A fragrant and spicy Thai curry with coconut milk, vegetables, and chicken or tofu.',
        'instructions': [
            'In a pan, sauté green curry paste in coconut oil until fragrant.',
            'Add coconut milk, sliced bell peppers, bamboo shoots, and protein (chicken or tofu).',
            'Simmer until everything is cooked and flavors meld together.',
            'Serve with jasmine rice and garnish with fresh basil leaves.'
        ]
    },
    {
        'name': 'Homemade Guacamole',
        'description': 'A simple and delicious dip made with ripe avocados, tomatoes, onions, and lime juice.',
        'instructions': [
            'Mash ripe avocados in a bowl and add diced tomatoes, minced onions, and lime juice.',
            'Season with salt and pepper and stir in chopped cilantro.',
            'Serve with tortilla chips or as a topping for tacos and burritos.'
        ]
    }

]



@app.route('/recipe_suggestion', methods=['GET', 'POST'])
def recipe_suggestion():
    if request.method == 'POST':
        # Generate a random recipe suggestion
        suggested_recipe = random.choice(recipes)
        # print("Suggested Recipe:", suggested_recipe)
        return render_template('suggestion.html', suggested_recipe=suggested_recipe)
    return render_template('suggestion.html', suggested_recipe=None)




@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        user_id = session['user_id']

        if request.method == 'POST':
            # Handle form submission for editing profile
            new_name = request.form['name']
            new_email = request.form['email']
            

            # Update the user's profile in the database
            conn = sqlite3.connect('user_registration.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (new_name, new_email, user_id))
            conn.commit()
            conn.close()

            flash('Profile updated successfully!', 'success')

        # Retrieve user data from the database based on user_id
        conn = sqlite3.connect('user_registration.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user_name = user_data[1]
            user_email = user_data[2]
            user_phone = user_data[5]
            return render_template('profile.html', user_name=user_name, user_email=user_email,user_phone=user_phone)

    # If the user is not logged in, redirect them to the login page
    #return redirect(url_for('login'))

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        # Find the item in the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        item_id_to_delete = item_id # Replace with the actual item ID you want to delete
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id_to_delete,))
        conn.commit()
        conn.close()
        # Return a JSON response indicating success
        return jsonify(message='Item deleted successfully'), 204  # 204 No Content status code
    except Exception as e:
        # Handle errors and return an error response
        session.rollback()
        return jsonify(error=str(e)), 500


@app.route('/fruits_inventory',methods=['GET','POST'])
def fruits_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('fruits_inventory.html')

@app.route('/vegetable_inventory',methods=['GET','POST'])
def vegetable_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        # conn = sqlite3.connect('food_inventory.db')
        # cursor = conn.cursor()
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        # cursor.execute('INSERT INTO inventory (item_name, quantity, expiration_date) VALUES (?, ?, ?)',
        #                (item_name, quantity, expiration_date))
        # conn.commit()
        # conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('vegetable_inventory.html')


@app.route('/meat_inventory',methods=['GET','POST'])
def meat_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('meat_inventory.html')

@app.route('/beverage_inventory',methods=['GET','POST'])
def beverage_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('beverage_inventory.html')

@app.route('/pantry_inventory',methods=['GET','POST'])
def pantry_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('pantry_inventory.html')

@app.route('/snacks_inventory',methods=['GET','POST'])
def snacks_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('snacks_inventory.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('index')) 
if __name__ == '__main__':
    app.run(debug=True)
