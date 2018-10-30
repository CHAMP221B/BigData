#!/usr/bin/python3
print("content-type: text/html")
print("")

import os
import subprocess as sp
import cgi,cgitb
cgitb.enable()
data=cgi.FieldStorage()
month=data.getvalue('month')
year=data.getvalue('year')
print(month)
code='''
#!/usr/bin/python

import sys
for i in sys.stdin:
        j=i.split(',')
        year=j[1]
        month=j[2]
        type=j[29]
	if(month=="{0}" and year=="{1}"):
        	print(month+" "+year+" "+type),
'''.format(month,year)

sp.getoutput("sudo touch /m.py")
sp.getoutput("sudo chown apche /m.py")
sp.getoutput("sudo chmod 777 /m.py")

f=open('/m.py','w')
f.write(code)
f.close()

code='''
#!/usr/bin/python
import sys
for i in sys.stdin:
	j=i.split(',')
        print("<tr>")
	print("<td>"+j[0]+"</td>")
	print("<td>"+j[1]+"</td>")
	print("<td>"+j[2]+"</td>")
	print("</tr>")
'''

sp.getoutput("sudo touch /r.py")
sp.getoutput("sudo chown apche /r.py")
sp.getoutput("sudo chmod 777 /r.py")

f=open('/r.py','w')
f.write(code)
f.close()

sp.getoutput("sshpass -p redhat scp -o stricthostkeychecking=no /m.py root@192.168.43.160:/")
sp.getoutput("sshpass -p redhat scp -o stricthostkeychecking=no /r.py root@192.168.43.160:/")

sp.getoutput('sshpass -p redhat ssh -o stricthostkeychecking=no -l root 192.168.43.160 hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input /terrorism.csv -mapper "./m.py" file /m.py -reducer "./r.py" -file /r.py -output /terror4')

output =sp.getoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root 192.168.43.160 hadoop fs -cat /terror5/part-00000")
print("<table>")

print("<tr>")
print("<th>Year</th>")
print("<th>Month</th>")
print("<th>Attack Type</th>")
print("</tr>")

print(output)

print("</table")
