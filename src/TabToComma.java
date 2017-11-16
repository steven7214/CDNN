
		import java.io.*;

		public class TabToComma {
			
			public static void main(String[] args) {
				try {
					BufferedReader reader = new BufferedReader(new FileReader("Data/gdac.broadinstitute.org_CESC.Clinical_Pick_Tier1.Level_4.2016012800.0.0/All_CDEs.txt"));
					PrintWriter writer = new PrintWriter(new FileWriter("cleanedData.csv"));
					
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
						System.out.println("successful");
					}
				} catch(Exception ex) {
					ex.printStackTrace();
				}
				System.out.println("what");

			}
		}


	

