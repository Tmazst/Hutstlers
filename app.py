import secrets

from flask import Flask,render_template,url_for,redirect,request,flash,session, make_response
# from alchemy_db import engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from Forms import Register,Login, Contact_Form,Update_account_form,Reset,Reset_Request
from Tokeniser import Tokenise
from flask_mail import Mail,Message
from Advert_Forms import Job_Ads_Form,Company_Register_Form, Company_Login, Company_UpdateAcc_Form, Freelance_Ads_Form
import os
from PIL import Image
from sqlalchemy import exc
import rsa
#......for local DB
import MySQLdb
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from models import db, user,company_user,job_user,Jobs_Ads,Applications,Freelance_Jobs_Ads,Email_Verifications,FreeL_Applications
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from wtforms.validators import ValidationError
from datetime import datetime


# from models.user import get_reset_token, very_reset_token
#DB sessions
# db_sessions = sessionmaker(bind=engine)
# db = db_sessions()

#Applications
app = Flask(__name__)


# app.config['SECRET KEY'] = 'Tmazst41'
app.config['SECRET_KEY'] = 'f9ec9f35fbf2a9d8b95f9bffd18ba9a1'
# APP_DATABASE_URI = "mysql+mysqlconnector://Tmaz:Tmazst*@1111Aynwher_isto3/Tmaz.mysql.pythonanywhere-services.com:3306/users_db"
# Local
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:tmazst41@localhost/tht_database"
# Online
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://Tmaz:Tmazst41@Tmaz.mysql.pythonanywhere-services.com:3306/Tmaz$users_db"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

pub, priv = rsa.newkeys(512)

#Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Encrypt Password
encry_pw = Bcrypt(app)

# migrate = Migrate(app,db)

class user_class:

    s = None
    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])

        return s.dumps({'user_id': c_user_id}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'])

        try:
             # f'We are trying Token {token} not accessed here is the outcome user'
            user_id = s.loads(token)['user_id']
        except:
            return f'Token {user_id} not accessed here is the outcome user'

        return user_id

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)

    # if current_user:
    #     #print("-------------------------User: ", user_class.cls_name)
    #     return db.query(user_class.cls_name).get(current_user.id)
    #
    # else:
    #     return db.query(user_class.cls_name).get(current_user.id)
    #     #print("-------------------------No Class User: ",user_class.cls_name)


def resize_img(img,size_x=30,size_y=30):

    i = Image.open(img)

    if i.size > (200,200):

        output_size = (size_x,size_y)
        i.thumbnail(output_size)

        i.save(img)
    else:
        pass
        #print("Check IMG Size: ",i.size)

    return img


def save_pic(picture,size_x=300,size_y=300):

    _img_name, _ext = os.path.splitext(picture.filename)
    gen_random = secrets.token_hex(8)
    new_img_name = gen_random + _ext

    saved_img_path = os.path.join(app.root_path,'static/images', new_img_name)

    output_size = (size_x, size_y)
    i = Image.open(picture)
    h,w = i.size
    if h > 400 and w > 400:
        # downsize the image with an ANTIALIAS filter (gives the highest quality)
        img = i.resize(i.size, Image.Resampling.LANCZOS)
        img.thumbnail(output_size)
    else:
        img = i.resize(i.size, Image.LANCZOS)
        # img.thumbnail(i.size)

    img.save(saved_img_path,optimize=True, quality=95)




    return new_img_name


#Web
@app.route("/")
def home():

    # img_1 = resize_img("/static/images/default.jpg",180,180)
    # img_2 = resize_img("/static/images/unnamed.png", 180, 180)
    # img_3 = resize_img("/static/images/image.jpg", 180, 180)

    try:
        companies_ls = company_user.query.all()
        comp_len = len(companies_ls)
    except:
        db.create_all()
        #print("Creating Tables")
        # companies_ls = db.session.query(company_user).all()
        #print("DEBUG COMPANIES: ",cpm.name)

    for cmp in companies_ls:
        print("Check Links: ",cmp.fb_link)


    return render_template("index.html",img_1='', img_2  ='',img_3 ='', companies_ls=companies_ls, comp_len=comp_len )


