class Config:
    DEBUG = True  # Set to False in production
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://localhost/notasAlumnosDBD?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
