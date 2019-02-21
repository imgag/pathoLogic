import atexit
import os
import pickle

picklePath = os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'pathoLogic.pickle')
# Global dict serves as database
if os.path.isfile(picklePath):
    db = pickle.load(open(picklePath, 'rb'))
else:
    db = {}
    db['samples'] = {}
    db['runs'] = {}
    db['status'] = {}

def goodbye(db):
    pickle.dump(db, open(os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'pathoLogic.pickle'), 'wb'))

atexit.register(goodbye, db)