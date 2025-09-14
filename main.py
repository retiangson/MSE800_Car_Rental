# main.py
from Business.Services.Installer import ServiceInstaller
from ui.MainMenu import run

if __name__ == "__main__":
    print("Starting Car Rental System.........")
    installer = ServiceInstaller()
    run(installer)   # pass installer into run
