# AHE17 : Android Hacking Events 2017

## **Esoteric** ([Esoteric.apk](https://team-sik.org/wp-content/uploads/2017/06/esoteric.apk_.zip) - India in the Dashboard)

**Hint**

So much Brainfuck... seems like there is more than you see! Please take a look at me!

## Write-up

by [svetrini](https://github.com/ningod)

After installing the Esoteric.apk on your device or emulator you can see a *stange* string composed by points, lines and brackets; pushing the *Evaluate* button you obtain the message

> *Hello World...This is Brainfuck*

This is an other hint together with apk title, infact the application is a simple interpreter for the [Brainfuck](https://it.wikipedia.org/wiki/Brainfuck) esoteric language.

### Static Analysis

Let's see inside  `Esoteric.apk` with a decompiler like [jadx or with jadx-gui](https://github.com/skylot/jadx)

```bash
$ jadx -d Esoteric.jadx Esoteric.apk
[...]

$ tree Esoteric.jadx/org
Esoteric.jadx/org
└── team_sik
    └── ahe17
        └── esoteric
            ├── BuildConfig.java
            ├── Interpreter.java
            ├── R.java
            └── SuperActivity.java

3 directories, 4 files

```

We can see `SuperActivity` that is the app main activity that draw the UI with the brainfuck text and the evaluate button, and uses the `Interpreter` class to evalate the brainfuck code.

```java
public class SuperActivity extends AppCompatActivity {
    EditText input;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) R.layout.activity_super);
        ((Button) findViewById(R.id.evalbutton)).requestFocus();
        this.input = (EditText) findViewById(R.id.textarea);
        this.input.setText("-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.[->+++<]>++...--[-->+++<]>--++++++++-+----+[--->++<]>+++-+++++++-+[--->++<]>+-+[->+++<]>---++-+------------++++++++++-++[------->+<]>-+[->+++++++<]>-+++++++-+----++[----->+++<]>-+>----[-->+++<]>--+--[->+++<]>-+[--->+<]>-----+>-[----->+<]>--+>-[--->+<]>---+[----->+++<]>-+-+>--[-->+++<]>-++[--->++<]>.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->++<]>.---[----->+<]>-.+++[->+++<]>++.++++++++.+++++.--------.-[--->+<]>--.+[->+++<]>+.++++++++.+[++>---<]>-.");
    }

    public void evaluate(View v) {
        Toast.makeText(this, new Interpreter().interpret(this.input.getText().toString()), 0).show();
    }
}
```

Looking inside the Interpreter code we can see an interpret method that is a only a brainfuck interpret and strange ( for Android ) java main method with an hard coded string in brainfuck

```java

public String interpret(String code) [...]

public static void main(String[] args) {
    System.out.println(new Interpreter().interpret("-[--->+<]>-.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->+++<]>+.+.----.+++.-[--->+<]>-.+[->+++<]>.++++++++++++.-----------.+.-[->+++<]>.------------.+[->+++<]>+.--[--->+<]>-.+[->+++<]>++.+.[->+++<]>-.++[--->++<]>.++++[->++<]>+.[----->+<]>-.-.+[---->+<]>+++.+++++[->+++<]>.-------------.[--->+<]>.[------>+<]>.++++++.++++++.--.-[++>---<]>+.------------.-[--->++<]>-.++++++++++.-----.[++>---<]>++.[->+++<]>-.[---->+<]>+++.-[--->++<]>-.+++++++++++.-[->+++++<]>."));
}
```
Exporting the class with main in a simple maven java project we can execute the method and the output is not a flag but another hint

> *This is dead code, dude. Its obvious, isn't it?*

All the applicationj is a simple puzzle, there is *ONLY* an interpreter no hidden code in java or other languages and some hints, and the more interesting are the parts:

* *more than you see*
* *dead code*

The solution is hidden inside the hello world code where there is *more than you see* inside a *dead code* block.
To find the dead code we revise brainfuck's commands:

* **\>**	increment the data pointer (to point to the next cell to the right).
* **<**	decrement the data pointer (to point to the next cell to the left).
* **\+**	increment (increase by one) the byte at the data pointer.
* **\-**	decrement (decrease by one) the byte at the data pointer.
* **.**	output the byte at the data pointer.
* **,**	accept one byte of input, storing its value in the byte at the data pointer.

For a simple hello world program dead code may be a block that doesn't do output like this


-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.[->+++<]>++...**--[-->+++<]>--++++++++-+----+[--->++<]>+++-+++++++-+[--->++<]>+-+[->+++<]>---++-+------------++++++++++-++[------->+<]>-+[->+++++++<]>-+++++++-+----++[----->+++<]>-+>----[-->+++<]>--+--[->+++<]>-+[--->+<]>-----+>-[----->+<]>--+>-[--->+<]>---+[----->+++<]>-+-+>--[-->+++<]>-++[--->++<]>**.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->++<]>.---[----->+<]>-.+++[->+++<]>++.++++++++.+++++.--------.-[--->+<]>--.+[->+++<]>+.++++++++.+[++>---<]>-.

or some instructions that does *nothing* like decrement/increment data sequentially:

-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.[->+++<]>++...--[-->+++<]>-**-+**+++++++**-+**---**-+**[--->++<]>+++**-+**++++++**-+**[--->++<]>+**-+**[->+++<]>--**-+**+**-+**-----------**-+**+++++++++**-+**+[------->+<]>**-+**[->+++++++<]>**-+**++++++**-+**---**-+**+[----->+++<]>**-+**>----[-->+++<]>-**-+**--[->+++<]>**-+**[--->+<]>----**-+**>-[----->+<]>-**-+**>-[--->+<]>--**-+**[----->+++<]>**-+-+**>--[-->+++<]>**-+**+[--->++<]>.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->++<]>.---[----->+<]>-.+++[->+++<]>++.++++++++.+++++.--------.-[--->+<]>--.+[->+++<]>+.++++++++.+[++>---<]>-.

