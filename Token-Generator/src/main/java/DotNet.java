import java.security.Security;
import java.util.Base64;

import org.bouncycastle.crypto.BlockCipher;
import org.bouncycastle.crypto.BufferedBlockCipher;
import org.bouncycastle.crypto.engines.RijndaelEngine;
import org.bouncycastle.crypto.modes.CBCBlockCipher;
import org.bouncycastle.crypto.paddings.PKCS7Padding;
import org.bouncycastle.crypto.paddings.PaddedBufferedBlockCipher;
import org.bouncycastle.crypto.params.KeyParameter;
import org.bouncycastle.crypto.params.ParametersWithIV;

public class DotNet {

	static byte[] buffer = new byte[] {
             (byte)17,
             (byte)185,
             (byte)186,
             (byte)161,
             (byte)188,
             (byte)43,
             (byte)253,
             (byte)224,
             (byte)76,
             (byte)24,
             (byte)133,
             (byte)9,
             (byte)201,
             (byte)173,
             (byte)255,
             (byte)152,
             (byte)113,
             (byte)171,
             (byte)225,
             (byte)163,
             (byte)121,
             (byte)177,
             (byte)211,
             (byte)18,
             (byte)50,
             (byte)50,
             (byte)219,
             (byte)190,
             (byte)168,
             (byte)138,
             (byte)97,
             (byte)197
         };

	
	static byte[] initVector = new byte[] {
			(byte)                8,
			(byte)                173,
			(byte)                47,
			(byte)                130,
			(byte)                199,
			(byte)                242,
			(byte)                20,
			(byte)                211,
			(byte)                63,
			(byte)                47,
			(byte)                254,
			(byte)                173,
			(byte)                163,
			(byte)                245,
			(byte)                242,
			(byte)                232,
			(byte)                11,
			(byte)                244,
			(byte)                134,
			(byte)                249,
			(byte)                44,
			(byte)                123,
			(byte)                138,
			(byte)                109,
			(byte)                155,
			(byte)                173,
			(byte)                122,
			(byte)                76,
			(byte)                93,
			(byte)                125,
			(byte)                185,
			(byte)                66
	};
	

    public static String decrypt(byte[] key, byte[] initVector, byte[] encrypted) {
        try {
        	
        	BlockCipher engine = new RijndaelEngine(256);
            CBCBlockCipher cbc = new CBCBlockCipher(engine);
            BufferedBlockCipher cipher = new PaddedBufferedBlockCipher(cbc, new PKCS7Padding());
            
            cipher.init(false, new ParametersWithIV(new KeyParameter(key), initVector));

            int minSize = cipher.getOutputSize(encrypted.length);
            byte[] outBuf = new byte[minSize];
            int length1 = cipher.processBytes(encrypted, 0, encrypted.length, outBuf, 0);
            int length2 = cipher.doFinal(outBuf, length1);
            int actualLength = length1 + length2;
            byte[] result = new byte[actualLength];
            System.arraycopy(outBuf, 0, result, 0, result.length);


            return new String(result);
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        return null;
    }
    
    public static void main(String[] args) {
    	Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
    	
    	String sha64 = "SxTgWtrMjXY/dA50Kk20PkNeNLQ=";
    	byte[] k = Base64.getDecoder().decode(sha64);
    	
    	System.out.println("Buffer :: "+Base64.getEncoder().encodeToString(buffer)+"  -->  length  "+buffer.length);
    	System.out.println("Key(Sha) :: "+Base64.getEncoder().encodeToString(k)+"  -->  length   "+k.length);
    	System.out.println("IV :: "+Base64.getEncoder().encodeToString(initVector)+"  -->  length  "+initVector.length);
    	
    	System.out.println(decrypt(k, initVector, buffer));
    	
    }
}

