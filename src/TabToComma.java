
		import java.io.*;

		public class TabToComma {
			
			public static void main(String[] args) {
				try {
					BufferedReader reader = new BufferedReader(new FileReader("Data/Mutation Log/TCGA-BI-A0VR-01.hg19.oncotator.hugo_entrez_remapped.maf.txt"));
					PrintWriter writer = new PrintWriter(new FileWriter("Data/Mutation.csv"));
					
					String line;
					while ((line = reader.readLine()) != null) {
						String[] words = line.split("	");
						String output = "";
						for (int count = 0; count < words.length; count++) {
							if (count == 0)
								output = words[count];
							else
								output = output + "," + words[count];
						}
						writer.println(output);
					}
				} catch(Exception ex) {
					ex.printStackTrace();
				}
				System.out.println("successful");

			}
		}


	

