import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Random;

import weka.classifiers.Evaluation;
import weka.classifiers.bayes.NaiveBayes;
import weka.core.Instances;
import weka.classifiers.functions.*;

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
		System.out.println(eval.predictions().get(0));
	}

}
