from common import rd


def save_code(phone, code):
    rd.set(phone, code, ex=120)  # 两分钟有效时间


def get_code(phone):
    return rd.get(phone)



def add_token(token, user_id):
    return rd.set(token, user_id, ex=3600 * 24 * 7)


def get_user_id(token):
    
    return rd.get(token)
