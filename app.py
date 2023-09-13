import secrets

from flask import Flask,render_template,url_for,redirect,request,flash
from alchemy_db import engine
from sqlalchemy.orm import sessionmaker
from models import *
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from Forms import Register,Login, Contact_Form,Update_account_form,Reset,Reset_Request
from Tokeniser import Tokenise
from flask_mail import Mail,Message
from Advert_Forms import Job_Ads_Form,Company_Register_Form , Company_Login,Company_UpdateAcc_Form
import os
from PIL import Image
from sqlalchemy import text



# from models.user import get_reset_token, very_reset_token
#DB sessions
db_sessions = sessionmaker(bind=engine)
db = db_sessions()

#Application
app = Flask(__name__)
app.config['SECRET KEY'] = 'Tma*@1111'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'




#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
#Encrypt Password
encry_pw = Bcrypt(app)

class user_class:
    cls_name = None

@login_manager.user_loader
def load_user(user_id):
    return db.query(user).get(user_id)

    # if current_user:
    #     print("-------------------------User: ", user_class.cls_name)
    #     return db.query(user_class.cls_name).get(current_user.id)
    #
    # else:
    #     return db.query(user_class.cls_name).get(current_user.id)
    #     print("-------------------------No Class User: ",user_class.cls_name)

app.config['SECRET_KEY'] = 'f9ec9f35fbf2a9d8b95f9bffd18ba9a1'



def resize_img(img,size_x=30,size_y=30):

    i = Image.open(img)

    if i.size > (200,200):

        output_size = (size_x,size_y)
        i.thumbnail(output_size)

        i.save(img)
    else:
        print("Check IMG Size: ",i.size)

    return img



def save_pic(picture,size_x=25,size_y=25):

    _img_name, _ext = os.path.splitext(picture.filename)
    gen_random = secrets.token_hex(8)
    new_img_name = gen_random + _ext

    saved_img_path = os.path.join(app.root_path,'static/images', new_img_name)

    output_size = (size_x, size_y)
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(saved_img_path)

    return new_img_name


#Web
@app.route("/")
def home():

    img_1 = resize_img("/static/images/default.jpg",180,180)
    img_2 = resize_img("/static/images/unnamed.png", 180, 180)
    img_3 = resize_img("/static/images/image.jpg", 180, 180)

    companies_ls = db.query(company_user).all()

    for cpm in companies_ls:
        print("DEBUG COMPANIES: ",cpm.name)

    return render_template("index.html",img_1=img_1, img_2  =  img_2,img_3 = img_3, companies_ls=companies_ls )


@app.route("/sign_up", methods=["POST","GET"])
def sign_up():

    register = Register()

    user.metadata.create_all(bind=engine)

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    image_fl = url_for('static', filename='images/image.jpg')

    if register.validate_on_submit():

        print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context


            # If the webpage has made a post e.g. form post
            with engine.connect():
                print('Create All..........................................')
                hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
                # Base.metadata.create_all()
                # ....user has inherited the Base class
                # user.metadata.create_all(bind=engine)
                user1 = job_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                             confirm_password=hashd_pwd,image="default.jpg")

                # db.rollback()
                db.add(user1)
                db.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                # print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        print(register.errors)



    # from myproject.models import user
    return render_template("sign_up_form.html",register=register)




#----------------UPDATE ACCOUNT --------------#

@app.route("/account",methods=['POST','GET'])
@login_required
def account():
    from sqlalchemy import update

    cv = Update_account_form()
    print("Current User: ",current_user.name)

    image_fl = url_for('static', filename='images/' + current_user.image)


    if request.method == 'POST':
        print("method is POST")
        print(cv.errors)

        if cv.validate_on_submit():
            id = current_user.id
            usr = db.query(job_user).get(id)
            if cv.image_pfl.data:
                print("Debug Image on If: ", cv.image_pfl.data)
                pfl_pic = save_pic(picture = cv.image_pfl.data)
                usr.image = pfl_pic

            usr.name = cv.name.data
            usr.email = cv.email.data
            usr.contacts = cv.contacts.data
            print("Current User School: ", current_user.school)
            usr.school = cv.school.data
            usr.tertiary = cv.tertiary.data
            usr.address = cv.address.data
            usr.hobbies = cv.hobbies.data
            usr.reference_1 = cv.reference_1.data
            usr.reference_2 = cv.reference_2.data
            usr.skills = cv.skills.data
            usr.experience = cv.experience.data

            db.commit()

            redirect(url_for('account'))

        elif cv.errors:
            # for error in cv.errors:
            print('Update Errors: ',cv.errors)
    elif cv.errors:
        # for error in cv.errors:
        flash("Update Unsuccessfull!!, check if all fields are filled", "error")
        print('Update Errors: ', cv.errors)


    return render_template("account.html",cv=cv, title="Account", image_fl = image_fl)


