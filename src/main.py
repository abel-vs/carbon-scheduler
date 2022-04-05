import sys

import scheduler
from interface import main_menu

if __name__ == '__main__':
    print('🌱 Welcome to CAS 🌱\n')
    if not len(sys.argv) > 1:
        main_menu()
    else:
        scheduler.main()
