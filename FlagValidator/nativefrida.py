import frida
import sys
import re

def on_message(message, data):
    global index, filename
    if message['type'] == 'send':
            print("[*] {0}".format(message['payload'].encode('utf-8')))
    else:
        print(message)

def get_script():
    jscode = """
Java.perform(function() {

    var classDef = Java.use('org.team_sik.flagvalidator.MainActivity');

    var nativeValue = classDef.value;

    nativeValue.implementation = function(){
        var ret = nativeValue.call(this);
        send("Part 3 => " + ret);
        return ret;
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
    if len(sys.argv) == 2:
        print "[+] Waiting for app called {0}".format(sys.argv[1])
        process = attach_to_process(sys.argv[1])
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
    else:
        print "Usage: {0} <package>".format(sys.argv[0])
