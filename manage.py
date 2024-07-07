# manage.py
import sys
import os
from dotenv import load_dotenv
from alembic.config import main

if __name__ == "__main__":
    load_dotenv()
    sys.argv.append("upgrade")
    sys.argv.append("head")
    main()
