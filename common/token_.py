import hashlib
import uuid


def gen_token(user_id):
    md5_ = hashlib.md5()
    md5_.update((uuid.uuid4().hex + str(user_id)).encode('utf-8'))
    md5_.update('$!$@#@%@#Fa'.encode('utf-8'))
    return md5_.hexdigest()
