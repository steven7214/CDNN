import java.io.*;
import org.apache.poi.hssf.usermodel.*;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.util.*;

public class ARFF_converter {

	public static void main(String[] args) {
		try {
			FileInputStream file = new FileInputStream(new File("Data/CancerSEEK/Supplmentary Tables (Steven).xlsx"));
			BufferedWriter writer = new BufferedWriter(new FileWriter("Data/CancerSeek/protein.arff"));
			writer.write("@relation ProteinMarkerConcentration \n \n");
			// Get the workbook instance for XLS file
			Workbook workbook = WorkbookFactory.create(file);

			// Get third(numbering starts from 0) sheet from the workbook
			Sheet table = workbook.getSheet("Table S6");

			// Get iterator to all the rows in current sheet

			int num = table.getLastRowNum();
			Row row = table.getRow(2);
			for (int count = 4; count < row.getLastCellNum() - 2; count++) {
				String line = "@attribute \"" + row.getCell(count).getStringCellValue() + "\" real";
				writer.write(line + "\n");
			}
			writer.write("@attribute Result {Positive, Negative} \n \n");
	
			writer.write("@DATA\n");
			for (int count = 3; count < 1820; count++) {
				row = table.getRow(count);
				String line = "" + row.getCell(4);
		//		if (line.substring(0,1) == "*")
		//			line = line.substring(1);
				for (int value = 5; value < 43; value++) {
					String added = "," + row.getCell(value);
		//			if (added.substring(1,2) == "*")
		//				added = added.substring(0,1) + added.substring(2);
					line += added;
				}
				line += "," + row.getCell(46).getStringCellValue(); //get the final answer
				writer.write(line + "\n");
			}
			writer.close();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

}
