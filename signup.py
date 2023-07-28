from database import Database
from flask_bcrypt import bcrypt

def signUp(UserName,PassWord,Role):
    if isinstance(UserName, str) and isinstance(PassWord, str) and isinstance(Role, int):
        if Role > 0 and Role < 4:
            PassWord = bcrypt.hashpw(PassWord.encode('utf-8'), bcrypt.gensalt())
            query = "INSERT INTO Login (UserName, Password, Role) VALUES (?, ?, ?)"
            params = (UserName, PassWord.decode('utf-8'), Role)
            db.cursor.execute(query, params)
            db.connection.commit()
            print("Username added")


def updatePassword(UserName, NewPassword):
    if isinstance(UserName, str) and isinstance(NewPassword, str):
        hashed_password = bcrypt.hashpw(NewPassword.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE Login SET Password = ? WHERE UserName = ?"
        params = (hashed_password.decode('utf-8'), UserName)
        db.cursor.execute(query, params)
        db.connection.commit()
        print("Password updated")



def delete(UserName):
    query = "DELETE FROM Login WHERE UserName = ?"
    params = (UserName,)
    db.cursor.execute(query, params)
    db.connection.commit()
    print("Username deleted")



db = Database()
db.connectDB()
val = int(input('Sign Up = 1 \nDelete User = 2\nUpdate Password = 3\nEnter:'))
if val == 1:
    print("Create User")
    UserName = input('Enter a Username: ')
    PassWord = input('Enter a Password: ')
    Role = int(input('Enter a Role: '))
    signUp(UserName,PassWord,Role)
elif val == 2:
    UserName = input('Enter a Username: ')
    delete(UserName)
elif val == 3:
    print("Updating Password")
    UserName = input('Enter a Username: ')
    PassWord = input('Enter a Password: ')
    updatePassword(UserName,PassWord)

#  user: steve
# pwd: steve-hydro

# user gordon
# pwd: gordon-hydro

# user: makintunde
# pwd: 63LarkRidgeWay