import java.util.ArrayList;
import java.util.Comparator;

public class Person {
	public String id;
	public boolean death;
	private ArrayList<String[]> mutations;
	private ArrayList<String[]> combinations;
	
	public Person(String name) {
		id = name;
		mutations = new ArrayList<String[]>();
		combinations = new ArrayList<String[]>();
	}
	
	public void setDeathStatus(boolean isDead) {
		death = isDead;
	}
	
	public void addMutation(String[] mutation) {
		for (String[] mut: mutations) {
			if (mut[0].equals(mutation[0])) {
				//System.out.println(mutation[0]+mutation[1]);
				return;
			}
		}
		mutations.add(mutation);
	}
	
	public ArrayList<String[]> getMutations() {
		return mutations;
	}
	
	public ArrayList<String[]> getCombinations() { //gets all subsets of 2 genes from whole mutation list
		mutations.sort(mutationComparator);
		for (int count = 0; count < mutations.size()-1; count++) {
			for (int value = count+1; value < mutations.size(); value++) {
				String[] input = {mutations.get(count)[0], mutations.get(count)[1], mutations.get(value)[0], mutations.get(value)[1]}; //
				combinations.add(input);
			}
				
		}	
		return combinations;
	}
	
	public static Comparator<String[]> mutationComparator = new Comparator<String[]>() {
		public int compare(String[] a, String[] b) {
			 return a[0].compareTo(b[0]);
				
		}
	};

}
