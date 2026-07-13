#file created with functions that are used to encrypt passwords stored in the database - project_data
import bcrypt
#generating hash 
def generate_hash(pasw):
    salt = bcrypt.gensalt()
    byte_pasw = pasw.encode('utf-8')
    hash = bcrypt.hashpw(byte_pasw,salt)
    return hash.decode('utf-8')

#validate password using hash
def is_valid_hash(pasw,hash):
    hasH = hash.encode('utf-8')
    byte_pasw = pasw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_pasw,hasH)
    return is_valid