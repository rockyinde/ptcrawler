import os

cmd = 'sort /tmp/videos | uniq > /tmp/videos.uniq'
os.system(cmd)
