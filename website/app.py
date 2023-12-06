import shutil
from flask import Flask, g,render_template,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from flask_ckeditor import CKEditor
import torch
import torch.nn as nn
import torch.optim as optim
from math import ceil
from torchvision import models, transforms
from PIL import Image
from segmentation_model import UNet
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from scipy.ndimage import zoom
from mammography import *
from nii_codes import *
from gpt import *


model_path = r".\static\assets\models\brain.pth"
composition_weights = r".\static\assets\models\composition_weight.pth"
birads_weights = r".\static\assets\models\birads_weight.pth"


# Kullanıcı Giriş Decorator
def login_required_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in_patient" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("forbidden"))           
    return decorated_function


def login_required_doctor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in_doctor" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("forbidden"))           
    return decorated_function


app = Flask(__name__)
app.secret_key = "ai_nabiz"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "yz_nabiz"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["UPLOAD_FOLDER"] = "static/assets/images/uploads"
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

mysql = MySQL(app)
ckeditor = CKEditor(app)

@app.context_processor
def inject_user():
    patient_info = None
    if "logged_in_patient" in session:
        patient_info = {
            "ID": session.get("ID"),
            "FirstName": session.get("FirstName"),
            "LastName": session.get("LastName"),
            "Email": session.get("Email"),
            "Password": session.get("Password"),
            "DateOfBirth": session.get("DateOfBirth"),
            "Gender": session.get("Gender"),
            "BloodGroup": session.get("BloodGroup"),
        }
    else:
        data = None
    return dict(patient_info=patient_info)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route("/403")
def forbidden():
    return render_template("403.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index")
def index2():
    return render_template("index.html")

@app.route("/intellicut")
def intellicut():
    return render_template("intellicut.html")

@app.route("/mammodes")
def mammodes():
    return render_template("mammodes.html")

@app.route("/kidneyvitality")
def kidneyvitality():
    return render_template("kidneyvitality.html")

@app.route("/kvkk")
def kvkk():
    return render_template("kvkk.html")

@app.route("/bilgi_guvenligi")
def bilgi_guvenligi():
    return render_template("bilgi_guvenligi.html")

@app.route("/aydinlatma_metni")
def aydinlatma_metni():
    return render_template("aydinlatma_metni.html")

@app.route("/saklamaveimha")
def saklamaveimha():
    return render_template("saklamaveimha.html")


