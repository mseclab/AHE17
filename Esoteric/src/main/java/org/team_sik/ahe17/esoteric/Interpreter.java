package org.team_sik.ahe17.esoteric;

//import android.support.v4.internal.view.SupportMenu;
import java.util.Scanner;

public class Interpreter {
	// copied from android.support.v4.internal.view.SupportMenu;
	public static final int USER_MASK = 65535;
	private final int LENGTH = USER_MASK;
	private int dataPointer;
	private byte[] mem = new byte[USER_MASK];
	private Scanner sc = new Scanner(System.in);

	public String interpret(String code) {
		int l = 0;
		StringBuilder sb = new StringBuilder();
		int i = 0;
		while (i < code.length()) {
			if (code.charAt(i) == '>') {
				this.dataPointer = this.dataPointer == 65534 ? 0 : this.dataPointer + 1;
			} else if (code.charAt(i) == '<') {
				this.dataPointer = this.dataPointer == 0 ? 65534 : this.dataPointer - 1;
			} else if (code.charAt(i) == '+') {
				byte[] r3 = this.mem;
				int r6 = this.dataPointer;
				r3[r6] = (byte) (r3[r6] + 1);
			} else if (code.charAt(i) == '-') {
				byte[] r3 = this.mem;
				int r6 = this.dataPointer;
				r3[r6] = (byte) (r3[r6] - 1);
			} else if (code.charAt(i) == '.') {
				sb.append((char) this.mem[this.dataPointer]);
			} else if (code.charAt(i) == ',') {
				this.mem[this.dataPointer] = (byte) this.sc.next().charAt(0);
			} else if (code.charAt(i) == '[') {
				if (this.mem[this.dataPointer] == (byte) 0) {
					i++;
					while (true) {
						if (l <= 0 && code.charAt(i) == ']') {
							break;
						}
						if (code.charAt(i) == '[') {
							l++;
						}
						if (code.charAt(i) == ']') {
							l--;
						}
						i++;
					}
				}
			} else if (code.charAt(i) == ']' && this.mem[this.dataPointer] != (byte) 0) {
				i--;
				while (true) {
					if (l <= 0 && code.charAt(i) == '[') {
						break;
					}
					if (code.charAt(i) == ']') {
						l++;
					}
					if (code.charAt(i) == '[') {
						l--;
					}
					i--;
				}
				i--;
			}
			i++;
		}
		return sb.toString();
	}

	public static void main(String[] args) {
		String deadCode = "-[--->+<]>-.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->+++<]>+.+.----.+++.-[--->+<]>-.+[->+++<]>.++++++++++++.-----------.+.-[->+++<]>.------------.+[->+++<]>+.--[--->+<]>-.+[->+++<]>++.+.[->+++<]>-.++[--->++<]>.++++[->++<]>+.[----->+<]>-.-.+[---->+<]>+++.+++++[->+++<]>.-------------.[--->+<]>.[------>+<]>.++++++.++++++.--.-[++>---<]>+.------------.-[--->++<]>-.++++++++++.-----.[++>---<]>++.[->+++<]>-.[---->+<]>+++.-[--->++<]>-.+++++++++++.-[->+++++<]>.";
		System.out.println("Dead Code\r\n"+new Interpreter().interpret(deadCode.replaceAll("-\\+", "\\.")));

		String hw = "-[------->+<]>-.-[->+++++<]>++.+++++++..+++.[--->+<]>-----.---[->+++<]>.-[--->+<]>---.+++.------.--------.[->+++<]>++...--[-->+++<]>--++++++++-+----+[--->++<]>+++-+++++++-+[--->++<]>+-+[->+++<]>---++-+------------++++++++++-++[------->+<]>-+[->+++++++<]>-+++++++-+----++[----->+++<]>-+>----[-->+++<]>--+--[->+++<]>-+[--->+<]>-----+>-[----->+<]>--+>-[--->+<]>---+[----->+++<]>-+-+>--[-->+++<]>-++[--->++<]>.[---->+++++<]>-.+.++++++++++.+[---->+<]>+++.-[--->++<]>-.++++++++++.+[---->+<]>+++.+[->++<]>.---[----->+<]>-.+++[->+++<]>++.++++++++.+++++.--------.-[--->+<]>--.+[->+++<]>+.++++++++.+[++>---<]>-.";
		System.out.println("Hello World\r\n"+new Interpreter().interpret(hw.replaceAll("-\\+", "\\.")));
	}
}