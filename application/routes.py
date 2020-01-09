from application import app, db, api
from flask import render_template, request, Response, json, jsonify, redirect, flash, url_for, session
from application.models import User, Course, Enrollment
from application.course_list import course_list
from application.forms import LoginForm, RegisterForm
from flask_restplus import Resource

# courseData = courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]


############# APIs ##############

@api.route('/api', '/api/')
class GetAndPost(Resource):

    # Get All users
    def get(self):
        return jsonify(User.objects.all())
    
    # POST to insert a new user
    def post(self):
        data = api.payload
        user = User(user_id=data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    # Get required user
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT request to Updata a current user
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    # DELETE request to Delete a user
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User has been deleted")



############# ROUTING #############

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, You are sucessfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, try again", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("+courseID")
    return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("Your are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')
    
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Ooops! You are already registered in {courseTitle}!", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"{user_id} is enrolled in {courseTitle}!", "success")

    classes = course_list(user_id)

    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)

# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if(idx == None):
#         jData = courseData
#     else:
#         jData = courseData[int(idx)]
#     return Response(json.dumps(jData), mimetype="application/json")


# class User(db.Document):
#     user_id = db.IntField( unique=True )
#     first_name = db.StringField( max_length=50 )
#     last_name = db.StringField( max_length=50 )
#     email = db.StringField( max_length=30 )
#     password = db.StringField( max_length=30 )

@app.route("/user")
def user():
    # User(user_id=5, first_name="Naeem", last_name="Ahmed", email="naeem@ahmed.com", password="abc123").save()
    # User(user_id=6, first_name="Abid", last_name="Jameel", email="abid@jameel.com",
    # password="abcd1234").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
