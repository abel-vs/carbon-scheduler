from src import scheduler
from src import interface
import sys

if __name__ == '__main__':
    print('🌱 Welcome to CAS 🌱\n')
    if not len(sys.argv) > 1:
        interface.main_menu()
    else:
        scheduler.main()