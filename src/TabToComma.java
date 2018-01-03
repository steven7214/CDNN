
		import java.io.*;

		public class TabToComma {
			
			public static String reWrite(String input) {
				int end = 0;
				int start = 0;
				for (int count = 0; count < input.length(); count++) {
					if (input.substring(count, count+1).equals("."))
						end = count;
					else if (input.substring(count, count+1).equals("/"))
						start = count+1;
				}
				
				String file = "/Data/" + input.substring(start,end) + ".csv";
				System.out.println(file);
			try {
					BufferedReader reader = new BufferedReader(new FileReader(input));
					PrintWriter writer = new PrintWriter(new FileWriter(file));
					
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
				return file;
			}
			
		/*	public static void main(String[] args) {
				
				System.out.println("successful");

			} */
		}


	

