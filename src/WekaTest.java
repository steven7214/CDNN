import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Random;

import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.evaluation.Prediction;
import weka.classifiers.functions.Logistic;
import weka.core.Instances;

public class WekaTest {

	public static void main(String[] args) throws Exception {
		BufferedReader reader = null;
		reader = new BufferedReader(new FileReader("Data/CancerSEEK/protein.arff"));
		Instances data = new Instances(reader);
		data.setClassIndex(data.numAttributes() - 1);
		reader.close();
		
		NaiveBayes nb = new NaiveBayes();
		nb.buildClassifier(data);
		Logistic lg = new Logistic();
		lg.buildClassifier(data);
		Evaluation eval = new Evaluation(data);
		
		eval.crossValidateModel(lg, data, 10, new Random(1));
		
		System.out.println(eval.toSummaryString("results", true));
		System.out.println(eval.fMeasure(1) + " " + eval.precision(1) + " " + eval.recall(1));
		for (int i = 0; i < data.numInstances(); i++) {
			double label = lg.classifyInstance(data.instance(i));
		//	System.out.println(label);
		}
		ArrayList<Prediction> predictions = eval.predictions();
		System.out.println(predictions.get(6).toString());
		double num = 0;
		for (int count = 0; count < predictions.size(); count++) {
			Prediction prediction = predictions.get(count);
			String update = prediction.toString();
			if (update.substring(5,8).equals(update.substring(9,12)))
					num++;	
		}
		System.out.println(num/predictions.size()*100);
	}
}