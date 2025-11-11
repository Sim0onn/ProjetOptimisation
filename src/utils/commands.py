import os 
from dotenv import load_dotenv

def loadVar(name,cast_type = 'str'):
    load_dotenv()
    VAR = os.getenv(name)
    if VAR is None:
        return None
    return cast_type(VAR) 
    