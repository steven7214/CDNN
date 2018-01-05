import java.io.*;
import java.util.*;

public class SynergyTester {

	public static ArrayList<Double> compareGenes(String combinationName, double[] vital,
		HashMap<String, double[]> genes) {
		ArrayList<Double> analysis = new ArrayList<Double>();
		String[] geneNames = combinationName.split("\t"); // gets individual genes from combinationName
		for (String geneName : geneNames) {
			genes.get(geneName)[0] -= vital[0]; // subtracts vital status of those in the combination
			genes.get(geneName)[1] -= vital[1];
		}

		double percentage1 = genes.get(geneNames[0])[0] / (genes.get(geneNames[0])[0] + genes.get(geneNames[0])[1]); // finds
																														// individual
																														// percentages
		double percentage2 = genes.get(geneNames[1])[0] / (genes.get(geneNames[1])[0] + genes.get(geneNames[1])[1]);
		double combinationPercentage = vital[0] / (vital[0] + vital[1]); // finds combined percentage
		if (combinationPercentage > percentage1 && combinationPercentage > percentage2) { // comparison analysis
			analysis.add(combinationPercentage - percentage1);
			analysis.add(combinationPercentage - percentage2);
		} else if (combinationPercentage > percentage1 || combinationPercentage > percentage2)
			analysis.add(combinationPercentage - (percentage1 + percentage2) / 2);

		return analysis;
	}

	public static void main(String[] args) {
		HashMap<String, double[]> combinations = new HashMap<String, double[]>();
		HashMap<String, double[]> genes = new HashMap<String, double[]>();
		File folder = new File("Data/Glioma Raw/Mutation Annotation Raw");
		// File folder = new File("Data/Test");
		File[] listOfFiles = folder.listFiles();
		ArrayList<Person> people = new ArrayList<Person>();
		ArrayList<String> patientNames = new ArrayList<String>();
		String line;
		for (int count = 0; count < listOfFiles.length; count++) {
			if (listOfFiles[count].getName().equalsIgnoreCase(".DS_Store"))
				continue;
			patientNames.add(listOfFiles[count].getName().substring(0, 12).toLowerCase()); // adds all names from
																							// mutations files
		}
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Data/Glioma Raw/Clinical.txt"));
			BufferedReader reader2;
			reader.readLine();
			while ((line = reader.readLine()) != null) {
				if (patientNames.contains(line.split("	")[0])) {
					people.add(new Person(line.split("\t")[0])); // adds Person with that name to people list
					if ("dead".equalsIgnoreCase(line.split("	")[3])) // adds death status to most recently created
																		// person in arraylist
						people.get(people.size() - 1).setDeathStatus(true);
					else
						people.get(people.size() - 1).setDeathStatus(false);
					reader2 = new BufferedReader(
							new FileReader(listOfFiles[patientNames.indexOf(line.split("	")[0])])); // reads in the
																										// annotation
																										// files for
																										// each person
					reader2.readLine();
					while ((line = reader2.readLine()) != null) {
						String[] input = { line.split("\t")[0], line.split("\t")[8] };
						people.get(people.size() - 1).addMutation(input); // adds all mutations to each person
					}
					reader2.close();
				}
			}
			reader.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}

		for (Person person : people) {
			ArrayList<String[]> personCombos = person.getCombinations(); // adds all combinations of two genes and their
			ArrayList<String[]> personGenes = person.getMutations(); // add all vital rates of individual genes
			for (String[] personGene : personGenes) {
				if (genes.containsKey(personGene[0])) {
					double[] value = genes.get(personGene[0]);
					if (person.death)
						value[0]++;
					else
						value[1]++;
				} else {
					double[] value = { 0.0, 0.0 };
					if (person.death)
						value[0]++;
					else
						value[1]++;
					genes.put(personGene[0], value);
				}
			}

			for (String[] personCombo : personCombos) {
				String key = personCombo[0] + "\t" + personCombo[2];

				if (combinations.containsKey(key)) {
					double[] value = combinations.get(key);
					if (person.death)
						value[0]++;
					else
						value[1]++;
				} else {
					double[] value = { 0.0, 0.0 };
					if (person.death)
						value[0]++;
					else
						value[1]++;
					combinations.put(personCombo[0] + "\t" + personCombo[2], value);
				}
			}
		}
		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter("output/SynergyTest.txt"));
			int count = 0;
			for (String currentKey : combinations.keySet()) {
				ArrayList<Double> output = SynergyTester.compareGenes(currentKey, combinations.get(currentKey),
						genes);
				if (output.size() == 0)
					continue;
				String lineToWrite = currentKey + "\t" + output.get(0);
				if (output.size() == 2)
					lineToWrite += "\t" + output.get(1);
				writer.write(lineToWrite + "\n");
					if (count > 100000) {
					writer.flush();
					count = 0;
				} else {
					count++;
				}
				}
			writer.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
		System.out.println("Done");
	}
}