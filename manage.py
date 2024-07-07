import sys
from alembic.config import main

if __name__ == "__main__":
    sys.argv.append("upgrade")
    sys.argv.append("head")
    main()
