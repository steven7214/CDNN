import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;

public class CSVRuner {
	public static void main(String[] args) {
		String name = "/output/hi.txt";		
		String csvName = TabToComma.reWrite(name);
		try {
			BufferedReader reader = new BufferedReader(new FileReader(csvName));
			
		} catch(Exception ex) {
			ex.printStackTrace();
		}
	}
}
