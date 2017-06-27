# AHE17 : Android Hacking Events 2017

## **Why Should I Pay?** ([WhyShouldIPay.apk](https://team-sik.org/wp-content/uploads/2017/06/WhyShouldIPay.apk_.zip) - Panama in the Dashboard)

**Hint**

This app is useluss without premium, but why would you pay for something if you can get it for free?

## Write-up

by [svetrini](https://github.com/ningod)


Let's start by running the challenge inside an emulator, the interface shows us a text box for the license and two button:

* **VERIFY**: return an error, Server unreachable
* **PREMIUM CONTENT**: tell us the App is not activated

### Static Analysis

Let's see inside  `WhyShouldIPay.apk` with a decompiler like [jadx or with jadx-gui](https://github.com/skylot/jadx)

```bash
$ tree WhyShouldIPay/de/fraunhofer/sit/premiumapp/
WhyShouldIPay/de/fraunhofer/sit/premiumapp/
├── BuildConfig.java
├── LauncherActivity.java
├── MainActivity.java
└── R.java

0 directories, 4 files
```

We can see the `MainActivity.java` and `LauncherActivity.java` classes loaded by 'AndroidManifest.xml', the App start from the last one.
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="1" android:versionName="1.0" package="de.fraunhofer.sit.premiumapp" platformBuildVersionCode="25" platformBuildVersionName="7.1.1">
    <uses-sdk android:minSdkVersion="19" android:targetSdkVersion="25" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    <application android:theme="@style/AppTheme" android:label="Not Premium App" android:icon="@mipmap/ic_launcher" android:debuggable="true" android:allowBackup="true" android:supportsRtl="true" android:roundIcon="@mipmap/ic_launcher_round">
        <activity android:name="de.fraunhofer.sit.premiumapp.MainActivity" />
        <activity android:name="de.fraunhofer.sit.premiumapp.LauncherActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

Inside *LauncherActivity* class we can see:

**verifyClick** attached to the *VERIFY* button, call an external (broken) server to check the license code from app, if it succeed than save the string "LICENSEKEYOK" XOR device MAC Address to the shared preferences

```java
public void verifyClick(View v) {
     try {
         InputStream in = new URL("http://broken.license.server.com/query?license=" + ((EditText) findViewById(R.id.text_license)).getText().toString()).openConnection().getInputStream();
         StringBuilder responseBuilder = new StringBuilder();
         byte[] b = new byte[0];
         while (in.read(b) > 0) {
             responseBuilder.append(b);
         }
         String response = responseBuilder.toString();
         if (response.equals("LICENSEKEYOK")) {
             String activatedKey = new String(MainActivity.xor(getMac().getBytes(), response.getBytes()));
             Editor editor = getApplicationContext().getSharedPreferences("preferences", 0).edit();
             editor.putString("KEY", activatedKey);
             editor.commit();
             new Builder(this).setTitle((CharSequence) "Activation successful").setMessage((CharSequence) "Activation successful").setIcon(17301543).show();
             return;
         }
         new Builder(this).setTitle((CharSequence) "Invalid license!").setMessage((CharSequence) "Invalid license!").setIcon(17301543).show();
     } catch (Exception e) {
         new Builder(this).setTitle((CharSequence) "Error occured").setMessage((CharSequence) "Server unreachable").setNeutralButton((CharSequence) "OK", null).setIcon(17301543).show();
     }
 }
```

**showPremium** attached to the *PREMIUM CONTENT* button, launch the *premium* MainActivity passing it device MAC Address and saved key from shared preferences
```java
 public void showPremium(View view) {
     Intent i = new Intent(this, MainActivity.class);
     i.putExtra("MAC", getMac());
     i.putExtra("KEY", getKey());
     startActivity(i);
 }

```

Inside *MainActivity* class we notice a call to native library used by *stringFromJNI* method inside *onCreate*

```java
static {
    System.loadLibrary("native-lib");
}

protected void onCreate(Bundle savedInstanceState) {
    String key = getIntent().getStringExtra("KEY");
    String mac = getIntent().getStringExtra("MAC");
    if (key == "" || mac == "") {
        key = "";
        mac = "";
    }
    super.onCreate(savedInstanceState);
    setContentView((int) R.layout.activity_main);
    ((TextView) findViewById(R.id.sample_text)).setText(stringFromJNI(key, mac));
}
```

Now our anlysis is ended and we can start bypassing controls.
### Bypass controls

The tool used is [frida](https://www.frida.re/), We can use it to hook all the **LauncherActivity** methods and force the App to pass desired parameters to JNI method.

We can use a python [script](bypass.py) to achieve the goal; the python script is only an helper for the following frida javascript code:

```js
Java.perform(function() {
    var flagArray = [];
    var activity = Java.use('de.fraunhofer.sit.premiumapp.LauncherActivity');

    //Force Key
    activity.getKey.implementation = function(){
        console.log('getKey called');
        //Precomputed "LICENSEKEYOK" xor "02:00:00:00:00:00" in Hex
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

    //Bypass url check and call directly premium
    activity.verifyClick.implementation = function(view)
    {
        console.log('verify cliccked');
        return activity.showPremium.call(this,view);
    }
```

```bash
$ python bypass.py
[+] Waiting for app called de.fraunhofer.sit.premiumapp
[*] Attached on process
[*] Press enter to exit...
verify cliccked
getMac called
02:00:00:00:00:00
getKey called
getMac called
02:00:00:00:00:00
getKey called

Bypassed...
```

After pushing the VERIFY button we get the flag on device screen:

> FLAG: AHE17{pr3mium4ctiv4yed}

That's all folks!
