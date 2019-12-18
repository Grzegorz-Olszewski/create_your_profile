# Create your profile
Application that allows user to login with his Github credentials and create/edit/delete/update his personal profile

# Installation
1. Clone repository ```git clone git@github.com:Grzegorz-Olszewski/create_your_profile.git```
2. Install docker-compose https://github.com/Yelp/docker-compose/blob/master/docs/install.md
3. Using terminal go to project directory and run ```docker-compose up --build```
4. Application is running on http://localhost:8000/


# Running tests and checking test coverage

1. When project is running on one terminal tab open second one. Go to project directory and run ```docker-compose exec backend bash```
2. Run ```coverage run --source='.' manage.py test core``` and ```coverage html ```
3. To see coverage report find htmlcov directory in project and open index.html file in a browser.
