from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mssql+pyodbc://sa:mnxjqqjxlJQXI!Cx@THUNDEROBOT\\SQLEXPRESS/fastapi_users?driver=ODBC+Driver+17+for+SQL+Server")
SessionLocal = sessionmaker(bind = engine)
