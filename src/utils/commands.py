import os 
from dotenv import load_dotenv

def loadVar(name,cast_type = 'str'):
    load_dotenv()
    VAR = os.getenv(name)
    if VAR is None:
        return None
    return cast_type(VAR) 

def update_env_seed(seed, path=".env"):
    lines = []
    seed_set = False

    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.startswith("SEED2="):
                    lines.append(f"SEED2={seed}\n")
                    seed_set = True
                else:
                    lines.append(line)

    if not seed_set:
        lines.append(f"SEED2={seed}\n")

    with open(path, "w") as f:
        f.writelines(lines)