@app.route("/sign_up", methods=["POST","GET"])
def sign_up():

    register = Register()

    db.create_all() 

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    image_fl = url_for('static', filename='images/image.jpg')

    if register.validate_on_submit():

        #print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            # If the webpage has made a post e.g. form post
            #print('Create All..........................................')
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            # Base.metadata.create_all()
            # ....user has inherited the Base class
            # db.create_all()
            user1 = job_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd,image="default.jpg")

            # db.rollback()
            try:
                db.session.add(user1)
                db.session.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"Something went wrong,please check for errors", "error")
                Register().validate_email(register.email.data)
                # return redirect(url_for('sign_up'))


            # #print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(register.errors)



    # from myproject.models import user
    return render_template("sign_up_form.html",register=register)

@app.route("/about")
def about():

    return render_template("about.html")


#----------------UPDATE ACCOUNT --------------#
@app.route("/account", methods=['POST','GET'])
@login_required
def account():
    from sqlalchemy import update

    cv = Update_account_form()
    #print("Current User: ",current_user.name)

    image_fl = url_for('static', filename='images/' + current_user.image)

    if request.method == 'POST':
        #print("method is POST")
        #print(cv.errors)

        if cv.validate_on_submit():
            id = current_user.id
            usr = job_user.query.get(id)
            if cv.image_pfl.data:
                #print("Debug Image on If: ", cv.image_pfl.data)
                pfl_pic = save_pic(picture = cv.image_pfl.data)
                usr.image = pfl_pic

            usr.name = cv.name.data
            usr.email = cv.email.data
            usr.contacts = cv.contacts.data
            #print("Current User School: ", current_user.school)
            usr.school = cv.school.data
            usr.tertiary = cv.tertiary.data
            usr.address = cv.address.data
            usr.hobbies = cv.hobbies.data
            usr.reference_1 = cv.reference_1.data
            usr.reference_2 = cv.reference_2.data
            usr.skills = cv.skills.data
            usr.experience = cv.experience.data

            db.session.commit()

            flash("Account Updated Successfull!!", "success")

            # redirect(url_for('verification'))

        elif cv.errors:
            pass
            # for error in cv.errors:
            #print('Update Errors: ',cv.errors)
    elif cv.errors:
        # for error in cv.errors:
        flash("Update Unsuccessfull!!, check if all fields are filled", "error")
        #print('Update Errors: ', cv.errors)


    return render_template("account.html",cv=cv, title="Account", image_fl = image_fl)


@app.route("/login",methods=["POST","GET"])
def login():

    login= Login()

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':


        if login.validate_on_submit():
            # #print(f"Account Successfully Created for {login.name.data}")
            user_login = user.query.filter_by(email=login.email.data).first()
            # flash(f"Hey! {user_login.password} Welcome", "success")
            #Stay sign in
            session['user_id'] = user_login.id
            if request.form.get('stay_signed_in'):
                token = secrets.token_urlsafe(16)  # Generate a 16-character token
                user_login.token = token
                db.session.commit()
                # Set a persistent cookie with the token
                resp = make_response("Login successful")
                resp.set_cookie('stay_signed_in', token, httponly=True, max_age=60 * 60 * 24 * 30)  # 30 days
                return resp

            else:
                if user_login and encry_pw.check_password_hash(user_login.password,login.password.data):
                    login_user(user_login)
                    #Query DB if User is verified; #Models' user class
                    if not user_login.verified:
                        return redirect(url_for('verification'))
                    else:
                        #After login required prompt, take me to the page I requested earlier
                        #print("No Verification Needed: ",user_login.verified)
                        req_page = request.args.get('next')
                        flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                        return redirect(req_page) if req_page else redirect(url_for('home'))
                else:
                    flash(f"Login Unsuccessful, please use correct email or password", "error")
                    #print(login.errors)

    return render_template('login_form.html', title='Login',login=login)

@app.before_request
def load_user_from_cookie():
    if 'user_id' not in session and 'stay_signed_in' in request.cookies:
        token = request.cookies.get('stay_signed_in')
        usr = user.query.filter_by(token=token).first()
        if usr:
            session['user_id'] = usr.id
            login_user(usr)


