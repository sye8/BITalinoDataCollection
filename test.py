import subprocess
import sys
import datetime
import time

filename = "test.mp4"
if sys.version_info[0] < 3:
    out = subprocess.check_output("ffmpeg -i " + filename + " 2>&1 | grep 'Duration'", shell=True).rstrip()
    print(out.split()[1].replace(',',''))
else:
    out = subprocess.getoutput("ffmpeg -i " + filename + " 2>&1 | grep 'Duration'")
    print(out.split()[1].replace(',',''))
vidDuration = time.strptime(out.split()[1].replace(',',''), "%H:%M:%S.%f")
print(datetime.timedelta(hours=vidDuration.tm_hour,minutes=vidDuration.tm_min,seconds=vidDuration.tm_sec).total_seconds()+1)

