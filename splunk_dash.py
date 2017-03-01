#Create a Splunk dashboard using UNIX TA
import csv
import os  
from tkinter import Tk
from random import randint

index = "log-lx-prod" #set this to your index name
label = "Host Health Summary"

chartBegin = ""
chartSelection = dict()
cpu = ""
cpulines = []
cpuSearch = ""
disk1 = ""
disk1lines = []
disk1Search = ""
disk2 = ""
disk2lines = []
disk2Search = ""
labelinput = ""
mem = ""
memlines = []
memSearch = ""
options = ""
selection = 0
server = ""
serverinfo = ""
randomMin = 30
randomMax = 600
randomrefresh = 0
bool = True

# If a server-info.csv exists the details URL will have the information
# after the server name.  CSV format is: servername,details
serverinfoexist = os.path.isfile('server-info.csv')    # Returns True if exists, else False
if serverinfoexist:
    reader = csv.reader(open('server-info.csv'))
    serverinfohash = dict()
    for row in reader:
        key = row[0]
        if key in serverinfohash:
            # implement your duplicate row handling here
            pass
        serverinfohash[key] = row[1:]

chartSelection = {
        1: 'Radial Gauge',
        2: 'Filler Gauge',
        3: 'Marker Gauge',
        4: 'Water Gauge',
    }

while selection == 0:
    for chart in chartSelection:
        print(chart,":",chartSelection[chart], sep="")
    try:
        selection = int(input())
    except:
        print("\nIntegers only please.\n")

if selection > 0 and selection < 4:
    chartBegin = "\n\t<chart>\n"
    options = """\

        <option name="charting.chart">radialGauge</option>
        <option name="charting.chart.rangeValues">[0,60,80,100]</option>
        <option name="charting.chart.style">minimal</option>
        <option name="charting.gaugeColors">["0x84E900","0xFFE800","0xBF3030"]</option>
        <option name="height">126</option>
        <option name="refresh.display">none</option>
      </chart>
\
"""
    if selection == 2:
        options = options.replace("radialGauge","fillerGauge")
    elif selection == 3:
        options = options.replace("radialGauge","markerGauge")

else:
    chartBegin = '<viz type="cuviz_water_gauge.water_gauge">'
    options = """\
        <option name="cuviz_water_gauge.water_gauge.circleColor">#795548</option>
        <option name="cuviz_water_gauge.water_gauge.circleFillGap">0.05</option>
        <option name="cuviz_water_gauge.water_gauge.circleThickness">0.08</option>
        <option name="cuviz_water_gauge.water_gauge.displayPercent">true</option>
        <option name="cuviz_water_gauge.water_gauge.height">126</option>
        <option name="cuviz_water_gauge.water_gauge.maxValue">100</option>
        <option name="cuviz_water_gauge.water_gauge.minValue">0</option>
        <option name="cuviz_water_gauge.water_gauge.textColor">#045681</option>
        <option name="cuviz_water_gauge.water_gauge.textSize">1</option>
        <option name="cuviz_water_gauge.water_gauge.textVertPosition">.5</option>
        <option name="cuviz_water_gauge.water_gauge.valueCountUp">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimate">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimateTime">50000</option>
        <option name="cuviz_water_gauge.water_gauge.waveColor">#8e24aa</option>
        <option name="cuviz_water_gauge.water_gauge.waveCount">1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeight">0.1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeightScaling">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveOffset">0</option>
        <option name="cuviz_water_gauge.water_gauge.waveRise">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveRiseTime">1000</option>
        <option name="cuviz_water_gauge.water_gauge.waveTextColor">#A4DBf8</option>
        <option name="cuviz_water_gauge.water_gauge.width">125</option>
        <option name="height">125</option>
      </viz>\
"""
cpu = """\
      <html>
        <a href="linux_server_cpu_usages?form.host_token=LINUXSERVERNAME" target="Host CPU">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAMESERVERINFO</b> 
        </a>
      </html>\
"""
mem = """\
      <html>
        <a href="linux_server_memory_usage?form.host_token=LINUXSERVERNAME" target="Host Memory">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAMESERVERINFO</b> 
        </a>
      </html>\
"""
disk1 = """\
      <html>
        <a href="linux_server_disk_usage?form.time_token.earliest=-7d%40d&amp;form.time_token.latest=now&amp;form.host_token=LINUXSERVERNAME" target="Host disk">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAMESERVERINFO</b> 
        </a>
      </html>\
"""
disk2 = """\
      <html>
        <a href="linux_server_disk_usage?form.time_token.earliest=-7d%40d&amp;form.time_token.latest=now&amp;form.host_token=LINUXSERVERNAME" target="Host disk">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAMESERVERINFO</b> 
        </a>
      </html>\
"""

