import os
import sys
script_to_call = sys.argv[1]
shellscript_filename = './GoogleCode/' + script_to_call + '.sh'
with open(shellscript_filename) as f:
    for line in f:
        command_string = 'adb shell ' + line
        print(command_string)
        os.system(command_string)

