#Function to flatten
import os
import shutil


def flatt(parentDir,currentDir): # Credit - https://gist.github.com/oatkiller/4429244
            # get all the files in the current dir
            files = os.listdir(currentDir)
            
            for file in files:
                # get the path of the file relative to the dir its in
                # so "./file" or on successive runs: "./dir/file"
                joinedFile = os.path.join(currentDir,file)
                
                if os.path.isdir(joinedFile):
                    # run the dir function on dirs
                    flatt(parentDir,joinedFile)
                else: # its not a dir, its a file,
                    # dont move files in the parent dir into the parent dir =p
                    if parentDir != currentDir:
                        try:
                            # move it to the dir we are flattening into
                            shutil.move(joinedFile,parentDir)
                        except shutil.Error:
                            # use rename to overwrite existing files
                            os.rename(joinedFile,os.path.join(parentDir,file))
                
            
            # if we arent working on the parent dir, delete the now empty dir
            if parentDir != currentDir:
                os.rmdir(currentDir)