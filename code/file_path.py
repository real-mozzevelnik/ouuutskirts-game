import sys, os

# if u need to go one direction down
def res(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    x =  os.path.join(base_path, relative_path)
    # if '../' in x:
    #     x = x.replace('../', '',1)
    return x