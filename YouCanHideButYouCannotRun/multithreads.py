"""
Allow to trace called methods and package
"""
import frida
import re

syms = []

def on_message(message, data):
    global syms
    global index, filename
    if message['type'] == 'send':
        if "SYM" in message["payload"]:
            c = message["payload"].split(":")[1]
            print c
            syms.append(c)
        else:
            print("[*] {0}".format(message["payload"]))
    else:
            print(message)


def overload2params(x):
    start = 97
    params = []
    count_re = re.compile('\((.*)\)')
    arguments = count_re.findall(x)
    if arguments[0]:
        arguments = arguments[0]
        arguments = arguments.replace(" ", "")
        arguments = arguments.split(",")
        for _ in arguments:
            params.append(chr(start))
            start += 1
        return ",".join(params)
    else:
        return ""


def get_script():
    jscode = """

Java.perform(function() {
    var flagArray = [];
    var randomfile = Java.use('java.io.RandomAccessFile');

    var skip = true;

    randomfile.seek.implementation = function(pos)
    {
        if (pos == 0){
            skip = false;
        }
        return randomfile.seek.call(this, pos);
    }

    randomfile.writeChar.implementation = function(c)
    {
        if(skip || c == 10)
        {
            send("PARTIAL:"+flagArray.join(""));   
        }else{
            send("index: "+c);
            flagArray.push(String.fromCharCode(c))
            send("SYM:"+String.fromCharCode(c));
        }
        return randomfile.writeChar.call(this, c);
    }

});
"""

    return jscode

def attach_to_process(proc_name):
    done = False
    process = None
    while not done:
        try:
            process = frida.get_usb_device().attach(proc_name)
            done = True
        except Exception:
            pass
    return process


if __name__ == "__main__":
    print "[+] Waiting for app called {0}".format("hackchallenge.ahe17.teamsik.org.romanempire")
    process = attach_to_process("hackchallenge.ahe17.teamsik.org.romanempire")
    script = get_script()
    try:
        script = process.create_script(script)
    except frida.InvalidArgumentError as e:
        message = e.args[0]
        line = re.compile('Script\(line (\d+)\)')
        line = int(line.findall(message)[0])
        script = script.split("\n")
        print "[-] Error on line {0}:\n{1}: {2}".format(line, line, script[line])
        exit(0)
    script.on('message', on_message)
    print('[*] Attached on process')
    print('[*] Press enter to exit...')
    script.load()
    try:
        raw_input()
    except KeyboardInterrupt:
        pass

    print "FLAG: " + "".join(syms)