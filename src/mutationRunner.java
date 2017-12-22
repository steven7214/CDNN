import java.io.BufferedReader;
import java.io.FileReader;
import java.util.HashMap;
//import org.apache.commons.math3.distribution.*;

public class mutationRunner {
	public static void main(String args[]) {
		//AbstractRealDistribution distributor = new NormalDistribution();
		HashMap<String, Integer> genes = new HashMap<String, Integer>();
		double backgroundRate = 0.02;
		int patientNum = 0;
		String name = "";
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Data/CARC.maf"));
			reader.readLine();
			String line;
			while ((line = reader.readLine()) != null) {
				String[] input = line.split("	");
				if (genes.containsKey(input[2]) == false)
					genes.put(input[2], 1);
				else
					genes.put(input[2], genes.get(input[2]) + 1);
				if (name.equals(input[1]) == false) {
					patientNum++;
					name = input[1];
				}
			}
			reader.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
		// System.out.println(genes.keySet().size());
		// System.out.println("patients= " + patientNum);

		int num = 0;
		for (String key : genes.keySet()) {
			double z_score = (((double) genes.get(key) / patientNum) - backgroundRate)
					/ (Math.sqrt(backgroundRate * (1 - backgroundRate) / patientNum));
			//if (distributor.cumulativeProbability(-Math.abs(z_score)) < 0.01) {
				//System.out.println(key);
				//num++;
			//}
		}
		//System.out.println(num);
	}

}
