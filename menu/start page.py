from loginform import LoginForm
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# папка для сохранения загруженных файлов
# (должна существовать в папке instance, которая находится в одном каталоге с программой)
UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = {'zip'}
LOADED = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploads_dir = os.path.join(app.instance_path, 'uploads')


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            f = request.files['file']
            print(f.read())
            LOADED = True
            return "Форма отправлена"
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect('/upload_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'tasks'
            file.save(os.path.join(uploads_dir, filename))

            return redirect(url_for('ok'))
    return render_template('upload.html')


@app.route('/ok', methods=['POST', 'GET'])
def ok():
    if request.method == 'POST':
        if request.form['submit_button'] == 'reload':
            return redirect(url_for('upload_file'))
        elif request.form['submit_button'] == 'start':
            pass  # отправляется разрешение Даниному сайту запускать игру
    form = LoginForm()
    '''if form.validate_on_submit():
        return redirect('/upload_file')'''
    return render_template('start.html', title='menu', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
