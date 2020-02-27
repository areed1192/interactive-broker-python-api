# Starting the IB Java Server

The Interactive Broker API is authenticated using a server written in Java. To use the API, the server must be running so that authenticated request can be made. To run the server, you need to pass through the following commands in the terminal or command console. The command arguments will change depending on the operating system you are using.

You must be in the `clientportal.gw` folder when you run these commands.

**Run Command For MacOS Terminal:**

``` bash
cd ../ib-robot/clientportal.gw
"bin/run.sh" "root/conf.yaml"
```

**Run Command For Windows Terminal:**

``` bash
cd ..\ib-robot\clientportal.gw
"bin/run.bat" "root/conf.yaml"
```
