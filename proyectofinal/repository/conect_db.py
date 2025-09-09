from sqlmodel import Session, create_engine

engine = create_engine("mysql+pymysql://root:Dalecolon123@localhost:3306/proyecto")



def get_session():
    return Session(engine)
