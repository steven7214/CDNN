import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;

public class MICRunner {

	public static void main(String[] args) {
		ArrayList<String> field = new ArrayList<String>();
		ArrayList<String[]> dataFile1 = new ArrayList<String[]>();
		ArrayList<String[]> dataFile2 = new ArrayList<String[]>();
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Data/wantedColumns.txt"));
			PrintWriter writer = new PrintWriter(new FileWriter("output/MIC_Ready.csv"));
			String[] data1 = reader.readLine().split(",");
			String[] data2 = reader.readLine().split(",");
			reader.close();
			reader = new BufferedReader(new FileReader("Data/cleanedData.csv"));
			String line;
			while ((line=reader.readLine()) != null) {
				dataFile1.add(line.split(","));
			}
			for (int count = 0; count < data1.length; count++) {
				field.add(dataFile1.get(Integer.parseInt(data1[count]) -1)[0]);
				String output = "";
				for (int value = 0; value < dataFile1.get(Integer.parseInt(data1[count])-1).length; value++) {
					if (value == 0)
						output = dataFile1.get(Integer.parseInt(data1[count])-1)[value];
					else
						output = output + "," + dataFile1.get(Integer.parseInt(data1[count])-1)[value];
				}
				writer.println(output);
			}
			reader.close();
			reader = new BufferedReader(new FileReader("Data/cleanedData2.csv"));
			while ((line=reader.readLine()) != null) {
				dataFile2.add(line.split(","));
			}
			
			for (int count = 0; count < data2.length; count++) {
				boolean checked = false;

				for (String check: field) {
					if (dataFile2.get(Integer.parseInt(data2[count])-1)[0].contentEquals(check)) {
						checked = true;
					}
						
				}
				if (checked) 
					continue;
				
				System.out.println(dataFile2.get(Integer.parseInt(data2[count])-1)[0]);

				field.add(dataFile2.get(Integer.parseInt(data2[count]) -1)[0]);
				String output = "";
				for (int value = 0; value < dataFile2.get(Integer.parseInt(data2[count])-1).length; value++) {
					if (value == 0)
						output = dataFile2.get(Integer.parseInt(data2[count])-1)[value];
					else
						output = output + "," + dataFile2.get(Integer.parseInt(data2[count])-1)[value];
				}
				writer.println(output);
			}
			reader.close();
			
			writer.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
}
