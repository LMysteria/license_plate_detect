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

def get_transaction_by_userid_parkingid(userid:int, parkingdataid:int) -> models.TransactionDetail:
    start = time.time()
    with connectdb.session() as db:
        response = db.query(models.TransactionDetail).filter(models.TransactionDetail.userid == userid and
                                                             models.TransactionDetail.parkingdataid == parkingdataid).first()
    time_message("Get transaction with userid {} and parkingdataid {} execution time".format(userid, parkingdataid), time.time()-start)
    return response

#UPDATE
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

def update_transaction_change(parkingdataid:int, userid:int, change:float):
    start = time.time()
    with connectdb.session() as db:
        dbtransaction = get_transaction_by_userid_parkingid(userid=userid, parkingdataid=parkingdataid)
        dbtransaction.balancechanges = round(change,2)
        db.add(dbtransaction)
        db.commit()
        db.refresh(dbtransaction)
        time_message("Update Transaction \"change\" to {} with userid {} and parkingdataid {} ".format(round(change,2), userid, parkingdataid), time.time()-start)
    return dbtransaction
    

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