cpuSearch = """\
        <search>
          <query>earliest="-5m" latest="now" index=log-lx-prod host=LINUXSERVERNAME* sourcetype=cpu  CPU=all| eval host=mvindex(split(host,"."),0) |eval cpupct=100-pctIdle | stats  avg(cpupct) as average | eval average=round(average,2)</query>
          <earliest>0</earliest>
          <latest></latest>
          <refresh>REFRESHTIMERs</refresh>
          <refreshType>delay</refreshType>
        </search>\
"""
memSearch = """\
        <search>
          <query>earliest="-5m" latest="now" index=log-lx-prod host=LINUXSERVERNAME* sourcetype=vmstat | eval host=mvindex(split(host,"."),0) | stats avg(memUsedPct) as avgmem |eval avgmem=round(avgmem, 2)</query>
          <earliest>0</earliest>
          <latest></latest>
          <refresh>REFRESHTIMERs</refresh>
          <refreshType>delay</refreshType>
        </search>\
"""
disk1Search = """\
        <search>
          <query>earliest=-2h latest=now index=log-lx-prod (host=LINUXSERVERNAME*) sourcetype=df | search NOT nfs NOT *cdrom* |	dedup mount |	sort -UsePct | head 1 | eval UsePct=rtrim(UsePct, "%") | table UsePct</query>
          <earliest>0</earliest>
          <latest></latest>
        </search>\
        """
disk2Search = """\
        <search>
          <query>earliest=-2h latest=now index=log-lx-prod (host=LINUXSERVERNAME*) sourcetype=df | search NOT nfs NOT *cdrom* |	dedup mount |	sort -UsePct | head 2 | tail 1 | eval UsePct=rtrim(UsePct, "%") | table UsePct</query>
          <earliest>0</earliest>
          <latest></latest>
        </search>\
"""
panel = """\

    </panel>
    <panel>

\
"""

top = """\
<dashboard>
  <label>Host Health Summary</label>
  <description>https://github.starbucks.net/dbond/splunk</description>
  <row>
    <panel>
      <html>
        <a>
          <h1 style="color:#4caf50;text-align:center;font-size:20px;border:none;">CPU Utilization Details</h1>
        </a>
      </html>
    </panel>
    <panel>
      <html>
        <a>
          <h1 style="color:#4caf50;text-align:center;font-size:20px;">Memory Utilization Details</h1>
        </a>
      </html>
    </panel>
    <panel>
      <html>
        <a>
          <h1 style="color:#4caf50;text-align:center;font-size:20px;">Disk Utilization (MOUNT1)</h1>
        </a>
      </html>
    </panel>
    <panel>
      <html>
        <a>
          <h1 style="color:#4caf50;text-align:center;font-size:20px;">Disk Utilization (MOUNT2)</h1>
        </a>
      </html>
    </panel>
  </row>
  <row>
    <panel>\
"""

bottom = """\
    </panel>
  </row>
</dashboard>\
"""

cpu = cpu + chartBegin + cpuSearch + options
mem = mem + chartBegin + memSearch + options
disk1 = disk1 + chartBegin + disk1Search + options
disk2 = disk2 + chartBegin + disk2Search + options

top = top.replace("Host Health Summary",label)
cpu = cpu.replace("log-lx-prod",index)
mem = mem.replace("log-lx-prod",index)
disk1 = disk1.replace("log-lx-prod",index)
disk2 = disk2.replace("log-lx-prod",index)

print("Enter a description default =",label,":")
labelinput = input()

if len(labelinput) > 0:
    top = top.replace(label,labelinput)

print("Input server name and press enter twice when done.")

try:
    while bool:
        server = input()
        if len(server) < 1:
            bool = False
        else:
            if server.find(".") > -1:
                server = server[0:server.find(".")]
            if serverinfohash:
                try:
                    serverinfo = serverinfohash.get(server,"")
                    if serverinfo:
                        serverinfo = " " + serverinfo[0]
                except KeyError:
                    pass
            randomrefresh = str(randint(randomMin,randomMax))
            cpulines.append(cpu.replace("LINUXSERVERNAME",server).replace("SERVERINFO",serverinfo).replace("REFRESHTIMER",randomrefresh))
            memlines.append(mem.replace("LINUXSERVERNAME",server).replace("SERVERINFO",serverinfo).replace("REFRESHTIMER",randomrefresh))
            disk1lines.append(disk1.replace("LINUXSERVERNAME",server).replace("SERVERINFO",serverinfo))
            disk2lines.append(disk2.replace("LINUXSERVERNAME",server).replace("SERVERINFO",serverinfo))
except EOFError:
    pass

cpulines = "\n".join(cpulines)
memlines = "\n".join(memlines)
disk1lines = "\n".join(disk1lines)
disk2lines = "\n".join(disk2lines)

output = top + cpulines + panel + memlines + panel + disk1lines + panel + disk2lines + bottom

print(output)

r = Tk()
r.withdraw()
r.clipboard_clear()
print("Output copied to clipboard.")
r.clipboard_append(output)
#r.destroy()
