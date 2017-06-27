"""
Bypass license control
"""
import frida
import re

def get_script():
    jscode = """

Java.perform(function() {
    var flagArray = [];
    var activity = Java.use('de.fraunhofer.sit.premiumapp.LauncherActivity');

    //Force Key
    activity.getKey.implementation = function(){
        console.log('getKey called');
        //LICENSEKEYOK xor 02:00:00:00:00:00 in Hex
        var hex  = '7c7b79757e69757b7f697f717c7979757e';
        var str = '';
        for (var n = 0; n < hex.length; n += 2) {
            str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
        }
        return str;
    }

    //force Mac Address
    activity.getMac.implementation = function(){
        console.log('getMac called');
        var result = '02:00:00:00:00:00';
        return result;
    }
    
    //Bypass url check
    activity.verifyClick.implementation = function(view)
    {
        console.log('verify cliccked');
        return activity.showPremium.call(this,view);
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
    print "[+] Waiting for app called {0}".format("de.fraunhofer.sit.premiumapp")
    process = attach_to_process("de.fraunhofer.sit.premiumapp")
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
    print('[*] Attached on process')
    print('[*] Press enter to exit...')
    script.load()
    try:
        raw_input()
    except KeyboardInterrupt:
        pass
    print('Bypassed...')