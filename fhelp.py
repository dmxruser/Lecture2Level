import os
import numpy as np
import re
import gzip
import base64

def encrypt_file(filepath, output_path):
    with open(filepath, 'rb') as f:
        with gzip.open(f, 'rb') as gz:
            data = gz.read()
    with open(output_path, 'wb') as f:
        f.write(data)
        f.write(base64.urlsafe_b64encode(data))
    return output_path

def output_file(fileoutput, data):
    with open(fileoutput, 'w') as f:
        f.write(f"""<?xml version="1.0"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://apple.com">
<plist version="1.0">
	<dict>
		<key>kCEK</key>
		<integer>4</integer>	
		<key>k2</key>
		<string>{os.path.splitext(os.path.basename(fileoutput))[0]}</string>
		<key>k3</key>
		<string></string>
		<key>k4</key>
		<string>{data}</string>
		<key>k5</key>
		<string>Not me</string>
		<key>k13</key>
		<true/>
		<key>k16</key>
		<integer>1</integer>
		<key>k46</key>
		<integer>1</integer>
		<key>k80</key>
		<integer>28</integer>
	</dict>
</plist>""")
    return fileoutput