@app.route("/login_patient", methods=["GET", "POST"])
def login_patient():
    session.clear()
    if request.method == "POST":
        TCNumber = request.form.get('TCNumber')
        Password = request.form.get('password')
        cursor = mysql.connection.cursor()
        query = "Select * from patients where TCNumber = %s"
        result = cursor.execute(query,(TCNumber,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data["Password"]
            if(sha256_crypt.verify(Password,real_password)):
                session["logged_in_patient"] = True
                session["ID"] = data["ID"]
                session["TCNumber"] = data["TCNumber"]
                session["FirstName"] = data["FirstName"]
                session["LastName"] = data["LastName"]
                session["Email"] = data["Email"]
                session["DateOfBirth"] = data["DateOfBirth"]
                session["Gender"] = data["Gender"]
                session["BloodGroup"] = data["BloodGroup"]
                return redirect(url_for("patient_home"))
            else:
                print("Parola Yanlış")
                return redirect(url_for("login_patient"))
        else:
            print("TC Kimlik Yanlış. Kullanıcı Bulunamadı!")
            return redirect(url_for("login_patient"))
    else:
        return render_template("login_patient.html")




@app.route("/logout_patient")
def logout_patient():
    session.clear()
    return redirect(url_for("index"))




@login_required_user
@app.route("/layout_patient", methods=["GET"])
def layout_patient():
    if request.method == "GET":
        data = {
            "ID": session.get("ID"),
            "FirstName": session.get("FirstName"),
            "LastName": session.get("LastName"),
            "Email": session.get("Email"),
            "Password": session.get("Password"),
            "DateOfBirth": session.get("DateOfBirth"),
            "Gender": session.get("Gender"),
            "BloodGroup": session.get("BloodGroup"),
        }
        return render_template("layout_patient.html", patient_info=data)
    else:
        return render_template("layout_patient.html", patient_info=data)



@login_required_user
@app.route("/patient_home")
def patient_home():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    cursor1 = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    cursor3 = mysql.connection.cursor()
    query = "Select * from hospitalvisits where PatientTC = %s LIMIT 5" 
    query2 = "SELECT HospitalName, TestDate, COUNT(*) as Total FROM laboratoryresults WHERE PatientTC = %s GROUP BY TestDate LIMIT 5 "
    query3 = "Select * from radiologyimages where PatientTC = %s LIMIT 5"
    cursor.execute(query,(TCNumber,))
    cursor2.execute(query2,(TCNumber,))
    cursor3.execute(query3,(TCNumber,))
    patientData = cursor.fetchall()
    patient_appointments = cursor2.fetchall()
    radiology_images = cursor3.fetchall()
    all_visits = []
    for visit in patientData:
        query1 = "Select * from doctors where TCNumber = %s LIMIT 5"
        cursor1.execute(query1,(visit["DoctorTC"],))
        doctorData = cursor1.fetchone()
        visit_info = {"visit": visit, "doctor": doctorData}
        all_visits.append(visit_info)
    return render_template("patient_home.html", visits=all_visits, patient_appointments=patient_appointments, radiology_images=radiology_images)


@login_required_user
@app.route("/bloody_results", methods=["GET"])
def bloody_results():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "SELECT HospitalName, TestDate, COUNT(*) as Total FROM laboratoryresults WHERE PatientTC = %s GROUP BY TestDate; "
    result = cursor.execute(query,(TCNumber,))
    if result > 0:
        bloody_result = cursor.fetchall()
        return render_template("bloody_results.html", bloody_result=bloody_result)

@login_required_user
@app.route("/hospital_visits", methods=["GET"])
def hospital_visits():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    query = "Select * from hospitalvisits where PatientTC = %s"
    cursor.execute(query,(TCNumber,))
    patientData = cursor.fetchall()
    all_visits = []
    for visit in patientData:
        query2 = "Select * from doctors where TCNumber = %s"
        cursor2.execute(query2,(visit["DoctorTC"],))
        doctorData = cursor2.fetchone()
        visit_info = {"visit": visit, "doctor": doctorData}
        all_visits.append(visit_info)
    
    return render_template("patient_hospital_visit.html", visits=all_visits)



    
@login_required_user
@app.route("/bloody_results_detail/<date>", methods=["GET"])
def bloody_results_detail(date):
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "SELECT * from laboratoryresults where TestDate = %s and PatientTC = %s"
    result = cursor.execute(query, (date, TCNumber))
    if result > 0:
        info = cursor.fetchall()
        print(info)
        return render_template("bloody_results_detail.html", info=info)

@login_required_user
@app.route("/ai_analysis/<TCNumber>/<date>", methods=["GET"])
def ai_analysis(TCNumber, date):
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "SELECT TestName, Result, ResultUnit, ReferenceValue from laboratoryresults where TestDate = %s and PatientTC = %s"
    result = cursor.execute(query, (date, TCNumber))
    if result > 0:
        info = cursor.fetchall()
        info = list_to_string(format_output(info))
        info = gpt_response(info)
        print(info)
        return render_template("ai_analysis.html", info=info)


@login_required_user
@app.route("/radiology_images", methods=["GET"])
def radiology_images():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "Select * from radiologyimages where PatientTC = %s"
    result = cursor.execute(query,(TCNumber,))
    if result > 0:
        radiology_images_info = cursor.fetchall()
    return render_template("radiology_images.html", radiology_images_info=radiology_images_info)


brain_segment_model_weights = "./static/assets/models/brain2.pth"


@login_required_user
@app.route("/view_radiology_images/<id>", methods=["GET"])
def view_radiology_images(id):
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    query = "Select * from radiologyimages where id = %s"
    query2 = "Select FirstName, LastName from patients where TCNumber = %s"
    result = cursor.execute(query,(id,))
    result2 = cursor2.execute(query2,(TCNumber,))
    if result or result2 > 0:
        radiology_images_info = cursor.fetchall()
        patient_name_surname = cursor2.fetchone()
        image_date = radiology_images_info[0]["ImageDate"]
        image_type = radiology_images_info[0]["ImageType"]
        ID = radiology_images_info[0]["ID"]
        image_path = "./static/assets" + str(radiology_images_info[0]["ImageLocation"])
        predict_unet(weights_path=brain_segment_model_weights, original_nii_path=image_path, TCNumber=TCNumber, ID=ID)
    return render_template("view_radiology_images.html", radiology_images_info = radiology_images_info[0] , patient_name_surname = patient_name_surname)


## DOKTOR ##

@app.context_processor
def inject_user():
    if "logged_in_doctor" in session:
        data = {
            "ID": session.get("ID"),
            "TCNumber": session.get("TCNumber"),
            "FirstName": session.get("FirstName"),
            "LastName": session.get("LastName"),
            "Email": session.get("Email"),
            "Specialty": session.get("Specialty")
        }
    else:
        data = None
    return dict(data=data)


@login_required_doctor
@app.route("/layout_doctor", methods=["GET"])
def layout_doctor():
    if request.method == "GET":
        data = {
            "ID": session.get("ID"),
            "TCNumber": session.get("TCNumber"),
            "FirstName": session.get("FirstName"),
            "LastName": session.get("LastName"),
            "Email": session.get("Email"),
            "Password": session.get("Password"),
            "Specialty": session.get("Specialty"),
        }
        return render_template("layout_doctor.html", data=data)
    else:
        return render_template("layout_doctor.html", data=data)


@app.route("/login_doctor", methods=["GET", "POST"])
def login_doctor():
    session.clear()
    if request.method == "POST":
        TCNumber = request.form.get('TCNumber')
        Password = request.form.get('password')
        cursor = mysql.connection.cursor()
        query = "Select * from doctors where TCNumber = %s"
        result = cursor.execute(query,(TCNumber,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data["Password"]
            if(sha256_crypt.verify(Password,real_password)):
                session["logged_in_doctor"] = True
                session["ID"] = data["ID"]
                session["TCNumber"] = data["TCNumber"]
                session["FirstName"] = data["FirstName"]
                session["LastName"] = data["LastName"]
                session["Email"] = data["Email"]
                session["Specialty"] = data["Specialty"]
                return redirect(url_for("doctor_dashboard"))
            else:
                return redirect(url_for("login_doctor"))
        else:
            return redirect(url_for("login_doctor"))
    else:
        return render_template("login_doctor.html")

@login_required_doctor
@app.route("/doctor_dashboard")
def doctor_dashboard():
    cursor1 = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    cursor3 = mysql.connection.cursor()
    cursor4 = mysql.connection.cursor()
    cursor5 = mysql.connection.cursor()
    TCNumber = session.get("TCNumber")
    query1 = "SELECT DISTINCT COUNT(*) as PatientCount FROM appointments where DoctorTC = %s"
    query2 = "SELECT DISTINCT COUNT(*) as DoctorCount FROM doctors"
    query3 = "SELECT DISTINCT p.TCNumber, p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup, lr.TestDate FROM patients AS p JOIN hospitalvisits AS hv ON p.TCNumber = hv.PatientTC JOIN laboratoryresults AS lr ON p.TCNumber = lr.PatientTC JOIN doctors AS d ON hv.DoctorTC = d.TCNumber WHERE d.TCNumber = %s AND lr.Result IS NOT NULL LIMIT 3;"
    query4 = "SELECT DISTINCT p.TCNumber, p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup, ri.HospitalName FROM patients AS p JOIN hospitalvisits AS hv ON p.TCNumber = hv.PatientTC JOIN radiologyimages AS ri ON p.TCNumber = ri.PatientTC JOIN doctors AS d ON hv.DoctorTC = d.TCNumber WHERE d.TCNumber = %s AND ri.ImageLocation IS NOT NULL;"
    query5 = "Select DISTINCT p.TCNumber, p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup, a.AppointmentDate from doctors d, patients p, appointments a where p.TCNumber in (Select a.PatientTC from appointments where a.DoctorTC = %s) LIMIT 3;"
    result1 = cursor1.execute(query1,(TCNumber,))
    result2 = cursor2.execute(query2)
    result3 = cursor3.execute(query3,(TCNumber,))
    result4 = cursor4.execute(query4,(TCNumber,))
    result5 = cursor5.execute(query5,(TCNumber,))
    if result1 or result2 or result3 or result4 > 0:
        patientCount = cursor1.fetchall()
        doctorCount = cursor2.fetchall()
        bloodyresultInfo = cursor3.fetchall()
        radiologyInfo = cursor4.fetchall()
        appointmentsInfo = cursor5.fetchall()
        print(radiologyInfo)
    return render_template("doctor_dashboard.html", patientCount=patientCount[0]["PatientCount"], doctorCount=doctorCount[0]["DoctorCount"], bloodyresultInfo=bloodyresultInfo,radiologyInfo=radiologyInfo,appointments=appointmentsInfo)

@app.route("/logout_doctor")
def logout_doctor():
    session.clear()
    return redirect(url_for("index"))

@login_required_doctor
@app.route("/patient_appointments")
def patient_appointments():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "Select DISTINCT p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup, a.AppointmentDate from doctors d, patients p, appointments a where p.TCNumber in (Select a.PatientTC from appointments where a.DoctorTC = %s);"
    result = cursor.execute(query,(TCNumber,))
    if result > 0:
        appointments = cursor.fetchall()
    return render_template("patient_appointments.html", appointments=appointments)

@login_required_doctor
@app.route("/patient_laboratory_results")
def patient_laboratory_results():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT p.TCNumber, p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup, lr.TestDate FROM patients AS p JOIN hospitalvisits AS hv ON p.TCNumber = hv.PatientTC JOIN laboratoryresults AS lr ON p.TCNumber = lr.PatientTC JOIN doctors AS d ON hv.DoctorTC = d.TCNumber WHERE d.TCNumber = %s AND lr.Result IS NOT NULL;"
    result = cursor.execute(query,(TCNumber,))
    if result > 0:
        results = cursor.fetchall()
    return render_template("patient_laboratory_results.html", results=results)

@login_required_doctor
@app.route("/patient_radiology_images")
def patient_radiology_images():
    TCNumber = session.get("TCNumber")
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT p.TCNumber, p.FirstName, p.LastName, p.Email, p.DateOfBirth, p.Gender, p.BloodGroup FROM patients AS p JOIN hospitalvisits AS hv ON p.TCNumber = hv.PatientTC JOIN radiologyimages AS ri ON p.TCNumber = ri.PatientTC JOIN doctors AS d ON hv.DoctorTC = d.TCNumber WHERE d.TCNumber = %s AND ri.ImageLocation IS NOT NULL;"
    result = cursor.execute(query,(TCNumber,))
    if result > 0:
        results = cursor.fetchall()
    return render_template("patient_radiology_images.html", results=results)


@login_required_user
@app.route("/patient_bloody_results_list/<PatientTC>", methods=["GET"])
def patient_bloody_results_list(PatientTC):
    cursor = mysql.connection.cursor()
    query = "SELECT PatientTC, HospitalName, TestDate, COUNT(*) as Total FROM laboratoryresults WHERE PatientTC = %s GROUP BY TestDate; "
    result = cursor.execute(query,(PatientTC,))
    if result > 0:
        bloody_result = cursor.fetchall()
        return render_template("patient_bloody_results_list.html", bloody_result=bloody_result)


@login_required_user
@app.route("/patient_radiology_images_list/<PatientTC>", methods=["GET"])
def patient_radiology_images_list(PatientTC):
    cursor = mysql.connection.cursor()
    query = "SELECT ri.ID, ri.PatientTC, ri.ImageType, ri.ImageLocation, ri.ImageDate FROM radiologyimages AS ri JOIN patients AS p ON ri.PatientTC = p.TCNumber WHERE p.TCNumber = %s AND ri.ImageLocation IS NOT NULL;"
    result = cursor.execute(query,(PatientTC,))
    if result > 0:
        radiology_images = cursor.fetchall()
        return render_template("patient_radiology_images_list.html", radiology_images=radiology_images)

@login_required_user
@app.route("/patient_bloody_results_detail/<TCNumber>/<date>", methods=["GET"])
def patient_bloody_results_detail(TCNumber, date):
    cursor = mysql.connection.cursor()
    query = "SELECT * from laboratoryresults where TestDate = %s and PatientTC = %s"
    result = cursor.execute(query, (date, TCNumber))
    if result > 0:
        bloody_result = cursor.fetchall()
        return render_template("patient_bloody_results_detail.html", bloody_result=bloody_result)


def update_class_composition(composition_predicted_class):
    class_mapping = {'0': "A", '1': "B", '2': "C", '3': "D"}
    composition_predicted_class_str = str(composition_predicted_class)
    return class_mapping.get(composition_predicted_class_str, "Geçersiz değer")

def update_class_birads(birads_predicted_class):
    class_mapping = {'0': "BIRADS 1", '1': "BIRADS 2-3", '2': "BIRADS 4-5"}
    birads_predicted_class_str = str(birads_predicted_class)
    return class_mapping.get(birads_predicted_class_str, "Geçersiz değer")

@login_required_user
@app.route("/patient_radiology_images_detail/<TCNumber>/<id>", methods=["GET"])
def patient_radiology_images_detail(TCNumber, id):
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    query = "Select * from radiologyimages where id = %s"
    query2 = "Select FirstName, LastName from patients where TCNumber = %s"
    result = cursor.execute(query,(id,))
    result2 = cursor2.execute(query2,(TCNumber,))
    if result or result2 > 0:
        radiology_images_info = cursor.fetchall()
        patient_name_surname = cursor2.fetchone()
        # image_date = radiology_images_info[0]["ImageDate"]
        image_type = radiology_images_info[0]["ImageType"]
        ID = radiology_images_info[0]["ID"]
        if image_type == "Brain MRI":
            image_path = "./static/assets" + str(radiology_images_info[0]["ImageLocation"])
            predict_unet(weights_path=brain_segment_model_weights, original_nii_path=image_path, TCNumber=TCNumber, ID=ID)
            return render_template("patient_radiology_images_detail.html", image_type = image_type, radiology_images_info = radiology_images_info[0], patient_name_surname = patient_name_surname)
        elif image_type == "Mamografi":
            image_paths = str(radiology_images_info[0]["ImageLocation"]) 
            image_paths_list = image_paths.split(',')
            rcc = "./static/assets"  + image_paths_list[0]
            lcc = "./static/assets"  + image_paths_list[1]
            rmlo = "./static/assets" + image_paths_list[2]
            lmlo = "./static/assets" + image_paths_list[3]
            composition_predicted_class, composition_max_probability = predict_composition(rcc, lcc, rmlo, lmlo)
            composition_predicted_class = update_class_composition(composition_predicted_class)
            birads_right_predicted_class, birads_right_max_probability = predict_birads_right(rcc, rmlo) #cc, mlo
            birads_right_predicted_class = update_class_birads(birads_right_predicted_class)
            birads_left_predicted_class, birads_left_max_probability = predict_birads_left(lcc, lmlo) #cc, mlo
            birads_left_predicted_class = update_class_birads(birads_left_predicted_class)
        return render_template("patient_radiology_images_detail.html", image_type = image_type, \
                            radiology_images_info = radiology_images_info[0], patient_name_surname = patient_name_surname, \
                            composition_predicted_class = str(composition_predicted_class), composition_max_probability = str(composition_max_probability),\
                            birads_right_predicted_class = str(birads_right_predicted_class), birads_right_max_probability = str(birads_right_max_probability), \
                            birads_left_predicted_class = str(birads_left_predicted_class), birads_left_max_probability = str(birads_left_max_probability), \
                            rcc = rcc[9:], lcc = lcc[9:], rmlo = rmlo[9:], lmlo = lmlo[9:])


if __name__ == "__main__":
    app.run(debug=True, port=5000)