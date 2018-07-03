
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Task1 {

	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);
	public static String queryPath="//Users//Shraddha//Desktop//IR-Project//Phase1//Task1//TaskB//queries.txt";
	public static ArrayList<String> query=new ArrayList<String>();

	private static void readDataFromFile() {
		try {
			
			BufferedReader br=new BufferedReader(new FileReader(new File(queryPath)));
			String s="";
			try {
				while((s=br.readLine())!=null)
				{
					query.add(s);
				}
			} catch (IOException ex) {
				System.out.println("IOException");
			}
		} catch (FileNotFoundException ex) {
			System.out.println("FileNotFoundException");
		}
	}

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {


		String indexPath = "//Users//Shraddha//Desktop//IR-Project//Phase1//Task1//TaskB//index";
		String s = "//Users//Shraddha//Desktop//IR-Project//Phase1//Task1//TaskB//index";

		Task1 indexer = null;
		try {
			indexer = new Task1(s);
		} catch (Exception ex) {
			System.exit(-1);
		}

		// try to add file into the index
		indexer.indexFileOrDirectory("//Users//Shraddha//Desktop//IR-Project//cleaned_cacm");


		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================


		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexPath)));

		readDataFromFile();


		s = "";
		
		for (int j=0;j<query.size();j++) {
			try {
				IndexSearcher searcher = new IndexSearcher(reader);
				TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
				System.out.println("Query  "+j+"  "+query.get(j));
				s=query.get(j);
				Query q = new QueryParser(Version.LUCENE_47, "contents",
						sAnalyzer).parse(s);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				BufferedWriter w = new BufferedWriter(new FileWriter("//Users//Shraddha//Desktop//IR-Project//Phase1//Task1//TaskB//LuceneRanking.txt", true));
				BufferedWriter w1 = new BufferedWriter(new FileWriter("//Users//Shraddha//Desktop//IR-Project//Phase1//Task1//TaskB//LuceneStats.txt", true));
				w.write("Query: " + s);
				w.write("\n");
				w.write("\n");
				String header = String.format("%8s|%8s|%70s|%8s|%20s|%15s", "QueryID", "Literal", "DocID", "Rank" , "Score", "SystemName");
				
				w.write(header);
				w.write("\n");
				System.out.println("Found " + hits.length + " hits.");
				for (int i = 0; i < hits.length; ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					String name = d.get("path").split("/Users/Shraddha/Desktop/IR-Project/cleaned_cacm/")[1];
					name = (docId + 1) + "(" + name + ")";
					String line = String.format("%8d|%8s|%70s|%8d|%20f|%15s", (j + 1), "Q0", name, (i + 1) , hits[i].score, "shraddha");
				    String line1 = (j + 1) + " " + (i + 1) + " " + (docId + 1) + " " + hits[i].score;
				    
					w.write(line);
				    w.write("\n");
				    w1.write(line1);
				    w1.write("\n");
				}
				w.write("\n");
				w.close();
				w1.close();


			} catch (Exception e) {
				System.out.println("Error searching " + s + " : "
						+ e.getMessage());
				break;
			}

		}

	}

	/**
	 * Constructor
	 *
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	Task1(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 *
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				// System.out.println(f);
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 *
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}


}

