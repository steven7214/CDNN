import java.io.*;

public class Normalize {

	public static void main(String[] args) throws Exception{
		BufferedReader reader = new BufferedReader(new FileReader("Data/CancerSeek/Only Numbers (normal).csv"));
		double[][] nums = new double[1817][40];
		double[][] bill = new double[39][2];
		for (int count = 0; count < nums.length; count++) {
			String[] line= reader.readLine().split(",");
			for (int value = 0; value < 40; value++) {
				nums[count][value] = Double.parseDouble(line[value]);
			}
		}
		reader.readLine();
		for (int value = 0; value < 39; value++) {
			double max = Integer.MIN_VALUE;
			double min = Integer.MAX_VALUE;
			for (int count = 0; count < nums.length; count++) {
				max = Math.max(max, nums[count][value]);
				min = Math.min(min, nums[count][value]);
			}
			bill[value][0] = max;
			bill[value][1] = min;
		}
		
		for (int value = 0; value < 39; value++) {
			for (int count = 0; count < nums.length; count++) {
				nums[count][value] -= bill[value][1];
				nums[count][value] /= bill[value][0] - bill[value][1];
				System.out.println(nums[count][value]);
			}
		}
		
		BufferedWriter writer = new BufferedWriter(new FileWriter("Data/CancerSeek/Bill is bad.csv"));
		for (int count = 0; count < nums.length; count++) {
			for (int value = 0; value < 39; value++) {
				writer.write(nums[count][value] + ",");
			}
			writer.write(nums[count][39] + "\n");
		}
		writer.close();
	}

}
