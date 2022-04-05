import sys
import src.scheduler
import src.interface

def main():
    print('🌱 Welcome to CAS 🌱\n')
    if not len(sys.argv) > 1:
        src.interface.main_menu()
    else:
        src.scheduler.main()

if __name__ == '__main__':
    main()