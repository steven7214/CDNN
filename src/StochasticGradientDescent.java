import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;

public class StochasticGradientDescent {

	public static double dotproduct(double[] x, double[] y) {
		double product = 0.0;
		if (x.length != y.length) {
			System.out.println("lengths don't match for dot product"); // arrays
																		// must
																		// be
																		// same
																		// length
			return product;
		}
		for (int count = 0; count < x.length; count++)
			product += x[count] * y[count];
		return product;
	}

	public static void main(String[] args) {
		ArrayList<double[]> inputs = new ArrayList<double[]>();
		ArrayList<Double> outputs = new ArrayList<Double>();
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Data/Bike-Sharing-Dataset/hour.csv"));
			// put in path of the data in previous line
			String line;
			reader.readLine(); // first line doesn't contain real data
			while ((line = reader.readLine()) != null) {
				String[] temp = line.split(",");
				double[] transfer = new double[temp.length - 3]; // remove
																	// index(first),
																	// date(second)
				// attribute
				// and output
				transfer[0] = 1;
				for (int count = 2; count < transfer.length - 1; count++) {
					// transfer[count] = Double
					// .parseDouble(temp[count + 1].substring(1, temp[count +
					// 1].length() - 1).trim());
					transfer[count - 1] = Double.parseDouble(temp[count]);
					// removes the first and last quotes from each attribute
				}
				// outputs.add(Double.parseDouble(temp[1].substring(1,
				// temp[1].length() - 1).trim()));
				outputs.add(Double.parseDouble(temp[temp.length - 1]));
				inputs.add(transfer);
			}
		} catch (Exception ex) {
			ex.printStackTrace();
		}

		double[] weights = new double[inputs.get(0).length];
		double[] temp = new double[weights.length];
		double stop = 100.0;
		while (stop > 1) {
			for (int i = 0; i < inputs.size(); i++) {
				stop = 0.0;
				int draw = (int) (Math.random() * inputs.size());
				for (int value = 0; value < weights.length; value++) {
					temp[value] = weights[value] - 0.001
							* (StochasticGradientDescent.dotproduct(weights, inputs.get(draw)) - outputs.get(draw))
							* inputs.get(draw)[value];
				}

				for (int test = 0; test < weights.length; test++)
					stop += Math.abs(weights[test] - temp[test]);
				weights = temp;
				temp = new double[weights.length]; // java is pass by
													// reference
													// not
													// pass by value
			}
			System.out.println(stop);

		}

		double sum = 0.0;
		for (int count = 0; count < inputs.size(); count++) {
			sum += Math.pow(StochasticGradientDescent.dotproduct(weights, inputs.get(count)) - outputs.get(count), 2);
		}
		for (double test : weights)
			System.out.println("weights= " + test);
		System.out.println("average error= " + (sum * 0.5) / inputs.size());

		try {
			FileWriter writer = new FileWriter("test.txt");
			for (int count = 0; count < inputs.size(); count++)
				writer.write(
						(StochasticGradientDescent.dotproduct(weights, inputs.get(count)) - outputs.get(count)) + "\n");
		} catch (Exception ex) {
			ex.printStackTrace();
		}

	}
}
