from ...database import connectdb, models
from ...schema import data
from ...util import time_message
import time

def get_userdetails_by_userid(userid:int) -> models.UserDetail:
    
    with connectdb.session() as db:
        response = db.query(models.UserDetail).filter(models.UserDetail.id == userid).first()
    return response

def get_transaction_by_userid_parkingid(userid:int, parkingdataid:int) -> models.TransactionDetail:
    with connectdb.session() as db:
        response = db.query(models.TransactionDetail).filter(models.TransactionDetail.userid == userid and
                                                             models.TransactionDetail.parkingdataid == parkingdataid).first()
    return response

def get_transaction_by_parkingid(parkingdataid:int) -> models.TransactionDetail:
    with connectdb.session() as db:
        response = db.query(models.TransactionDetail).filter(models.TransactionDetail.parkingdataid == parkingdataid).first()
    return response

#UPDATE
def update_userbalance(user:models.User, balancechange:float) -> models.UserDetail:
    """update balance

    Args:
        userid (int): userid
        balancechange (float): positive for increase balance (insert money) and negative for decrease balance (pay money)

    Returns:
        models.UserDetail: updated userdetail
    """
    with connectdb.session() as db:
        dbuserdetail = get_userdetails_by_userid(userid=user.id)
        dbuserdetail.balance = round(dbuserdetail.balance + balancechange, 2)
        db.add(dbuserdetail)
        db.commit()
        db.refresh(dbuserdetail)
    return dbuserdetail

def update_transaction_change(parkingdataid:int, userid:int, change:float):
    with connectdb.session() as db:
        dbtransaction = get_transaction_by_userid_parkingid(userid=userid, parkingdataid=parkingdataid)
        dbtransaction.balancechanges = round(change,2)
        db.add(dbtransaction)
        db.commit()
        db.refresh(dbtransaction)
    return dbtransaction

def update_userphonenumber(user:models.User, phonenumber:str):
    with connectdb.session() as db:
        dbuserdetail = get_userdetails_by_userid(userid=user.id)
        dbuserdetail.phonenumber = phonenumber
        db.add(dbuserdetail)
        db.commit()
        db.refresh(dbuserdetail)
    return dbuserdetail
    
    

#CREATE
def create_transaction(user:models.User, balancechange:float, description:str, parkingdataid:int):
    start = time.time()
    with connectdb.session() as db:
        newtransaction = models.TransactionDetail(userid=user.id, balancechanges=round(balancechange,2), description=description, parkingdataid=parkingdataid)
        db.add(newtransaction)
        db.commit()
        db.refresh(newtransaction)
        time_message("Transaction details between user {} and parkingdataid {}".format(user.username, parkingdataid), time.time()-start)
    return newtransaction

def create_feedback(user:models.User, subject:str, detail:str) -> models.FeedBack:
    start = time.time()
    with connectdb.session() as db:
        newfeedback = models.FeedBack(userid=user.id, subject=subject, detail=detail)
        db.add(newfeedback)
        db.commit()
        db.refresh(newfeedback)
        time_message("User {} sent a feedback with subject {}".format(user.username, subject), time.time()-start)
    return newfeedback