If we execute a modified main method to execute a string replace on on the hello world string removing the decrement/increment sequences *-+* and those with an output char *.* we obtain the flags

```java

public static void main(String[] args) {
  String deadCode = "-[--->+<]>-.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->+++<]>+.+.----.+++.-[--->+<]>-.+[->+++<]>.++++++++++++.-----------.+.-[->+++<]>.------------.+[->+++<]>+.--[--->+<]>-.+[->+++<]>++.+.[->+++<]>-.++[--->++<]>.++++[->++<]>+.[----->+<]>-.-.+[---->+<]>+++.+++++[->+++<]>.-------------.[--->+<]>.[------>+<]>.++++++.++++++.--.-[++>---<]>+.------------.-[--->++<]>-.++++++++++.-----.[++>---<]>++.[->+++<]>-.[---->+<]>+++.-[--->++<]>-.+++++++++++.-[->+++++<]>.";
  System.out.println("Dead Code\r\n"+new Interpreter().interpret(deadCode.replaceAll("-\\+", "\\.")));

  String hw = "-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.[->+++<]>++...--[-->+++<]>--++++++++-+----+[--->++<]>+++-+++++++-+[--->++<]>+-+[->+++<]>---++-+------------++++++++++-++[------->+<]>-+[->+++++++<]>-+++++++-+----++[----->+++<]>-+>----[-->+++<]>--+--[->+++<]>-+[--->+<]>-----+>-[----->+<]>--+>-[--->+<]>---+[----->+++<]>-+-+>--[-->+++<]>-++[--->++<]>.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->++<]>.---[----->+<]>-.+++[->+++<]>++.++++++++.+++++.--------.-[--->+<]>--.+[->+++<]>+.++++++++.+[++>---<]>-.";
  System.out.println("Hello World\r\n"+new Interpreter().interpret(hw.replaceAll("-\\+", "\\.")));
}

```

```bash
$  mvn -N io.takari:maven:wrapper
[...]
$ ./mvnw clean package
[INFO] Scanning for projects...
[...]
------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 0.959 s
[INFO] Finished at: 2017-06-19T11:30:48+02:00
[INFO] Final Memory: 14M/207M
[INFO] ------------------------------------------------------------------------

$ java -jar target/esoteric-0.0.1-SNAPSHOT.jar
Dead Code
This is dead code, dude. Its obvious, isn't it?
Hello World
Hello World...AHE17{openYourEyes2See}This is Brainfuck!
```

>  FLAG: AHE17{openYourEyes2See}

That's all folks!