@app.route('/logout')
def log_out():
    session.pop('user_id', None)
    make_response('Logged out').delete_cookie('stay_signed_in')
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
        ##print(users)

    return f"{users}"

@app.route("/contact", methods=["POST", "GET"])
def contact_us():

    contact_form = Contact_Form()
    if request.method == "POST":
        if contact_form.validate_on_submit():
            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
                app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

                mail = Mail(app)

                msg = Message(contact_form.subject.data, sender=contact_form.email.data, recipients=[em])
                msg.body = f"""{contact_form.message.data}
{contact_form.email.data}
                    """

                try:
                    mail.send(msg)
                    flash("Your Message has been Successfully Sent!!", "success")
                    return "Email Sent"
                except Exception as e:
                    # print(e)
                    flash(f'Ooops Something went wrong!! Please Retry', 'error')
                    return "The mail was not sent"

                # Send the pwd reset request to the above email
            send_link()

            #print("Posted")
        else:
            flash("Please be sure to fill both email & message fields, correctly","error")

    return render_template("contact_page.html",contact_form=contact_form)


@app.route("/companies")
def companies():

    companies_list = company_user.query.all()

    return render_template("companies.html",companies_list=companies_list)

@app.route("/reset/<token>", methods=['POST', "GET"])
def reset(token):
    from sqlalchemy import update
    reset_form = Reset()

    #print("Current User: ",current_user.__dict__)

    if request.method == 'POST':
        # if reset_form.validate_on_submit():
            # if current_user.is_authenticated:
            #     #Current User Changing Password
            #     #....script compares
            #     if encry_pw.check_password_hash(current_user.password, reset_form.old_password.data):
            #         # token = Tokenise().get_reset_token(current_user.id)
            #         #print("Reset Token: ", token)
            #         # v_user_id = Tokenise().verify_reset_token(token)
            #         #print("User_id: ", v_user_id)
            #
            #         pass_reset_hash_lc = encry_pw.generate_password_hash(reset_form.new_password.data)
            #
            #         usr = user.query.get(current_user.id)
            #         usr.password = pass_reset_hash_lc
            #         db.session.commit()
            #
            #         # logout_user()
            #
            #         flash(f"Password Changed Successfully!", "success")
            #         return redirect(url_for("login"))
            #     else:
            #         flash(f"Ooops! Passwords don't match, You might have forgotten your Old Password", "error")
            # else:

            try:
                flash(f"Trying to Reset Please wait","success")
                usr_obj = user_class().verify_reset_token(token)
                flash(f"User Id {usr_obj}", "success")
                pass_reset_hash = encry_pw.generate_password_hash(reset_form.new_password.data)
                usr_obj = user.query.get(usr_obj)
                usr_obj.password = pass_reset_hash
                db.session.commit()

                flash(f"Password Changed Successfully!", "success")

                return redirect(url_for("login"))
            except:
                print("Password Reset Failed!!")
                flash(f"Password Reset Failed, Please try again later", "error")
                return None


    return render_template("pass_reset.html",reset_form=reset_form)


