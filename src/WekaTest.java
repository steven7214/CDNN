import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Random;

import weka.classifiers.Evaluation;
import weka.classifiers.evaluation.Prediction;
import weka.classifiers.functions.Logistic;
import weka.core.Instances;

public class WekaTest {

	public static void main(String[] args) throws Exception {
		BufferedReader reader = null;
		reader = new BufferedReader(new FileReader("Data/CancerSEEK/protein (normal).arff"));
		Instances data = new Instances(reader);
		data.setClassIndex(data.numAttributes() - 1);
		reader.close();
		
	
		Logistic lg = new Logistic();
		lg.buildClassifier(data);
		Evaluation eval = new Evaluation(data);
		
		eval.crossValidateModel(lg, data, 10, new Random(1));
		
		System.out.println(eval.toSummaryString("results", true));
		System.out.println(eval.fMeasure(1) + " " + eval.precision(1) + " " + eval.recall(1));
		BufferedWriter writer = new BufferedWriter(new FileWriter("Data/CancerSEEK/test.txt"));
		for (int i = 0; i < data.numInstances(); i++) {
			double label = lg.classifyInstance(data.instance(i));
			writer.write(label + "\n");
		}
		writer.close();
		ArrayList<Prediction> predictions = eval.predictions();
		writer = new BufferedWriter(new FileWriter("Data/CancerSEEK/results.txt"));
		double num = 0;
		for (int count = 0; count < predictions.size(); count++) {
			Prediction prediction = predictions.get(count);
			writer.write(prediction + "\n");
			String update = prediction.toString();
			if (update.substring(5,8).equals(update.substring(9,12)))
					num++;	
		}
		writer.close();
		System.out.println(num/predictions.size()*100);
	}
}