from ...database import connectdb, models
from ...schema import data
from ...util import time_message
import time

def get_userdetails_by_userid(userid:int) -> models.UserDetail:
    start = time.time()
    
    with connectdb.session() as db:
        response = db.query(models.UserDetail).filter(models.UserDetail.id == userid).first()
    time_message("Get userdetails with id {} execution time".format(userid), time.time()-start)
    return response

def update_userbalance_by_userid(user:models.User, balancechange:float) -> models.UserDetail:
    """update balance

    Args:
        userid (int): userid
        balancechange (float): positive for increase balance (insert money) and negative for decrease balance (pay money)

    Returns:
        models.UserDetail: updated userdetail
    """
    start = time.time()
    with connectdb.session() as db:
        dbuserdetail = get_userdetails_by_userid(userid=user.id)
        dbuserdetail.balance = round(dbuserdetail.balance + balancechange, 2)
        db.add(dbuserdetail)
        db.commit()
        db.refresh(dbuserdetail)
        time_message("User {} balance remaining: {} . The change was: {}".format(user.username, dbuserdetail.balance, balancechange), time.time()-start)
    return dbuserdetail