@app.route("/login",methods=["POST","GET"])
def login():
    login= Login()


    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':



        if login.validate_on_submit():
            # print(f"Account Successfully Created for {login.name.data}")
            user_login = db.query(user).filter_by(email = login.email.data).first()
            # flash(f"Hey! {user_login.password} Welcome", "success")
            if user_login and encry_pw.check_password_hash(user_login.password,login.password.data):
                login_user(user_login)
                #After login required prompt, take me to the page I requested earlier
                req_page = request.args.get('next')
                flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                return redirect(req_page) if req_page else redirect(url_for('home'))
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                print(login.errors)

    return render_template('login_form.html', title='Login',login=login)

@app.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('home'))

@app.route("/user")
def user_profile():
    from sqlalchemy import text

    users = []
    all = text('''SELECT * FROM company_user;''')
    # db has binded the engine's database file
    for ea_user in db.execute(all):
        users.append(list(ea_user))
        #print(users)

    return f"{users}"

@app.route("/contact", methods=["POST", "GET"])
def contact_us():

    contact_form = Contact_Form()
    if request.method == "POST":
        if contact_form.validate_on_submit():
            if request.method == "POST":
                flash("Message Successfully Sent!!", "success")
                print("Posted")
        else:
            flash("Ooops!! Please be sure fill both email & message fields, correctly","error")

    return render_template("contact_page.html",contact_form=contact_form)




@app.route("/reset", methods=['POST', "GET"])
def reset():
    from sqlalchemy import update
    reset_form = Reset()

    print("Current User: ",current_user.__dict__)

    if request.method == 'POST':
        if reset_form.validate_on_submit():
            #Current User Changing Password
            if encry_pw.check_password_hash(current_user.password,reset_form.old_password.data):
                token = Tokenise().get_reset_token(current_user.id)
                print("Reset Token: ", token)
                v_user_id = Tokenise().verify_reset_token(token)
                print("User_id: ", v_user_id)

                pass_reset_hash = encry_pw.generate_password_hash(reset_form.new_password.data)

                usr = db.query(user).get(v_user_id)
                usr.password = pass_reset_hash
                db.commit()

                # logout_user()

                flash(f"Password Changed Succesfully!", "success")
                return redirect(url_for("account"))
            else:
                flash(f"Ooops! Passwords don't match, You might have forgotten your Old Password", "error")
            # for field,v in current_user.__dict__.items():
            #     if not field=="_sa_instance_state" and not field=="id":
            #         _attr = user1.__dict__[field]
            #         update(user).where(user1.id == current_user.id).values(field=user1.__dict__[field])




    return render_template("pass_reset.html",reset_form=reset_form)


@app.route("/reset_request", methods=['POST', "GET"])
def reset_request():

    reset_request_form = Reset_Request()

    print("Current User: ",current_user.__dict__)

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            usr_email = db.query(user).filter_by(email=reset_request_form.email.data).first()
            print("DEBUG EMAIL: ",usr_email.email)
            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 465
                app.config["MAIL_USE_SSL"] = True
                em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
                app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")

                token = Tokenise().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=["pro.dignitron@gmail.com"])
                msg.body = f"""To reset your password, visit the following link:
                {url_for('reset', token=token, _external=True)}"""
                flash('An email has been sent with instructions to reset your password', 'success')

                mail = Mail(app)
                mail.send(msg)

            #Current User Changing Password
            send_link(usr_email)

            return redirect(url_for('login'))


    return render_template("reset_request.html",reset_request_form=reset_request_form)

