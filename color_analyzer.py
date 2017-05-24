from weppy import App,url,request,session, now
#from weppy_bs3 import BS3
import os
from weppy.tools import service
from weppy.orm import Model, Field, belongs_to, has_many,Database
from weppy.tools import auth
from weppy.tools import Auth
from weppy.tools.auth import AuthUser


app = App(__name__)

#app.use_extension(BS3)
app.config.auth.single_template = True
app.config.auth.registration_verification = False
app.config.auth.hmac_key = "MassiveDynamicRules"

@app.route("/echo/<str:msg>")
def echo(msg):
    return dict(message=msg)

@app.command('setup')
def setup():
    # create the user
    user = User.create(
        email="4etvegr@gmail.com",
        first_name="ddd",
        last_name="444",
        password="pocketuniverse"
    )
    # create an admin group
    admins = auth.create_group("admin")
    # add user to admins group
    auth.add_membership(admins, user.id)
    db.commit()

@app.on_error(404)
def not_found():
    #code
    return "Page not found. What are you doing?!"

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/post/<int:id>/edit")
def edit(id):
    # code
    return ("your ID is: {0}".format(id))

@app.route("/time")
@service.json
def get_time():
    return "Current time is: ", request.now_local

@app.route("/listimages")
@service.json
def listimages():
    path=ur"/Users/4etvegr/Pictures"
    imagedict = {}
    id = 0
    try:
        for file in os.listdir(path):
            print("it works")
            if file.endswith(".jpg") or file.endswith("jpeg"):
                id += 1
                imagedict[id] = file
                #Image.create()
        #strout = ""
        #outvar = strout.join(imagelist)
    except:
        return "Wrong"
    #return(outvar)
    return imagedict

class User(AuthUser):
    # will create "users" table and groups/permissions ones
    has_many('images', 'comments')

class Image(Model):
    belongs_to('user')
    has_many('comments')

    id = Field('text')
    title = Field('text')
    path = Field('text')
    comment = Field('text')
    date = Field('datetime')

    default_values = {
        'user': lambda: session.auth.user.id,
        'date': lambda: now
    }
    validation = {
        'id': {'presence': True},
    }
    fields_rw = {
        'user': False,
        'date': False
    }


class Comment(Model):
    belongs_to('user', 'image')

    text = Field('text')
    date = Field('datetime')

    default_values = {
        'user': lambda: session.auth.user.id,
        'date': lambda: now
    }
    validation = {
        'text': {'presence': True}
    }
    fields_rw = {
        'user': False,
        'image': False,
        'date': False
    }

db = Database(app, auto_migrate=True)
auth = Auth(app, db, user_model=User)
db.define_models(Image, Comment)

if __name__ == "__main__":
    app.run()
    hello()
