import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from PIL import Image
from forms import ImageForm
from services import get_translation, get_random_file_name

app = Flask(__name__)
app.secret_key = '<secret key>'

if os.path.isdir("static/temp_images") is False:
    os.mkdir("static/temp_images")

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# print(pytesseract.get_languages(config=''))


@app.route("/", methods=['POST', 'GET'])
def home():
    form = ImageForm()

    #clear temp files
    session_temp_file = session.get('res_img', None)
    if session_temp_file:
        try:
            os.remove(rf"static\temp_images\{session_temp_file}")
        except FileNotFoundError:
            pass

    if form.validate_on_submit():
        # try:
            dest_lang = form.lang_select.data
            file_ext = os.path.splitext(form.image.data.filename)[1]
            random_file_name = get_random_file_name() + file_ext

            picture_path = os.path.join(app.root_path, 'static/temp_images', random_file_name)
            i = Image.open(form.image.data)
            i.save(picture_path)

            translated_text = get_translation(filename=random_file_name, dest_lang=dest_lang)

            result_img = os.path.splitext(random_file_name)[0] + "-res" + os.path.splitext(random_file_name)[1]
            session["res_img"] = result_img
            session["translation"] = translated_text

            return redirect(url_for("res"))
        # except IndexError:
        #     flash(f"Something went wrong, try again with different image", "warning")
        #     return render_template("home.html", form=form)

    return render_template("home.html", form=form)


@app.route("/res")
def res():
    global res_img_name

    if session.get('res_img', None):
        res_img_name = session.get('res_img', None)
        translation = session.get('translation', None)

        return render_template("res.html", res_img_name=res_img_name, translation=translation)
    else:
        return redirect(url_for('home'))


@app.after_request
def delete_image(response):
    if request.endpoint == "res" and session.get('res_img', None):
        try:
            os.remove(rf"static\temp_images\{res_img_name.replace('-res', '')}")
        except FileNotFoundError:
            pass

    return response


if __name__ == '__main__':
    app.run(debug=True)
