/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package javaconsume;

import com.bitmechanic.barrister.HttpTransport;
import java.util.Arrays;

/**
 *
 * @author william
 */
public class JavaConsume {
    public static void main(String argv[]) throws Exception {
        HttpTransport trans = new HttpTransport("http://localhost:7667/Alpha");
        AlphaClient lista = new AlphaClient(trans);

        System.out.println(lista.Alpha("WILLIAM "));
        System.out.println(lista.Alpha("FERNANDO "));

        System.out.println("\nIDL metadata:");

        // BarristerMeta is a Idl2Java generated class in the same package
        // as the other generated files for this IDL
        System.out.println("barrister_version=" + BarristerMeta.BARRISTER_VERSION);
        System.out.println("checksum=" + BarristerMeta.CHECKSUM);
    }
}