@app.route("/job_ads_form", methods=["POST","GET"])
@login_required
def job_ads_form():

    job_ad_form = Job_Ads_Form()
    job_ads_model = Jobs_Ads

    job_ads_model.metadata.create_all(bind=engine)


    if request.method == 'POST':
       if job_ad_form.validate_on_submit():
            job_post1 = job_ads_model(
                job_title=job_ad_form.job_title.data,
                description = job_ad_form.description.data,
                responsibilities = job_ad_form.responsibilities.data,
                qualifications = job_ad_form.qualifications.data,
                contact_person = job_ad_form.posted_by.data,
                job_type= request.form.get('job_type_sel'),
                # date_posted = datetime.utcnow(),
                application_deadline=job_ad_form.application_deadline.data,
                job_posted_by = current_user.id
                          )


            # if bools are True
            if job_ad_form.pay_type_bl.data:
                print('Job Type: ', job_ad_form.pay_type_bl.data)
                job_post1.pay_type = job_ad_form.other_pay_type.data

            if job_ad_form.other_job_type.data:
                job_post1.job_type = job_ad_form.other_job_type.data

            if job_ad_form.work_duration_bl.data:
                job_post1.work_duration = job_ad_form.work_duration.data

            if job_ad_form.work_days_bl.data:
                job_post1.work_days = job_ad_form.work_days.data

            if job_ad_form.work_hours_bl.data:
                job_post1.work_hours = job_ad_form.work_hours.data

            if job_ad_form.age_range_bl.data:
                job_post1.age_range = job_ad_form.age_range.data

            if job_ad_form.benefits_bl.data:
                job_post1.benefits = job_ad_form.benefits.data



            db.add(job_post1)
            db.commit()

    return render_template("job_ads_form.html",job_ad_form = job_ad_form)

@app.route("/company_retieve")
def cmp_user_profile():
    from sqlalchemy import text

    users = []
    all = text('''SELECT * FROM job_applications;''')
    # db has binded the engine's database file
    for ea_user in db.execute(all):
        users.append(list(ea_user))
        #print(users)


    return f"{users}"

@app.route("/job_ads",methods=["GET", "POST"])
def job_adverts():


    if current_user.is_authenticated:
        print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")

    no_image_fl = 'static/images/default.jpg'

    Jobs_Ads.metadata.create_all(bind=engine)
    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()

    if request.method == 'GET':
        id = request.args.get('id')
        print("Check Get Id: ",id)
        if id:
            #Filter Ads with a specific company's id
            job_ads = db.query(Jobs_Ads).filter_by(job_posted_by=id)
        else:
            job_ads = db.query(Jobs_Ads).all()

    job_ads_form = Job_Ads_Form()




    # Fix jobs adds does not have hidden tag
    return render_template("job_ads_gui.html",job_ads=job_ads,job_ads_form=job_ads_form,db=db,
                           company_user=company_user,user=usr,no_image_fl =no_image_fl)





                    #------------------------------COMPANIES DATA-------------------------------#

@app.route("/company_sign_up", methods=["POST","GET"])
def company_sign_up_form():

    company_register = Company_Register_Form()

    company_user.metadata.create_all(bind=engine)

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if company_register.validate_on_submit():


        if request.method == 'POST':
            # context


            # If the webpage has made a post e.g. form post
            with engine.connect():
                print('Create All..........................................')
                company_hashd_pwd = encry_pw.generate_password_hash(company_register.company_password.data).decode('utf-8')
                # Base.metadata.create_all()
                # ....user has inherited the Base class
                # user.metadata.create_all(bind=engine)
                user1 = company_user(name=company_register.company_name.data, email=company_register.company_email.data, password=company_hashd_pwd,
                                     confirm_password=company_hashd_pwd ,company_contacts=company_register.company_contacts.data,image="default.jpg",
                                     company_address=company_register.company_address.data, web_link=company_register.website_link.data,fb_link=company_register.facebook_link.data,
                                     twitter_link=company_register.twitter_link.data,youtube=company_register.youtube_link.data)

                # db.rollback()
                db.add(user1)
                db.commit()
                flash(f"Account Successfully Created for {company_register.company_name.data}", "success")

                return redirect(url_for('company_login'))

                # print(company_register.name.data,company_register.email.data)
    elif company_register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        print(company_register.errors)


    # from myproject.models import user
    return render_template("company_signup_form.html",company_register=company_register)


@app.route("/company_login",methods=["POST","GET"])
def company_login():
    company_login= Company_Login()

    # image_fl = url_for('static', filename='images/' + current_user.image)

    user_class.cls_name = company_user
    # if current_company_user.is_authenticated:
    #     return redirect(url_for('home'))
    if request.method == 'POST':

        if company_login.validate_on_submit():
            # print(f"Account Successfully Created for {company_login.name.data}")
            company_user_login = db.query(company_user).filter_by(email = company_login.company_email.data).first()
            # flash(f"Hey! {user_login.password} Welcome", "success")
            if company_user_login and encry_pw.check_password_hash(company_user_login.password,company_login.company_password.data):
                login_user(company_user_login)
                #After company_login required prompt, take me to the page I requested earlier
                req_page = request.args.get('next')
                flash(f"{company_user_login.name.title()} You're Logged In!", "success")
                return redirect(req_page) if req_page else redirect(url_for('home'))
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                print(company_login.errors)

    return render_template('company_login_form.html', title='Company Login',company_login=company_login)