@app.route("/reset_request", methods=['POST', "GET"])
def reset_request():

    reset_request_form = Reset_Request()

    #print("Current User: ",current_user.__dict__)

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            #Get user details through their email
            usr_email = user.query.filter_by(email=reset_request_form.email.data).first()
            #print("DEBUG EMAIL: ",usr_email.email)

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash("The email you are requesting a password reset for, is not registered with T.H.T, please register as account first", 'error')

                return redirect(url_for("reset_request"))

                # redirect(url_for())

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.body = f"""Good day, {usr_email.name}
                
You have requested a password reset for your The Hustlers Time Account.
To reset your password, visit the following link:{url_for('reset', token=token, _external=True)}

If you did not requested the above message please ignore it, and your password will remain unchanged.
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:
                    #print(e)
                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"

            #Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("reset_request.html", reset_request_form=reset_request_form)


@app.route("/how_does_it_work")
def tht_how():

    return render_template("how_does_it_work.html")


@app.route("/job_ads_form", methods=["POST","GET"])
@login_required
def job_ads_form():

    job_ad_form = Job_Ads_Form()
    job_ads_model = Jobs_Ads

    db.create_all()

    if request.method == 'POST':
       if job_ad_form.validate_on_submit():
            job_post1 = job_ads_model(
                job_title=job_ad_form.job_title.data,
                description = job_ad_form.description.data,
                category = request.form.get('field_category_sel'),
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
                #print('Job Type: ', job_ad_form.pay_type_bl.data)
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

            if not request.form.get('field_category_sel'):
                job_post1.category = job_ad_form.category.data

            #print("Check Category: ",request.form.get('field_category_sel'))
            db.session.add(job_post1)
            db.session.commit()

            flash('Your Job Post was succesfull', 'success')

    return render_template("job_ads_form.html",job_ad_form=job_ad_form)


@app.route("/fl_job_ads_form", methods=["POST","GET"])
@login_required
def fl_job_ads_form():

    fl_job_ad_form = Freelance_Ads_Form()
    fl_job_ads_model = Freelance_Jobs_Ads

    db.create_all()

    if request.method == 'POST':
       if fl_job_ad_form.validate_on_submit():
            job_post1 = fl_job_ads_model(
                service_title=fl_job_ad_form.service_title.data,
                specialty=request.form.get('speciality'),
                description = fl_job_ad_form.description.data,
                project_duration = fl_job_ad_form.project_duration.data,
                # other_info=fl_job_ad_form.prerequisites.data,
                service_category = request.form.get('field_category_sel'),
                contact_person = fl_job_ad_form.posted_by.data,
                # date_posted = datetime.utcnow(),
                application_deadline=fl_job_ad_form.application_deadline.data,
                job_posted_by = current_user.id
                          )

            # if bools are True
            if not request.form.get('speciality'):
                job_post1.service_title = fl_job_ad_form.speciality.data
            if not request.form.get('field_category_sel'):
                job_post1.service_category = fl_job_ad_form.service_category.data
            if fl_job_ad_form.benefits_bl.data:
                job_post1.benefits = fl_job_ad_form.benefits.data

            db.session.add(job_post1)
            db.session.commit()

            flash('Your Freelance Job Post was succesfull', 'success')

    return render_template("fl_job_ads_form.html",fl_job_ad_form=fl_job_ad_form)


@app.route("/all_users")
def users():
    from sqlalchemy import text

    user_v = []
    al_users = user.query.all()

    ea_usr = [usr_obj for usr_obj in al_users]

    # all_users = text("SELECT * FROM user;")
    # for ea_user in db.execute(al_users):
    #     users.append(list(ea_user))

    return render_template("users.html",al_users=al_users )


@app.route("/company_retieve")
def cmp_user_profile():
    from sqlalchemy import text

    users = []
    all = text('''SELECT * FROM job_applications;''')
    # db has binded the engine's database file
    for ea_user in db.execute(all):
        users.append(list(ea_user))
        ##print(users)


    return f"{users}"



@app.route("/job_ads",methods=["GET", "POST"])
def job_adverts():

    if current_user.is_authenticated:
        #print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")

    no_image_fl = 'static/images/default.jpg'

    db.create_all()
    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()
    job_ads_form = Job_Ads_Form()
    if request.method == 'GET':
        id = request.args.get('id')
        value = request.args.get('value')
        #print("Check Get Id: ",id)
        if id:
            #Filter Ads with a specific company's id
            job_ads = Jobs_Ads.query.filter_by(job_posted_by=id)
        elif not value and not id:
            job_ads = Jobs_Ads.query.all()
            print("ESLE is Printed: ")


    # Fix jobs adds does not have hidden tag
    return render_template("job_ads_gui.html",job_ads=job_ads,job_ads_form=job_ads_form,db=db,
                           company_user=company_user,user=usr,no_image_fl =no_image_fl)

@app.route("/job_ads_filtered",methods=["GET", "POST"])
def job_adverts_filtered():


    if current_user.is_authenticated:
        #print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")

    no_image_fl = 'static/images/default.jpg'

    db.create_all()
    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()
    job_ads_form = Job_Ads_Form()
    if request.method == 'GET':

        value = request.args.get('value')
        print("Check Get Id: ",value)

        job_ads = Jobs_Ads.query.filter(Jobs_Ads.category.like(f"{value}%")).all()
        print("Check Get Id: ", job_ads)


    # Fix jobs adds does not have hidden tag
    return render_template("job_ads_filtered.html",job_ads=job_ads,job_ads_form=job_ads_form,db=db,
                           company_user=company_user,user=usr,no_image_fl =no_image_fl)

@app.route("/freelance_job_ads", methods=["GET", "POST"])
def freelance_job_adverts():

    if current_user.is_authenticated:
        # print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields","error")
        else:
            pass
    else:
        pass

    no_image_fl = 'static/images/default.jpg'

    db.create_all()
    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()

    if request.method == 'GET':
        id = request.args.get('id')
        # print("Check Get Id: ",id)
        if id:
            # Filter Ads with a specific company's id
            fl_job_ads = Freelance_Jobs_Ads.query.filter_by(job_posted_by=id)
        else:
            fl_job_ads = Freelance_Jobs_Ads.query.all()

    fl_job_ads_form = Freelance_Ads_Form()

    # Fix jobs adds does not have hidden tag
    return render_template("freelance_jobs_ui.html", fl_job_ads=fl_job_ads, fl_job_ads_form=fl_job_ads_form, db=db,
                           company_user=company_user, user=usr, no_image_fl=no_image_fl)
@app.route("/send_application_fl", methods=["GET","POST"])
@login_required
def send_application_fl():

    send_application = FreeL_Applications()

    db.create_all()

    if not current_user.image and not current_user.school:
        redirect(url_for('account'))
        flash("Warning!! Your Account needs to be updated Soon, You won't be able to send Application if not so", "error")

    else:
        if current_user.is_authenticated:

            if request.method == "GET":
                tender_id=request.args['tender_id']
                apply = FreeL_Applications(
                    applicant_id = current_user.id,
                    jfreel_job_details_id = tender_id, #db.query(Jobs_Ads).get(jb_id),
                    employer_id = Freelance_Jobs_Ads.query.get(tender_id).job_posted_by
                )

                #Check if application not sent before
                job_obj = FreeL_Applications.query.filter_by(jfreel_job_details_id =tender_id).first()
                company_obj = company_user.query.get(apply.employer_id)

                #print('----------------------job_obj: ',job_obj)
                if not job_obj:
                    db.session.add(apply)
                    db.session.commit()
                    return render_template("send_application.html", send_application=send_application, job_obj=job_obj,
                                           company_obj=company_obj)
                else:
                    # fl = flash(f"Application with this details Already Submitted!!", "error")
                    return f'''This Application Already Submitted before.
                     Please Wait for a Reply!!'''


    return f'Something went Wrong, Please return to the previuos page'

@app.route("/tender_ad_opened", methods=["GET", "POST"])
def view_tender():

    if request.method == 'GET':
        id = request.args['id']

        tender_ad = Freelance_Jobs_Ads.query.get(id)

        #print("Job Ad Title: ",job_ad.job_title)


    return render_template('tender_ad_opened.html',item=tender_ad,db=db,company_user=company_user)


#------------------------------COMPANIES DATA-------------------------------#

@app.route("/company_sign_up", methods=["POST","GET"])
def company_sign_up_form():

    company_register = Company_Register_Form()

    db.create_all()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if company_register.validate_on_submit():

        if request.method == 'POST':
            # context

            # If the webpage has made a post e.g. form post

            #print('Create All..........................................')
            company_hashd_pwd = encry_pw.generate_password_hash(company_register.company_password.data).decode('utf-8')
            # Base.metadata.create_all()
            # ....user has inherited the Base class
            # db.create_all()
            user1 = company_user(name=company_register.company_name.data, email=company_register.company_email.data, password=company_hashd_pwd,
                                 confirm_password=company_hashd_pwd ,company_contacts=company_register.company_contacts.data,image="default.jpg",
                                 company_address=company_register.company_address.data, web_link=company_register.website_link.data,fb_link=company_register.facebook_link.data,
                                 twitter_link=company_register.twitter_link.data,youtube=company_register.youtube_link.data)

            db.session.rollback()

            try:
                try:
                    db.session.add(user1)
                    db.session.commit()
                    flash(f"Account Successfully Created for {company_register.company_name.data}", "success")
                except exc.IntegrityError:
                    flash(f"This email is already registered on this platform, Please use a regeister a different email", "error")
                    return render_template("company_signup_form.html",company_register=company_register)
                except Exception as e:
                    db.session.rollback()
                    flash(f"Something went wrong, Please re-enter your details", "error")
                    return redirect(url_for('company_sign_up_form'))
                return redirect(url_for('login'))
            except:
                flash(f"Something went wrong, check for errors", "error")
                Register().validate_email(company_register.company_email.data)

            return redirect(url_for('login'))

                # #print(company_register.name.data,company_register.email.data)
    elif company_register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(company_register.errors)


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
            # #print(f"Account Successfully Created for {company_login.name.data}")
            company_user_login = company_user.query.filter_by(email = company_login.company_email.data).first()
            # flash(f"Hey! {user_login.password} Welcome", "success")
            if company_user_login and encry_pw.check_password_hash(company_user_login.password,company_login.company_password.data):
                login_user(company_user_login)
                #After company_login required prompt, take me to the page I requested earlier
                req_page = request.args.get('next')
                flash(f"{company_user_login.name.title()} You're Logged In!", "success")
                return redirect(req_page) if req_page else redirect(url_for('home'))
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                #print(company_login.errors)

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
        cmp_usr = company_user.query.get(id)

        #print('DEBUG UPDATE 1: ', cmp_usr.web_link)

        if company_update.company_logo.data:
            #print("Debug Image on If: ", company_update.company_logo.data)
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

        db.session.commit()

        #print('DEBUG UPDATE: ',cmp_usr.web_link)

    return render_template("company_account.html",company_update = company_update,image_fl=image_fl)

#-------------------PARTNERING COMPANIES----------------------#
@app.route("/partnering_companies",methods=["GET", "POST"])
def partnering_companies():

    job_ads = Jobs_Ads.query.all()


    # Fix jobs adds does not have hidden tag
    return render_template("partnering_companies.html",job_ads=job_ads,job_ads_form=job_ads_form,db=db,
                           company_user=company_user,user=usr,no_image_fl =no_image_fl)




@app.route("/send_application", methods=["GET","POST"])
@login_required
def send_application():

    send_application = Applications()

    db.create_all()

    if not current_user.image and not current_user.school:
        redirect(url_for('account'))
        flash("Warning!! Your Account needs to be updated Soon, You won't be able to send Application if not so", "error")

    else:
        if current_user.is_authenticated:

            if request.method == "GET":
                jb_id = request.args['job_id']
                apply = Applications(
                    applicant_id = current_user.id,
                    jfreel_job_details_id= jb_id, #db.query(Jobs_Ads).get(jb_id),
                    employer_id = Jobs_Ads.query.get(jb_id).job_posted_by
                )

                #Check if application not sent before
                job_obj = Applications.query.filter_by(jfreel_job_details_id=jb_id).first()
                company_obj = company_user.query.get(apply.employer_id)

                #print('----------------------job_obj: ',job_obj)
                if not job_obj:
                    db.session.add(apply)
                    db.session.commit()
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
        job_ad = Jobs_Ads.query.get(id)

        #print("Job Ad Title: ",job_ad.job_title)


@app.route("/job_ad_opened", methods=["GET", "POST"])
def view_job():

    if request.method == 'GET':
        id = request.args['id']

        job_ad = Jobs_Ads.query.get(id)

        #print("Job Ad Title: ",job_ad.job_title)


    return render_template('job_ad_opened.html',item=job_ad,db=db,company_user=company_user)


@app.route("/verified/<token>", methods=["POST", "GET"])
#Email verification link verified with a token
def verified(token):

    #Check to verify the token received from the user email
    #process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    # if current_user.is_authenticated:
    #     # usr_obj = user_class().verify_reset_token(token)
    #     check_hash = encry_pw.check_password_hash(token,current_user.is_authenticated+str(current_user.id))
    #     flash(f'User ID is {token} is found','error')
    #

    try:
        usr = user.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            qry_usr = user.query.get(user_id)
            if not current_user.is_authenticated:
                login_user(usr)
            flash(f"Welcome, {qry_usr.name} ;verified {qry_usr.verified}; Your Email Verification was Successful!!","success")
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Something went wrong, Please try again: {e} ","error")


    return render_template('verified.html')


@app.route("/verification", methods=["POST","GET"])
#User email verification @login
#@login the user will register & when the log in the code checks if the user is verified first...
def verification():
    #Manage DB tables
    db.create_all()

    def send_veri_mail():
        if current_user.is_authenticated:

            app.config["MAIL_SERVER"] = "smtp.googlemail.com"
            app.config["MAIL_PORT"] = 587
            app.config["MAIL_USE_TLS"] = True
            #Creditentials saved in environmental variables
            em = app.config["MAIL_USERNAME"] = "pro.dignitron@gmail.com" #os.getenv("MAIL")
            app.config["MAIL_PASSWORD"] = os.getenv("PWD")

            mail = Mail(app)

            token = user_class().get_reset_token(current_user.id)

            # try:
            #     usr_verified = user.query.get(current_user.id)
            #     token = encry_pw.generate_password_hash(current_user.email + str(current_user.id)).decode("utf-8")
            #     if not usr_verified:
            #
            #         store_hash = Email_Verifications(generated_hash = token, time_stamp = datetime.utcnow())
            #         print('HASH: ',token)
            #
            #         # db.session.rollback()
            #         db.session.add(store_hash)
            #         db.session.commit()
            #     else:
            #         usr_verified.generated_hash = token;

            # except Exception as e:
            #     flash("Something is wrong, Please try again later", 'error')
            #     print("ERROR: ", e)
            #
            #     return redirect(url_for('verification'))

            #user_class().get_reset_token(current_user.id)
            usr_email = current_user.email
            # print("Debug Token: ", token)
            # print("DEBUG CURRENT USER EMAIL: ",current_user.email)
            # print("DEBUG CURRENT DEFAULT EMAIL: ", em)

            msg = Message("Email Verification", sender="noreply@demo.com", recipients=[usr_email])

            msg.body = f"""Hi, {current_user.name}
