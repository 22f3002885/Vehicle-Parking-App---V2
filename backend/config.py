class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECURITY_PASSWORD_SALT = 'mad-2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False