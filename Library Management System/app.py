from flask import Flask, render_template, request, redirect
import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["library"]
mycol = mydb["book"]
print("Connected to database.")
collist = mydb.list_collection_names()
if "book" in collist:
    print("The 'book' collection exists.")

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def form():
    return render_template('home.html')
    
@app.route('/get', methods=['GET', 'POST'])
def get():
    bname= request.form.get('bname')
    bcategory = request.form.get('bcategory')
    language = request.form.get('language')
    byear = request.form.get('byear')
    bnumber = request.form.get('bnumber')
    print(bname)
    book = {
        "bname": bname,
        "bcategory": bcategory,
        "language": language,
        "byear": byear,
        "bnumber": bnumber
    }
    try:
        book_id = mycol.insert_one(book).inserted_id
        print("Record added to 'book' collection with ID:", book_id)
        text="0"
        return render_template('home.html', success=text)
    except Exception as e:
        text="1"
        print("Error:", e)
        return render_template('home.html', success=text)

@app.route('/table', methods=['GET', 'POST'])
def table():
    books = mycol.find()
    return render_template('table.html', books=books)

@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    if request.method == 'GET':
        book = mycol.find_one({"_id": ObjectId(book_id)})
        return render_template('edit.html', book=book)
    elif request.method == 'POST':
        bname= request.form.get('bname')
        bcategory = request.form.get('bcategory')
        language = request.form.get('language')
        byear = request.form.get('byear')
        bnumber = request.form.get('bnumber')
        newvalues = {
            "$set": {
                "bname": bname,
                "bcategory": bcategory,
                "language": language,
                "byear": byear,
                "bnumber": bnumber
            }
        }
        mycol.update_one({"_id": ObjectId(book_id)}, newvalues)
        return redirect('/table')
    
@app.route('/delete/<book_id>', methods=['GET', 'POST'])
def delete(book_id):
    try:
        mycol.delete_one({"_id": ObjectId(book_id)})
        print("Record with ID", book_id, "deleted from 'book' collection")
    except Exception as e:
        print("Error:", e)
    return redirect('/table')
    
if __name__ == '__main__':
    app.run(debug=True)
