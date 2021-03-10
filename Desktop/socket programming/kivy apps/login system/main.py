from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd  # save user details
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,

        )
        print("connection successful")
    except OperationalError as e:
        print(f"the essor '{e}' occured")
    return connection


connection = create_connection("kivy", "postgres", "dalyzhee", "127.0.0.1", "5432")


# class to call popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()


# class to build GUI for popup window
class P(FloatLayout):
    pass


# a function to display the popup content
def popFun():
    show = P()
    window = Popup(title='Popup', content=show, size_hint=(None, None), size=(300, 300))
    window.open()


# a class to accept user info and store using csv
class LoginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):
        connection.autocommit = True
        cursor = connection.cursor()
        select_query = "SELECT email FROM public.users"
        cursor.execute(select_query)
        data = cursor.fetchall()
        if self.email.text != data:
            popFun()
        else:
            sm.current = 'logdata'  # switching screen

            # reset textinput widget
            self.email.text = ""
            self.pwd.text = ""


# a class to accept signup info
class SignupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):
        # user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]], columns=['Name', 'Email', 'Password'])
        connection.autocommit = True
        cursor = connection.cursor()
        select_query = "SELECT email FROM public.users"
        cursor.execute(select_query)
        email = cursor.fetchall()

        if self.email.text != "":
            if self.email.text != email:
                # user.to_csv('login.csv', mode='a', header=False, index=False)
                # name1 = self.name2.text
                # email1 = self.email.text
                # password1 = self.pwd.text
                insert_query = "INSERT INTO users (name, email, password) VALUES (name2, email, pwd)"
                cursor.execute(insert_query)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            popFun()


# class to display validation result
class LogDataWindow(Screen):
    pass


# class for managing screen
class windowManager(ScreenManager):
    pass


# kv file loader
kv = Builder.load_file('login.kv')
sm = windowManager()

sm.add_widget(LoginWindow(name='login'))
sm.add_widget(SignupWindow(name='signup'))
sm.add_widget(LogDataWindow(name='logdata'))


# a class that builds the GUI
class loginMain(App):
    def build(self):
        return sm


if __name__ == "__main__":
    loginMain().run()
