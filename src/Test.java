import java.util.*;
public class Test {

	public static void main(String[] args) {
		HashMap<String[], Integer> test = new HashMap<String[], Integer>();
		String[] input = {"hi", "bill"};
		test.put(input, 7);
		String[] tester = {"hi", "bill"};
		System.out.println(input);
		System.out.println(tester);
		if (test.containsKey(tester))
			System.out.println("true");
		
	}

}