Please follow the link below to verify your email with The Hustlers Time:
verify email here,{url_for('verified', token=token, _external=True)}
"""
            try:
                mail.send(msg)
                flash(f'An email has been sent with a verification link to your email account {current_user.verified}', 'success')
                return "Email Sent"
            except Exception as e:
                print("DEBUG ERROR: ", e)
                flash(f'Email not sent here\n {e}', 'error')
                return "The mail was not sent"

    if not current_user.verified:
        send_veri_mail()
    else:
        return redirect(url_for("home"))

    return render_template('verification.html')

@app.route("/job_applications",methods=["GET", "POST"])
def applications():

    #Get all applications from Applications database
    all_applications = Applications.query.all()

    #print("Debug Application List: ", db.query(job_user).get(all_applications[0].applicant_id).name )

    applications = Applications()

    job_usr = job_user
    job_ads = Jobs_Ads

    return render_template("applications.html", all_applications = all_applications, job_user = job_usr, job_ads = job_ads, applications = applications,db=db)

@app.route("/view_applicant")
def view_applicant():

    if request.method == 'GET':
        id = request.args['id']
        job_usr = job_user.query.get(id)

    return render_template("view_applicant.html", job_usr = job_usr)

@app.route("/hire_applicant")
def hire_applicant():

    if request.method == 'GET':
        id = request.args['id']
        job_usr = job_user.query.get(id)

    return render_template("hire_applicant.html", job_usr = job_usr,db=db)


if __name__ == "__main__":


    app.run(debug=True)
