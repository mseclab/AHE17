# AHE17 : Android Hacking Events 2017

## **Token-Generator** ([Token-Generator.apk](https://team-sik.org/wp-content/uploads/2017/06/Token-Generator.apk_.zip) - Kongo in the Dashboard)

**Hint**

If you enter a flag in the app it will validate if it is the correct flag. To find the correct flag, which the validator will accept, just reverse the app. Attention: Token format is AHE17-THEFLAG

## Write-up

by [svetrini](https://github.com/ningod)

After installing the `Token-Generator.apk` on your device or emulator you can see a simple text field and a button:

*DON'T PUSH IT*...

*NEVER!*

### Static Analysis

Let's see inside  `Token-Generator.apk` with  [apktool](https://ibotpeaches.github.io/Apktool/)

We can see the classic folders and native library `lib/armeabi-v7a` folder

```bash
$ tree Token-Generator.apktool/lib
Token-Generator.apktool/lib
└── armeabi-v7a
    ├── libmonodroid.so
    └── libmonosgen-2.0.so

1 directory, 2 files
```

But also a *strange* folder `unknown` containing these files:

```bash
$ tree Token-Generator.apktool/unknown
dotNetChallenge.apktool/unknown
├── assemblies
│   ├── dotNetChallenge.dll
│   ├── Java.Interop.dll
│   ├── Mono.Android.dll
│   ├── Mono.Android.Export.dll
│   ├── mscorlib.dll
│   ├── System.Core.dll
│   ├── System.dll
│   ├── System.Runtime.Serialization.dll
│   ├── System.ServiceModel.Internals.dll
│   └── System.Xml.dll
├── environment
├── NOTICE
├── typemap.jm
└── typemap.mj

1 directory, 14 files

```

*Mono.Android.dll*... Mono?!? the open source version of the Microsoft .Net platform?

*Fe-fi-fo-fum, I smell the blood of a [Xamarin](https://www.xamarin.com) framework !*

And now? Let's start reversing mono code with last version of [Mono Develop](http://www.monodevelop.com/) the cross platform IDE for C# and more.


Opening the `dotNetChallenge.dll` with *Assembly Browser* we can disassembly it.
We find two classes: `MainActivity` and `MyService`

* *MyService*: is not very important, but remember **DON'T PUSH THE BUTTON!**
* *MainActivity*: contain all the interesting things.


```cs
[...]

namespace dotNetChallenge
{
    [Activity (Label = "dotNetChallenge", MainLauncher = true, Icon = "@drawable/icon")]
    public class MainActivity : Activity
    {
        //
        // Methods
        //
        private bool callNext (int cnt, Random rnd)
        {
            bool result;
            try {
                List<MethodInfo> methods = this.GetMethods ();
                int index = rnd.Next (methods.Count);
                MethodInfo methodInfo = methods [index];
                if (!(bool)methodInfo.Invoke (this, new object[] {
                    cnt + 1,
                    rnd
                })) {
                    result = false;
                }
                else {
                    string folderPath = Environment.GetFolderPath (Environment.SpecialFolder.MyDocuments);
                    List<MainActivity.z> list = new List<MainActivity.z> ();
                    foreach (string current in Directory.EnumerateFiles (folderPath)) {
                        if (Path.GetFileName (current).Length > 3) {
                            list.Add (new MainActivity.z {
                                str = current
                            });
                        }
                    }
                    base.RunOnUiThread (delegate {
                        TextView textView = base.FindViewById<TextView> (2131034115);
                        textView.Text = "Getting there...";
                        textView.Invalidate ();
                    });
                    IEnumerable<MainActivity.z> arg_DA_0 = list;
                    Func<MainActivity.z, bool> arg_DA_1;
                    if ((arg_DA_1 = MainActivity.<>c.<>9__10_1) == null) {
                        arg_DA_1 = (MainActivity.<>c.<>9__10_1 = new Func<MainActivity.z, bool> (MainActivity.<>c.<>9.<callNext>b__10_1));
                    }
                    List<MainActivity.z> list2 = arg_DA_0.Where (arg_DA_1).ToList<MainActivity.z> ();
                    foreach (MainActivity.z current2 in list2) {
                        this.k (current2.str);
                    }
                    list.Clear ();
                    base.RunOnUiThread (delegate {
                        TextView textView = base.FindViewById<TextView> (2131034115);
                        textView.Text = "Just a moment...";
                        textView.Invalidate ();
                    });
                    foreach (string current3 in Directory.EnumerateFiles (folderPath)) {
                        if (Path.GetFileName (current3).Length > 3) {
                            list.Add (new MainActivity.z {
                                str = current3
                            });
                        }
                    }
                    IEnumerable<MainActivity.z> arg_1AC_0 = list;
                    Func<MainActivity.z, bool> arg_1AC_1;
                    if ((arg_1AC_1 = MainActivity.<>c.<>9__10_3) == null) {
                        arg_1AC_1 = (MainActivity.<>c.<>9__10_3 = new Func<MainActivity.z, bool> (MainActivity.<>c.<>9.<callNext>b__10_3));
                    }
                    List<MainActivity.z> list3 = arg_1AC_0.Where (arg_1AC_1).ToList<MainActivity.z> ();
                    bool flag = false;
                    foreach (MainActivity.z current4 in list2) {
                        if (this.l (current4.str)) {
                            base.RunOnUiThread (delegate {
                                Toast.MakeText (this, "You got it!", ToastLength.Long).Show ();
                            });
                            flag = true;
                            break;
                        }
                    }
                    if (!flag) {
                        base.RunOnUiThread (delegate {
                            Toast.MakeText (this, "Scotty doesn't know...", ToastLength.Long).Show ();
                        });
                    }
                    base.RunOnUiThread (delegate {
                        TextView textView = base.FindViewById<TextView> (2131034115);
                        textView.Text = "Waiting for user input...";
                        textView.Invalidate ();
                    });
                    result = true;
                }
            }
            catch (Exception ex) {
                Console.WriteLine (ex.Message);
                result = false;
            }
            return result;
        }

        private List<MethodInfo> GetMethods ()
        {
            List<MethodInfo> list = new List<MethodInfo> ();
            MethodInfo[] methods = base.GetType ().GetMethods (BindingFlags.Instance | BindingFlags.NonPublic);
            for (int i = 0; i < methods.Length; i++) {
                MethodInfo methodInfo = methods [i];
                if (methodInfo.Name.StartsWith ("X")) {
                    list.Add (methodInfo);
                }
            }
            return list;
        }

        private void k (string str)
        {
            try {
                PackageInfo packageInfo = this.PackageManager.GetPackageInfo ("dotNetChallenge.dotNetChallenge", PackageInfoFlags.ResolvedFilter);
                byte[] array = packageInfo.Signatures [0].ToByteArray ();
                byte[] array2 = File.ReadAllBytes (str);
                string folderPath = Environment.GetFolderPath (Environment.SpecialFolder.MyDocuments);
                byte[] array3 = File.ReadAllBytes (folderPath + "/bar");
                Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes (array, array3, 100);
                byte[] bytes = rfc2898DeriveBytes.GetBytes (32);
                Random random = new Random ();
                ICryptoTransform transform = new RijndaelManaged {
                    BlockSize = 256,
                    Mode = CipherMode.CBC,
                    Padding = PaddingMode.PKCS7
                }.CreateEncryptor (bytes, array3);
                for (int i = 0; i < 10; i++) {
                    using (MemoryStream memoryStream = new MemoryStream ()) {
                        using (CryptoStream cryptoStream = new CryptoStream (memoryStream, transform, CryptoStreamMode.Write)) {
                            byte[] array4 = new byte[array2.Length];
                            array2.CopyTo (array4, 0);
                            int num = random.Next (3);
                            for (int j = 0; j < array.Length; j++) {
                                byte[] expr_D8_cp_0 = array;
                                int expr_D8_cp_1 = j;
                                expr_D8_cp_0 [expr_D8_cp_1] += (byte)num;
                            }
                            cryptoStream.Write (array4, 0, array4.Length);
                            byte[] bytes2 = memoryStream.ToArray ();
                            File.WriteAllBytes (folderPath + "/bar" + Guid.NewGuid (), bytes2);
                        }
                    }
                }
            }
            catch (Exception ex) {
                Console.WriteLine (ex.Message);
            }
        }

        private bool l (string str)
        {
            bool result;
            try {
                string folderPath = Environment.GetFolderPath (Environment.SpecialFolder.MyDocuments);
                byte[] rgbIV = File.ReadAllBytes (folderPath + "/bar");
                byte[] buffer = File.ReadAllBytes (str);
                byte[] rgbKey;
                using (SHA1Managed sHA1Managed = new SHA1Managed ()) {
                    rgbKey = sHA1Managed.ComputeHash (buffer);
                }
                RijndaelManaged rijndaelManaged = new RijndaelManaged ();
                rijndaelManaged.BlockSize = 256;
                rijndaelManaged.Mode = CipherMode.CBC;
                rijndaelManaged.Padding = PaddingMode.PKCS7;
                ICryptoTransform cryptoTransform = rijndaelManaged.CreateEncryptor (rgbKey, rgbIV);
                byte[] buffer2 = new byte[] {
                    17,
                    185,
                    186,
                    161,
                    188,
                    43,
                    253,
                    224,
                    76,
                    24,
                    133,
                    9,
                    201,
                    173,
                    255,
                    152,
                    113,
                    171,
                    225,
                    163,
                    121,
                    177,
                    211,
                    18,
                    50,
                    50,
                    219,
                    190,
                    168,
                    138,
                    97,
                    197
                };
                ICryptoTransform transform = rijndaelManaged.CreateDecryptor (rgbKey, rgbIV);
                using (MemoryStream memoryStream = new MemoryStream (buffer2)) {
                    using (CryptoStream cryptoStream = new CryptoStream (memoryStream, transform, CryptoStreamMode.Read)) {
                        using (StreamReader streamReader = new StreamReader (cryptoStream)) {
                            EditText editText = base.FindViewById<EditText> (2131034113);
                            string text = streamReader.ReadToEnd ();
                            if (text.Equals (editText.Text)) {
                                result = true;
                                return result;
                            }
                        }
                    }
                }
                result = false;
            }
            catch (Exception ex) {
                Console.WriteLine (ex.Message);
                result = false;
            }
            return result;
        }

        [Export ("onBeamClick")]
        public void onBeamClick (View v)
        {
            TextView textView = base.FindViewById<TextView> (2131034115);
            textView.Text = "Checking your password...";
            textView.Invalidate ();
            this.StartService (new Intent (this, typeof(MyService)));
            List<MethodInfo> methods = this.GetMethods ();
            Random rnd = new Random ();
            Thread thread = new Thread (delegate {
                MethodInfo methodInfo;
                do {
                    int index = rnd.Next (methods.Count);
                    methodInfo = methods [index];
                }
                while (!(bool)methodInfo.Invoke (this, new object[] {
                    0,
                    rnd
                }));
            });
            thread.Start ();
        }

        protected override void OnCreate (Bundle bundle)
        {
            base.OnCreate (bundle);
            this.SetContentView (2130903040);
            base.Title = "The Awesome Challenge";
            string folderPath = Environment.GetFolderPath (Environment.SpecialFolder.MyDocuments);
            List<MainActivity.z> list = new List<MainActivity.z> ();
            foreach (string current in Directory.EnumerateFiles (folderPath)) {
                File.Delete (current);
            }
            RijndaelManaged rijndaelManaged = new RijndaelManaged ();
            rijndaelManaged.BlockSize = 256;
            rijndaelManaged.Key = new byte[] {
                167,
                63,
                7,
                203,
                120,
                97,
                159,
                54,
                168,
                33,
                52,
                209,
                27,
                53,
                232,
                11,
                250,
                63,
                5,
                192,
                91,
                128,
                199,
                67,
                20,
                91,
                151,
                226,
                185,
                218,
                41,
                34
            };
            File.WriteAllBytes (folderPath + "/foo", rijndaelManaged.Key);
            rijndaelManaged.Clear ();
            rijndaelManaged.IV = new byte[] {
                8,
                173,
                47,
                130,
                199,
                242,
                20,
                211,
                63,
                47,
                254,
                173,
                163,
                245,
                242,
                232,
                11,
                244,
                134,
                249,
                44,
                123,
                138,
                109,
                155,
                173,
                122,
                76,
                93,
                125,
                185,
                66
            };
            File.WriteAllBytes (folderPath + "/bar", rijndaelManaged.IV);
            rijndaelManaged.Clear ();
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool Xa (int cnt, Random rnd)
        {
            return cnt <= 10 && this.callNext (cnt, rnd);
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool Xá (int cnt, Random rnd)
        {
            bool result;
            try {
                string text = "";
                using (Stream stream = this.Assets.Open ("someFile.txt")) {
                    using (StreamReader streamReader = new StreamReader (stream)) {
                        string str;
                        while ((str = streamReader.ReadLine ()) != null) {
                            text = text + str + "\n";
                        }
                    }
                }
                string folderPath = Environment.GetFolderPath (Environment.SpecialFolder.MyDocuments);
                byte[] rgbKey = File.ReadAllBytes (folderPath + "/foo");
                byte[] rgbIV = File.ReadAllBytes (folderPath + "/bar");
                ICryptoTransform transform = new RijndaelManaged {
                    BlockSize = 256,
                    Mode = CipherMode.CBC,
                    Padding = PaddingMode.PKCS7
                }.CreateEncryptor (rgbKey, rgbIV);
                for (int i = 0; i < 10; i++) {
                    using (MemoryStream memoryStream = new MemoryStream ()) {
                        using (CryptoStream cryptoStream = new CryptoStream (memoryStream, transform, CryptoStreamMode.Write)) {
                            byte[] bytes = Encoding.UTF8.GetBytes (text);
                            int num = rnd.Next (3);
                            for (int j = 0; j < bytes.Length; j++) {
                                byte[] expr_EF_cp_0 = bytes;
                                int expr_EF_cp_1 = j;
                                expr_EF_cp_0 [expr_EF_cp_1] += (byte)num;
                            }
                            cryptoStream.Write (bytes, 0, bytes.Length);
                            byte[] bytes2 = memoryStream.ToArray ();
                            File.WriteAllBytes (folderPath + "/foo" + Guid.NewGuid (), bytes2);
                        }
                    }
                }
                result = true;
            }
            catch (Exception ex) {
                Console.WriteLine (ex.Message);
                result = false;
            }
            return result;
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool Xà (int cnt, Random rnd)
        {
            return cnt <= 10 && this.callNext (cnt, rnd);
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool Xä (int cnt, Random rnd)
        {
            return cnt <= 10 && this.callNext (cnt, rnd);
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool XI (int cnt, Random rnd)
        {
            return cnt <= 10 && this.callNext (cnt, rnd);
        }

        [Obfuscation (Exclude = true, Feature = "renaming")]
        private bool Xl (int cnt, Random rnd)
        {
            return cnt <= 10 && this.callNext (cnt, rnd);
        }

        //
        // Nested Types
        //
        [CompilerGenerated]
        [Serializable]
        private sealed class <>c
        {
            public static readonly MainActivity.<>c <>9 = new MainActivity.<>c ();

            public static Func<MainActivity.z, bool> <>9__10_1;

            public static Func<MainActivity.z, bool> <>9__10_3;

            internal bool <callNext>b__10_1 (MainActivity.z p)
            {
                return p.str.Contains ("foo");
            }

            internal bool <callNext>b__10_3 (MainActivity.z p)
            {
                return p.str.Contains ("bar");
            }
        }

        private class z
        {
            public string str;
        }
    }
}

```

We notice the `"You got it!"` toast message that App will return us when flag will be correct.

```cs
if (this.l (current4.str)) {
    base.RunOnUiThread (delegate {
        Toast.MakeText (this, "You got it!", ToastLength.Long).Show ();
    });
    flag = true;
    break;
}
```
The input string is compared with the flag, but how it's calculated?

These are summarized steps:

1. Save builtin byte array **Key** as file **foo**
2. Save builtin byte array **IV** as file **bar**
3. Read file `"someFile.txt"` and cipher it with Rijndael 256 and the Key/IV read from their files
4. Save the encrypted data as many foo*UUID* files
5. Calculate SHA1 of all files in the *Environment.SpecialFolder.MyDocuments* folder
6. Decrypt builtin byte array **buffer2** using the SHA1s as Key and bar file as IV
7. Compare input text with the result of decryption of buffer2


Looking for foo and bar files inside device, we can find them inside the path `/data/data/dotNetChallenge.dotNetChallenge/files` and then download some foo*UUID* files

```bash
$ adb shell
root@deb:/data/data/dotNetChallenge.dotNetChallenge/files # ls
bar
bar02fae9b1-277a-4d29-8bec-29a96b603d37
[...]
foo
foo28d1b0ec-a9a3-4c89-b89c-e074ba1e82b4
foo45aeba6e-85c6-4a57-9961-1dcc6eca016b
```

```bash
$ adb pull /data/data/dotNetChallenge.dotNetChallenge/files/fooff079944-380a-4cbf-a62d-cd4e7bbc6049
```

Then use files to calculate SHA1 on them

```bash
$ sha1sum fooff079944-380a-4cbf-a62d-cd4e7bbc6049

4b14e05adacc8d763f740e742a4db43e435e34b4  
```

> B64(SHA): SxTgWtrMjXY/dA50Kk20PkNeNLQ=

Now we compose a simple program to rewrite the algorithm with java and bouncycastle library [this](src/main/java/DotNet.java)


```java
public static void main(String[] args) {
  Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());

  String sha64 = "SxTgWtrMjXY/dA50Kk20PkNeNLQ=";
  byte[] k = Base64.getDecoder().decode(sha64);

  System.out.println("Buffer :: "+Base64.getEncoder().encodeToString(buffer)+"  -->  length  "+buffer.length);
  System.out.println("Key(Sha) :: "+Base64.getEncoder().encodeToString(k)+"  -->  length   "+k.length);
  System.out.println("IV :: "+Base64.getEncoder().encodeToString(initVector)+"  -->  length  "+initVector.length);

  System.out.println(decrypt(k, initVector, buffer));

}
```
And executing it

```bash
$  mvn -N io.takari:maven:wrapper
[...]
$ ./mvnw clean package
[INFO] Scanning for projects...
[...]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 1.643 s
[INFO] Finished at: 2017-06-27T00:53:06+02:00
[INFO] Final Memory: 17M/355M
[INFO] ------------------------------------------------------------------------


$ java -jar target/token-generator-0.0.1-SNAPSHOT.jar

Buffer :: Ebm6obwr/eBMGIUJya3/mHGr4aN5sdMSMjLbvqiKYcU=  -->  length  32
Key(Sha) :: SxTgWtrMjXY/dA50Kk20PkNeNLQ=  -->  length   20
IV :: CK0vgsfyFNM/L/6to/Xy6Av0hvkse4ptm616TF19uUI=  -->  length  32
AHE17-d0tn€t-c0de
```

We get the flag

> FLAG: AHE17-d0tn€t-c0de

That's all folks!
