from flask import Flask, render_template, url_for, request, redirect, jsonify, json
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['TESTING'] = True

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Norberta123!'
app.config['MYSQL_DATABASE_DB'] = 'books'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

data = {}

@app.route('/')
def hellowWorld():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT Books.*, BookAuthors.AuthorID, BookAuthors.Royalty FROM Books LEFT JOIN BookAuthors ON BookAuthors.BookID = Books.BookID")
    data['Books'] = cur.fetchall()
    cur.execute("SELECT * FROM Authors")
    data['Authors'] = cur.fetchall()
    cur.execute("SELECT * FROM Genres")
    data['Genres'] = cur.fetchall()
    cur.execute("SELECT * FROM Publishers")
    data['Publishers'] = cur.fetchall()
    cur.execute("SELECT * FROM BookAuthors")
    data['BookAuthors'] = cur.fetchall()
    print("HOME DATA")
    print(data)
    return render_template("index.html", data=data)

@app.route('/add_genre', methods=['POST'])
def add_genre():
    form = request.form
    gname = form['gname']
    gdesc = form['gdesc']
    try:
        form['gfic']
        gfic =1
    except:
        gfic =0

    cur = mysql.get_db().cursor()
    cur.execute('INSERT INTO Genres(GenreName, GenreDescription, Fiction) VALUES(%s, %s, %s)',(gname, gdesc, gfic))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/add_author', methods=['POST'])
def add_author():
    form = request.form
    fname = form['fname']
    lname = form['lname']
    phone = form['aphone']
    email = form['aemail']
    address = form['aaddress']
    city = form['acity']
    state = form['astate']

    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO Authors(FirstName, LastName, Phone, Email, Address, City, State) VALUES(%s, %s, %s, %s, %s, %s, %s)",(fname, lname, phone, email, address, city, state))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/add_publisher', methods=['POST'])
def add_publisher():
    form = request.form
    pname = form['pname']
    address = form['paddress']
    city = form['pcity']
    state = form['pstate']

    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO Publishers(PublisherName, Address,City, State) VALUES(%s, %s, %s, %s)",(pname, address, city, state))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/add_book', methods=['POST'])
def add_book():
    form = request.form
    pID = None if form['pID'] == "" else form['pID']
    gID = None if form['gID'] == "" else form['gID']
    title = form['title']
    unitprice = None if form['unitprice'] == "" else form['unitprice']
    print("Unit price: ", unitprice)
    contract = form['contract']
    comments = form['comments']
    pdate = None if form['pdate'] == "" else form['pdate']

    aID = None if form['aID'] == "" else form['aID']
    royalty = None if form['royalty'] == "" else form['royalty']

    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO Books(PublisherID, GenreID,Title, UnitPrice, Contract, Comments, PublicationDate) VALUES(%s, %s, %s, %s, %s, %s, %s)",(pID, gID, title, unitprice, contract, comments, pdate))
    mysql.get_db().commit()
    # bID = cur.execute("SELECT BookID FROM Books WHERE PublisherID=%s GenreID=%s Title=%s UnitPrice=%s Contract=%s Comments=%s PublicationDate=%s",(pID, gID, title, unitprice, contract, comments, pdate)).fetchone()
    bID = cur.lastrowid
    if (aID != None):
        cur.execute("INSERT INTO BookAuthors(AuthorID, BookID, Royalty) VALUES(%s, %s, %s)",(aID, bID, royalty))
        mysql.get_db().commit()
    
    return redirect(url_for('home'))

@app.route('/update_genre', methods=['POST'])
def update_genre():
    form = request.form
    gID = int(form['gID'])
    gname = form['gname']
    gdesc = form['gdesc']
    try:
        form['gfic']
        gfic =1
    except:
        gfic =0

    cur = mysql.get_db().cursor()
    cur.execute('UPDATE Genres SET GenreName=%s, GenreDescription=%s, Fiction=%s WHERE GenreID = %s',(gname, gdesc, gfic, gID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/update_author', methods=['POST'])
def update_author():
    form = request.form
    aID = form['aID']
    print(aID)
    fname = form['fname']
    lname = form['lname']
    phone = form['aphone']
    email = form['aemail']
    address = form['aaddress']
    city = form['acity']
    state = form['astate']

    cur = mysql.get_db().cursor()
    cur.execute("UPDATE Authors SET FirstName=%s, LastName=%s, Phone=%s, Email=%s, Address=%s, City=%s, State=%s WHERE AuthorID = %s",(fname, lname, phone, email, address, city, state, aID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/update_publisher', methods=['POST'])
def update_publisher():
    form = request.form
    pID = form["pID"]
    pname = form['pname']
    address = form['paddress']
    city = form['pcity']
    state = form['pstate']

    cur = mysql.get_db().cursor()
    cur.execute("UPDATE Publishers SET PublisherName =%s, Address=%s,City=%s, State=%s WHERE PublisherID =%s ",(pname, address, city, state,pID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/update_book', methods=['POST'])
def update_book():
    form = request.form
    bID = form['bID']
    pID = form['pID']
    gID = form['gID']
    title = form['title']
    unitprice = form['unitprice']
    contract = form['contract']
    comments = form['comments']
    pdate = form['pdate']

    aID = form['aID']
    royalty = form['royalty']

    print("aID:" + aID)

    cur = mysql.get_db().cursor()
    cur.execute("UPDATE Books SET PublisherID=%s, GenreID=%s,Title=%s, UnitPrice=%s, Contract=%s, Comments=%s, PublicationDate=%s WHERE BookID = %s",(pID, gID, title, unitprice, contract, comments, pdate,bID))
    mysql.get_db().commit()
    # bID = cur.execute("SELECT BookID FROM Books WHERE PublisherID=%s GenreID=%s Title=%s UnitPrice=%s Contract=%s Comments=%s PublicationDate=%s",(pID, gID, title, unitprice, contract, comments, pdate)).fetchone()
    # bID = cur.lastrowid

    cur.execute("UPDATE BookAuthors SET AuthorID=%s, Royalty=%s WHERE BookID = %s",(aID, royalty, bID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/delete_genre', methods=['POST'])
def delete_genre():
    print("Delete genre")
    gID = request.form["id"]
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM Genres WHERE GenreID = %s',(gID))
    mysql.get_db().commit()
    cur.execute("SELECT * FROM Genres")
    data['Genres'] = cur.fetchall()
    print(data["Genres"])
    return redirect(url_for('home'))

@app.route('/delete_author', methods=['POST'])
def delete_author():
    aID = request.form["id"]
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM Authors WHERE AuthorID = %s',(aID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/delete_publisher', methods=['POST'])
def delete_publisher():
    pID = request.form["id"]
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM Publishers WHERE PublisherID = %s',(pID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

@app.route('/delete_book', methods=['POST'])
def delete_book():
    bID = request.form["id"]
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM Books WHERE BookID = %s',(bID))
    mysql.get_db().commit()
    return redirect(url_for('home'))

def formStringToNull(form):
    for key in form:
        if form[key] == "":
            form[key] = None

if __name__ == '__main__':
    app.run(debug=True)