from sqlalchemy.orm import Session
from database.models import User



def create_user(db: Session, fname: str, lname: str | None = None):
    user_obj = User(firstname=fname, lastname=lname)
    
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return user_obj





def get_user(db: Session):
    return db.query(User).first()


def update_user(
    db: Session,
    user: User,
    firstname: str,
    lastname: str | None,
    bio: str | None,
):
    user.firstname = firstname.strip()
    user.lastname = lastname.strip() if lastname else None
    user.bio = bio.strip() if bio else None

    db.commit()
    db.refresh(user)

    return user
    