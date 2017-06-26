"""
Hook on EVP_DecryptInit_ex
"""
import frida
import sys
import re
import base64


def get_messages_from_js(mess, data):
            print("{0} B64 --> {1}".format(mess['payload'], base64.b64encode(data)))


def get_script():
    jscode = """

console.log("Starting frida hooks on Process.arch:: "+Process.arch);

var decrypt = undefined;

var imports = Module.enumerateImportsSync("libnative-lib.so");

for(i = 0; i < imports.length; i++) {
    //console.log("imports["+i+"].name : "+imports[i].name)
    if(imports[i].name == "EVP_DecryptInit_ex") {
        decrypt = imports[i].address;
    }
}



if(decrypt){
    console.log("decrypt found at address: "+decrypt);
    Interceptor.attach(decrypt, {
                onEnter: function (args) {

                    //The Key in AES 256 is composed by 32 byte
                    var rawParamKey = Memory.readByteArray(ptr(args[3]),32);
                    var paramHexDump =hexdump(rawParamKey, { offset: 0, length: 32, header: true, ansi: true });

                    var msg = "[*] D Key "+ 3 + " " + args[3];
                    send("KEY",rawParamKey);
                    console.log(msg);
                    console.log(paramHexDump);

                    //The Key in IV 256 is composed by 16 byte
                    var rawParamIv = Memory.readByteArray(ptr(args[4]),16);
                    var paramHexDump = hexdump(rawParamIv, { offset: 0, length: 16, header: true, ansi: true });

                    var msg = "[*] D IV "+ 4 + " " + args[4];
                    send("IV",rawParamIv);
                    console.log(msg);
                    console.log(paramHexDump);
                }
    });
}

"""
    return jscode


def attach_to_process(proc_name):
    done = False
    proc = None
    while not done:
        try:
            proc = frida.get_usb_device().attach(proc_name)
            done = True
        except Exception:
            pass
    return proc


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
        script.on('message', get_messages_from_js)
        print('[*] Attached on process')
        print('[*] Press enter to exit...')
        script.load()
        try:
            raw_input()
        except KeyboardInterrupt:
            pass
    else:
        print "Usage: {0} <package>".format(sys.argv[0])
