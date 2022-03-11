import sys
from directory_manager import DirectoryManager
from get_parameters import get_user_parameters

if len(sys.argv) == 1:
    sys.argv.extend(("localhost,test,1234,yd", "c:\\test", "2", "30", "32"))

if __name__ == "__main__":
    # get parameters from command line
    ftp_website, local_directory, max_depth, refresh_frequency, excluded_extensions, threadNumber = get_user_parameters()

    # init directory manager with local directory and maximal depth and threadNumber
    directory_manager = DirectoryManager(ftp_website, local_directory, max_depth, excluded_extensions, threadNumber)

    # launch the synchronization
    directory_manager.synchronize_directory(refresh_frequency)