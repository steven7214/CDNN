import java.io.*;
import java.util.*;

public class GeneTester {

	public static void main(String[] args) {
		HashMap<String, double[]> geneList = new HashMap<String, double[]>();
		File folder = new File("Data/Glioma Raw/Mutation Annotation Raw");
		File[] listOfFiles = folder.listFiles();
		ArrayList<String> patientNames = new ArrayList<String>();
		String line;
		boolean isDead;
		for (int count = 0; count < listOfFiles.length; count++) {
			patientNames.add(listOfFiles[count].getName().substring(0, 12).toUpperCase());
		}
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Data/Glioma Raw/Clinical.txt"));
			BufferedReader reader2;		
			reader.readLine();
			while((line = reader.readLine()) != null) {
				if(patientNames.contains(line.split("	")[0].toUpperCase())) {
					if("dead".equalsIgnoreCase(line.split("	")[3]))
						isDead = true;
					else
						isDead = false;
					reader2 = new BufferedReader(
							new FileReader(listOfFiles[patientNames.indexOf(line.split("	")[0].toUpperCase())]));
					reader2.readLine();
					while((line = reader2.readLine()) != null) {
						if(geneList.containsKey(line.split("	")[0] + "\t" + line.split("	")[8])) {
							double[] value = geneList.get(line.split("	")[0] + "\t" + line.split("	")[8]);
							if(isDead) 
								value[0]++;
							else
								value[1]++;
						} else {
							double[] value = {0.0,0.0};
							if(isDead) 
								value[0]++;
							else
								value[1]++;
							geneList.put(line.split("	")[0] + "\t" + line.split("	")[8], value);
						}
					}
				}	
			}
			System.out.println(geneList.size());
			reader.close();
			PrintWriter writer = new PrintWriter(new FileWriter("output/Gene vs Vitality.txt"));
			writer.println("gene" + "\t" + "Mutation Type" + "\t" + "dead" + "\t" + "alive" + "\t" + "percentage");
			for (String key: geneList.keySet()) {
				double dead = geneList.get(key)[0];
				double alive = geneList.get(key)[1];
				if (alive + dead < 5)
					continue;
				writer.println(key + "\t" + dead + "\t" + alive + "\t" + dead/(dead+alive)*100);
					//writer.println(key + ": " + "\t" + "alive= " + alive + "\t" + " dead= " + dead + "\t" + " percentage= " + alive/(dead+alive)*100 + "%");
			}
			writer.flush();
			writer.close();
			
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

}
