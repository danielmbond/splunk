#Create a splunk dashboard using UNIX TA
index = "log-lx-prod" #set this to your index name
mount1 = "/" #set this to whatever you like
mount2 = "/srv/" #set this to whatever you like or delete it

cpulines = []
memlines = []
disk1lines = []
disk2lines = []
str = ""
bool = True

panel = """\

    </panel>
    <panel>

\
"""
top = """\
<dashboard>
  <label>Host Health Summary</label>
  <description>https://starbucks.splunkcloud.com/en-US/app/search/oracle_ebs/edit#</description>
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
cpu = """\
      <html>
        <a href="linux_server_cpu_usages?form.host_token=LINUXSERVERNAME" target="Host CPU">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAME</b> 
        </a>
      </html>
      <viz type="cuviz_water_gauge.water_gauge">
        <search>
          <query>earliest="-5m" latest="now" index=log-lx-prod host=LINUXSERVERNAME* sourcetype=cpu  CPU=all| eval host=mvindex(split(host,"."),0) |eval cpupct=100-pctIdle | stats  avg(cpupct) as average | eval average=round(average,2)</query>
          <earliest>0</earliest>
          <latest></latest>
          <refresh>30s</refresh>
          <refreshType>delay</refreshType>
        </search>
        <option name="cuviz_water_gauge.water_gauge.circleColor">#009688</option>
        <option name="cuviz_water_gauge.water_gauge.circleFillGap">0.08</option>
        <option name="cuviz_water_gauge.water_gauge.circleThickness">0.08</option>
        <option name="cuviz_water_gauge.water_gauge.displayPercent">true</option>
        <option name="cuviz_water_gauge.water_gauge.height">125</option>
        <option name="cuviz_water_gauge.water_gauge.maxValue">100</option>
        <option name="cuviz_water_gauge.water_gauge.minValue">0</option>
        <option name="cuviz_water_gauge.water_gauge.textColor">#045681</option>
        <option name="cuviz_water_gauge.water_gauge.textSize">1</option>
        <option name="cuviz_water_gauge.water_gauge.textVertPosition">.5</option>
        <option name="cuviz_water_gauge.water_gauge.valueCountUp">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimate">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimateTime">50000</option>
        <option name="cuviz_water_gauge.water_gauge.waveColor">#ff5722</option>
        <option name="cuviz_water_gauge.water_gauge.waveCount">1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeight">0.1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeightScaling">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveOffset">0</option>
        <option name="cuviz_water_gauge.water_gauge.waveRise">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveRiseTime">1000</option>
        <option name="cuviz_water_gauge.water_gauge.waveTextColor">#A4DBf8</option>
        <option name="cuviz_water_gauge.water_gauge.width">125</option>
        <option name="height">125</option>
        <option name="refresh.display">none</option>
      </viz>\
"""
mem = """\
      <html>
        <a href="linux_server_memory_usage?form.host_token=LINUXSERVERNAME" target="Host Memory">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAME</b> 
        </a>
      </html>
      <viz type="cuviz_water_gauge.water_gauge">
        <search>
          <query>earliest="-5m" latest="now" index=log-lx-prod host=LINUXSERVERNAME* sourcetype=vmstat |eval host= mvindex(split(host,"."),0) | stats avg(memUsedPct) as avgmem |eval avgmem=round(avgmem, 2)</query>
          <earliest>0</earliest>
          <latest></latest>
          <refresh>30s</refresh>
          <refreshType>delay</refreshType>
        </search>
        <option name="cuviz_water_gauge.water_gauge.circleColor">#388e3c</option>
        <option name="cuviz_water_gauge.water_gauge.circleFillGap">0.05</option>
        <option name="cuviz_water_gauge.water_gauge.circleThickness">0.08</option>
        <option name="cuviz_water_gauge.water_gauge.displayPercent">true</option>
        <option name="cuviz_water_gauge.water_gauge.height">125</option>
        <option name="cuviz_water_gauge.water_gauge.maxValue">100</option>
        <option name="cuviz_water_gauge.water_gauge.minValue">0</option>
        <option name="cuviz_water_gauge.water_gauge.textColor">#045681</option>
        <option name="cuviz_water_gauge.water_gauge.textSize">1</option>
        <option name="cuviz_water_gauge.water_gauge.textVertPosition">.5</option>
        <option name="cuviz_water_gauge.water_gauge.valueCountUp">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimate">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveAnimateTime">50000</option>
        <option name="cuviz_water_gauge.water_gauge.waveColor">#e91e63</option>
        <option name="cuviz_water_gauge.water_gauge.waveCount">1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeight">0.1</option>
        <option name="cuviz_water_gauge.water_gauge.waveHeightScaling">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveOffset">0</option>
        <option name="cuviz_water_gauge.water_gauge.waveRise">true</option>
        <option name="cuviz_water_gauge.water_gauge.waveRiseTime">1000</option>
        <option name="cuviz_water_gauge.water_gauge.waveTextColor">#A4DBf8</option>
        <option name="cuviz_water_gauge.water_gauge.width">125</option>
        <option name="height">125</option>
        <option name="refresh.display">none</option>
      </viz>\
"""
disk = """\
      <html>
        <a href="linux_server_disk_usage?form.time_token.earliest=-7d%40d&amp;form.time_token.latest=now&amp;form.host_token=LINUXSERVERNAME" target="Host disk">
        <b style="color:blue;text-decoration:none;text-align:left;font-size:10px;">LINUXSERVERNAME</b> 
        </a>
      </html>
      <viz type="cuviz_water_gauge.water_gauge">
        <search>
          <query>earliest=-4h latest=now index=log-lx-prod (host=LINUXSERVERNAME*) sourcetype=df mount="LINUXMOUNT" | head 1 | eval UsePct=rtrim(UsePct, "%") | table UsePct</query>
          <earliest>0</earliest>
          <latest></latest>
        </search>
        <option name="cuviz_water_gauge.water_gauge.circleColor">#795548</option>
        <option name="cuviz_water_gauge.water_gauge.circleFillGap">0.05</option>
        <option name="cuviz_water_gauge.water_gauge.circleThickness">0.08</option>
        <option name="cuviz_water_gauge.water_gauge.displayPercent">true</option>
        <option name="cuviz_water_gauge.water_gauge.height">125</option>
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
bottom = """\
    </panel>
  </row>
</dashboard>\
"""
cpu = cpu.replace("log-lx-prod",index)
mem = mem.replace("log-lx-prod",index)
disk = disk.replace("log-lx-prod",index)

print("Input server name and press enter twice when done.\n")

try:
    while bool:
        str = input()
        if len(str) < 1:
            bool = False
        else:
            if str.find(".") > -1:
                str = str[0:str.find(".")]
            cpulines.append(cpu.replace("LINUXSERVERNAME",str))
            memlines.append(mem.replace("LINUXSERVERNAME",str))
            disk1lines.append(disk.replace("LINUXSERVERNAME",str).replace("LINUXMOUNT",mount1))
            if len(mount2) > 0:
                print(len(mount2))
                disk2lines.append(disk.replace("LINUXSERVERNAME",str).replace("LINUXMOUNT",mount2))
except EOFError:
    pass

cpulines = "\n".join(cpulines)
memlines = "\n".join(memlines)
disk1lines = "\n".join(disk1lines)

if len(disk2lines) > 0:
    disk2lines = "\n".join(disk2lines)

top = top.replace("MOUNT1",mount1).replace("MOUNT2",mount2)

print(top,cpulines,panel,memlines,panel,disk1lines,panel,disk2lines,bottom)

