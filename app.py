from flask import Flask, render_template


app = Flask(__name__)



users = {}
status = ""
@app.route('/')

        #start the login 


@app.route('/display_menu')    
def displayMenu():
        status = input("Are you registered user? y/n? Press q to quit")
        if status == "y":
            oldUser()
        elif status == "n":
            newUser()

@app.route('/new_user')       
def newUser():
        createLogin = input("Create login name: ")
    
        if createLogin in users:
            print("\nLogin name already exist!\n")
        else:
            createPassw = input("Create password: ")
            users[createLogin] = createPassw
            print("\nUser created\n")


@app.route('/old_user')       
def oldUser():
        login = input("Enter login name: ")
        passw = input("Enter password: ")
    
        if login in users and users[login] == passw:
            print("\nLogin successful!\n")
        else:
            print("\nUser doesn't exist or wrong password!\n")
    
        while status != "q":
             displayMenu()
        
    #end of login
    
        return render_template('index.html')


# def post(self):
    # data = UserRegister.parser.parse_args()
# 
    # if UserModel.find_by_username(data['username']):
        # return {"message": "A user with that username already exists"}, 400
# 
    # user = UserModel(**data)
    # user.save_to_db()
# 
    # return {"message": "User created successfully."}, 201

if __name__ == '__main__':
  app.run(debug=True)

