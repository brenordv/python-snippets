import os
import mods.mymod

if __name__ == "__main__":
    main_path = os.getcwd()
    print("Main script path: %s" % main_path)
    
    mods.mymod.where_am_i()