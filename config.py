import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key'  # 本番環境では安全な値に変更してください
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dog_spots.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False