import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '3d6f45a5fc12445dbac2f59c3b6c7cb1d3c11316384af4638bbc8e5f0babcc2f'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'dog_spots.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
