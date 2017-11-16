import java.io.*;

public class MICRunner {

	public static void main(String[] args) {
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader("bill is bad.csv"));
			PrintWriter writer = new PrintWriter(new FileWriter("bill is very bad.csv"));
			String line;
			while ((line = reader.readLine()) != null) {
				String[] input = line.split(",");
				String[] desired = {input[0], input[1]};
				String output = "";
				for (int count = 0; count < desired.length; count++) {
					if (count == 0)
						output = desired[count];
					else
						output = output + "," + desired[count];
				}
				System.out.println(output);
				writer.println(output);
			}
			reader.close();
			writer.close();
		} catch(Exception ex) {
			ex.printStackTrace();
		}
	}
}
