from ..auth import authcrud

def update_user_role(username: str, rolename: str) -> bool:
    try:
        dbuser = authcrud.get_user_by_username(username=username)
        dbrole = authcrud.get_role_by_name(name=rolename)
        authcrud.update_role(user=dbuser, role=dbrole)
        return True
    except Exception as e:
        raise e