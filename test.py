#!/usr/bin/python3    -     
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pytz import timezone

f = open("/home/ubuntu/test2/test.txt", 'w')

now = datetime.now(timezone('Asia/Seoul'))
text = now.strftime('%Y-%m-%d %H:%M:%S') 
f.write(text)
f.close()
print("10시 50분에 시행")