#---------------COMPANY ACCOUNT---------------------#
@app.route("/company_account",methods=["GET", "POST"])
@login_required
def company_account():

    company_update = Company_UpdateAcc_Form()

    image_fl = url_for('static', filename='images/' + current_user.image)

    if request.method == "POST":

        # if company_update.validate_on


        id = current_user.id
        cmp_usr = db.query(company_user).get(id)

        print('DEBUG UPDATE 1: ', cmp_usr.web_link)

        if company_update.company_logo.data:
            print("Debug Image on If: ", company_update.company_logo.data)
            pfl_pic = save_pic(picture=company_update.company_logo.data)
            cmp_usr.image = pfl_pic

        cmp_usr.name = company_update.company_name.data
        cmp_usr.email = company_update.company_email.data
        cmp_usr.contacts = company_update.company_contacts.data
        cmp_usr.web_link = company_update.website_link.data
        cmp_usr.fb_link = company_update.facebook_link.data
        cmp_usr.company_address = company_update.company_address.data
        cmp_usr.twitter_link = company_update.twitter_link.data
        cmp_usr.youtube = company_update.youtube_link.data


        db.commit()

        print('DEBUG UPDATE: ',cmp_usr.web_link)

    return render_template("company_account.html",company_update = company_update,image_fl=image_fl)

#-------------------PARTNERING COMPANIES----------------------#
@app.route("/partnering_companies",methods=["GET", "POST"])
def partnering_companies():

    job_ads = db.query(Jobs_Ads).all()


    # Fix jobs adds does not have hidden tag
    return render_template("partnering_companies.html",job_ads=job_ads,job_ads_form=job_ads_form,db=db,
                           company_user=company_user,user=usr,no_image_fl =no_image_fl)


@app.route("/send_application", methods=["GET","POST"])
@login_required
def send_application():

    send_application = Applications()

    Applications.metadata.create_all(bind=engine)

    if not current_user.image and not current_user.school:
        redirect(url_for('account'))
        flash("Warning!! Your Account needs to be updated Soon, You won't be able to send Application if not so", "error")

    else:
        if current_user.is_authenticated:

            if request.method == "GET":
                jb_id = request.args['job_id']
                apply = Applications(

                    applicant_id = current_user.id,
                    job_details_id= jb_id, #db.query(Jobs_Ads).get(jb_id),
                    employer_id = db.query(Jobs_Ads).get(jb_id).job_posted_by

                )

                #Check if application not sent before
                job_obj = db.query(Applications).filter_by(job_details_id=jb_id).first()
                company_obj = db.query(company_user).get(apply.employer_id)
                print('----------------------job_obj: ',job_obj)
                if not job_obj:
                    db.add(apply)
                    db.commit()
                    return render_template("send_application.html", send_application=send_application, job_obj=job_obj,
                                           company_obj=company_obj)
                else:
                    # fl = flash(f"Application with this details Already Submitted!!", "error")
                    return f'''This Application Already Submitted before.
                     Please Wait for a Reply!!'''



    return f'Something went Wrong, Please return to the previuos page'


@app.route("/company_jb_ads",methods=["GET", "POST"])
@login_required
def local_jb_ads():

    if request.method == 'GET':
        id = request.args['id']
        job_ad = db.query(Jobs_Ads).get(id)

        print("Job Ad Title: ",job_ad.job_title)


@app.route("/job_ad_opened",methods=["GET", "POST"])
def view_job():

    if request.method == 'GET':
        id = request.args['id']
        job_ad = db.query(Jobs_Ads).get(id)

        print("Job Ad Title: ",job_ad.job_title)


    return render_template('job_ad_opened.html',item=job_ad,db=db,company_user=company_user)

@app.route("/job_applications",methods=["GET", "POST"])
def applications():

    #Get all applications from Applications database
    all_applications = db.query(Applications).all()

    print("Debug Application List: ", db.query(job_user).get(all_applications[0].applicant_id).name )



    applications = Applications()

    job_usr = job_user
    job_ads = Jobs_Ads

    return render_template("applications.html", all_applications = all_applications, job_user = job_usr, job_ads = job_ads, applications = applications,db=db)

@app.route("/view_applicant")
def view_applicant():

    if request.method == 'GET':
        id = request.args['id']
        job_usr = db.query(job_user).get(id)

    return render_template("view_applicant.html", job_usr = job_usr)

@app.route("/hire_applicant")
def hire_applicant():

    if request.method == 'GET':
        id = request.args['id']
        job_usr = db.query(job_user).get(id)

    return render_template("hire_applicant.html", job_usr = job_usr,db=db)


if __name__ == "__main__":

    app.run(debug=True)
