from flask import Blueprint, request, render_template, redirect, make_response, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import config
from pymongo import MongoClient
from gridfs import GridFS



# /auth
bp = Blueprint("reading", __name__, url_prefix="/reading")
#client = MongoClient('mongodb://localhost:27017/')
#db = client['acl_bibs']
#gfs = GridFS(db, collection="pdf")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.ALLOW_EXTENSION


@bp.route("/",methods=['GET','POST'])
def upload():
    global filename
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
        else:
            filename = secure_filename(file.filename)
            #kwargs = {"filename": filename, "content_type": "PDF"}
            #gfs.put(file, **kwargs)
            uploadpath = os.path.join(config.UPLOAD_FOLDER, filename)
            file.save(uploadpath)
        return redirect(url_for('reading.viewer', filename=filename))
    return render_template("literature reading.html")

@bp.route("/viewer/<filename>")
def viewer(filename):
    src = 'http://127.0.0.1:5000/static/pdfjs/web/viewer.html?file=\\static\\uploads\\'+filename
    return render_template("viewer.html", src=src)



