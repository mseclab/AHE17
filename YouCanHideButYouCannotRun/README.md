# AHE17 : Android Hacking Events 2017

## **You Can Hide - But You Cannot Run** ([YouCanHideButYouCannotRun.apk](https://team-sik.org/wp-content/uploads/2017/06/YouCanHideButYouCannotRun.apk_.zip) Jamaica in the Dashboard)

**Hint**

Something is going on inside this app, don't know what it's doing. I have the feeling a secret message is transmitted somehow, somewhere... can you help me find the secret message?

## Write-up

by [svetrini](https://github.com/ningod)

After installing the YouCanHideButYouCannotRun.apk on your device or emulator you can see only a black background with a Caesar's image and a *start* button, pushing it the label changes to *running* but nothing else happens.

### Static Analysis

Let's see inside  `YouCanHideButYouCannotRun.apk` with a decompiler like [jadx or with jadx-gui](https://github.com/skylot/jadx)

```bash
$ jadx -d YouCanHideButYouCannotRun.jadx YouCanHideButYouCannotRun.apk
[...]
tree YouCanHideButYouCannotRun.jadx/hackchallenge/ahe17/teamsik/org/romanempire/         
YouCanHideButYouCannotRun.jadx/hackchallenge/ahe17/teamsik/org/romanempire/
├── BuildConfig.java
├── MainActivity.java
├── MakeThreads.java
├── R.java
└── threads
    ├── X04c3eb5ce6c5e299ad93dac871bbbed16da09e21.java
    ├── X04e5009b4e4a32ffe7fceca119ea2d939b3ad7d0.java
    ├── X07ee33e4bb59fd268d5cc7200578668347eb96ec.java
    ├── X0a3d206b39888aa391e974a8c54eea7286dc524d.java
    ├── X0b29ab3e1b0160417fc49c7759046c195acdc0e2.java
[...]
├── Xfee882c1e9b3200f9ada43bc430571e0295d0ded.java
└── Xfffb8e85796e61b713c68833d9f84ef0958681aa.java

1 directory, 191 files
```

We can see the `MainActivity.java` is the first activity loaded at the startup as described in 'AndroidManifest.xml'

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="1" android:versionName="1.0" package="hackchallenge.ahe17.teamsik.org.romanempire" platformBuildVersionCode="25" platformBuildVersionName="7.1.1">
    <uses-sdk android:minSdkVersion="15" android:targetSdkVersion="25" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <application android:theme="@style/AppTheme" android:label="@string/app_name" android:icon="@mipmap/ic_launcher" android:debuggable="true" android:allowBackup="true" android:supportsRtl="true" android:roundIcon="@mipmap/ic_launcher_round">
        <activity android:name="hackchallenge.ahe17.teamsik.org.romanempire.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```
Inside `MainActivity.java` we notice a call to  **MakeThreads** class

```java
 MakeThreads.startWrites(MainActivity.this);
```

The `MakeThreads.java` contains the code to access in read/write mode to a `scroll.txt` file using many different thread classes, but when you look at the file on device you get it's useless.

```java
public static void startWrites(Activity activity) {
     File directory = new File(activity.getApplicationInfo().dataDir + "/Rome");
     directory.mkdirs();
     File scroll = new File(directory, "scroll.txt");
     try {
         RandomAccessFile raf = new RandomAccessFile(scroll, "rw");
         PrintWriter pw = new PrintWriter(new FileOutputStream(scroll));
         threads = new ArrayList();
         threads.add(new X4bc86a15e3dc7ff7dca5240422059c40ca55f084(raf));
[...]
    threads.add(new X1b629eed17073f7c9d6b318b77ab05bb453692f4(raf));
    } catch (FileNotFoundException e) {
     e.printStackTrace();
    } catch (IOException e2) {
     e2.printStackTrace();
    }
    Iterator it = threads.iterator();
    while (it.hasNext()) {
     ((Thread) it.next()).start();
   }
}
```

All the threads classes write their own char `"c"` local char to the file at position 0, overwriting the content each time. All the class are similar to this:

```java
public class X4bc86a15e3dc7ff7dca5240422059c40ca55f084 extends Thread {
    RandomAccessFile a;
    char c = 'l';
    long sleepTillTime = 169000;
    int timetoSleep = 250;

    public X4bc86a15e3dc7ff7dca5240422059c40ca55f084(RandomAccessFile a) {
        this.a = a;
    }

    public void run() {
        try {
            Thread.sleep(this.sleepTillTime);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        try {
            this.a.seek(0);
            this.a.writeChar(this.c);
            this.a.writeChar(10);
        } catch (IOException e2) {
            e2.printStackTrace();
        }
    }
}
```
Between these classes only the value of `"c"` and value of `"sleepTillTime"` change, because of it we can analyze the code statically and find correct order of the chars but this may need too much time, so we skip to a dynamic analysis of the challenge.



### Dynamic Analysis

The tool used is [frida](https://www.frida.re/).
We can use it to hook the java methods `seek` and `writeChar` of the class `RandomAccessFile`, we need to hook both method to catch correctly when threads write the `"c"` char, i.e. after the *seek(0)* calls


We can use a python [script](multithreads.py) to achieve the goal; the python script is only an helper for the following frida javascript code:

```js
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
```


After pushing the button on the application, we got the following output:
```bash
python multithreads.py
[+] Waiting for app called hackchallenge.ahe17.teamsik.org.romanempire
[*] Attached on process
[*] Press enter to exit...
[*] index: 65
A
[*] PARTIAL:A
[*] index: 111
o
[...]
[*] index: 33
!
[*] PARTIAL:Aol jsvjrdvyr ohz ybzalk Puav h zapmm tvklyu hya zahabl, Whpualk if uhabyl, svhaolk if aol Thzzlz, huk svclk if aol mld. Aol nlhyz zjylht pu h mhpslk ylcpchs: HOL17{IlaalyJyfwaZ4m3vyKpl}!
^CFLAG: Aol jsvjrdvyr ohz ybzalk Puav h zapmm tvklyu hya zahabl, Whpualk if uhabyl, svhaolk if aol Thzzlz, huk svclk if aol mld. Aol nlhyz zjylht pu h mhpslk ylcpchs HOL17{IlaalyJyfwaZ4m3vyKpl}!

```

Something strange: the frida output is not the flag...

> Aol jsvjrdvyr ohz ybzalk Puav h zapmm tvklyu hya zahabl, Whpualk if uhabyl, svhaolk if aol Thzzlz, huk svclk if aol mld. Aol nlhyz zjylht pu h mhpslk ylcpchs: HOL17{IlaalyJyfwaZ4m3vyKpl}!


*something*, like the package name *romanempire*  and the Caesar's image on the app, suggest me that the text is in [Caesar's Cipher](https://en.wikipedia.org/wiki/Caesar_cipher) :-)

Online there are many Caesar cipher decryption tools, for example [this](http://www.xarg.org/tools/caesar-cipher/)

We can choose one of them and try our text, the rotation is **19** and the result is this:

> The clockwork has rusted Into a stiff modern art statue, Painted by nature, loathed by the Masses, and loved by the few. The gears scream in a failed revival: AHE17{BetterCryptS4f3orDie}!

And from this we can extract the Flag

>  FLAG:  AHE17{BetterCryptS4f3orDie}

That's all folks!
