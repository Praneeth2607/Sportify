"# Authentication Project" 

 **ABOUT THIS PROJECT**

 This project is a secure authentication system built using Django. It includes essential authentication features with a strong focus on security and user experience. The key features of this authentication system are:

>>> **User Authentication:** Users can sign up, log in, change passwords, and log out securely.

>>> **Email-Based Password Reset:** Users receive a password reset link via email, which expires in 10 minutes for enhanced security.

>>> **Restricted Access:** Users cannot access the home page without logging in or creating an account.

>>> **Login Required After Signup:** New users must log in again after signing up before accessing the home page.

>>> **Email Verification for Password Reset:** To prevent unauthorized resets, Users can only reset their passwords using the same email linked to their accounts.

This authentication system is designed to ensure a secure and seamless user experience while protecting user credentials and access.


**HOW TO SETUP AND RUN THIS PROJECT**

1.) **Clone the Repository**

   git clone <your-repo-url>
   
   cd full-authentication/authenticationproject
   
2.) **Create a Virtual Environment**

Ensure you have pipenv installed:

   pip install pipenv

Create and activate a virtual environment:

   pipenv shell

3.) **Install Dependencies**

   pipenv install

4.) **Set Up Environment Variables**
   
Create a .env file in the project's root directory and add:

   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=465
   EMAIL_USE_SSL=True
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password

5.) **Apply Database Migrations**

   python manage.py migrate

6.) **Create a Superuser (Optional, for Admin Panel)**

   python manage.py createsuperuser
   
Follow the prompts to create an admin account.

7.) **Run the Server**

   python manage.py runserver
   
Access the application at: http://127.0.0.1:8000/

**NOTE**

>>> **Do NOT commit .env to GitHub.** Ensure it's listed in .gitignore?

>>> To use a different database, update the DATABASES setting in settings.py.

>>> To customize authentication, modify the core app inside the project.

Enjoy the project! 🚀

 ************************************************************************************************************************************************************************************************************************************************************************************
