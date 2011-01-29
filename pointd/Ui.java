package pl.poznan.pointd;

import java.util.Enumeration;

import javax.microedition.lcdui.Command;
import javax.microedition.lcdui.CommandListener;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.lcdui.Form;
import javax.microedition.lcdui.List;
import javax.microedition.lcdui.Spacer;
import javax.microedition.lcdui.StringItem;
import javax.microedition.lcdui.TextField;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

public class Ui extends MIDlet implements CommandListener {

	private Displayable scoreForm;
	private Displayable percentageTable;
	//private Display display;
	private Command count;
	private Command flip;

	TextField majorTotal;
	TextField minorTotal;

	TextField majorA;
	TextField minorA;

	TextField majorB;
	TextField minorB;

	StringItem scoreA;
	StringItem scoreB;
	StringItem percent;

	private int lastMajorTotal = 1;
	private int lastMinorTotal = 2000;
	private StringPair players;
	private Engine engine;
	private Command back;

	/**
	 * Creates several screens and navigates between them.
	 */
	public Ui() {
		this.display = Display.getDisplay(this);

		this.count = new Command("Count", Command.OK, 1);
		this.flip = new Command("Lookup", Command.BACK, 1);
		this.flip = new Command("Exit", Command.EXIT, 1);
		this.back = new Command("Back", Command.BACK, 1);

		this.scoreForm = getScoreForm();
		this.scoreForm.setCommandListener(this);
		this.scoreForm.addCommand(this.count);
		this.scoreForm.addCommand(this.flip);

		this.percentageTable = getPercentages();
		this.percentageTable.setCommandListener(this);
		this.percentageTable.addCommand(this.back);
	}

	private Displayable getScoreForm() {
		Form form = new Form("Results");

		majorTotal = new TextField("Major total",
				String.valueOf(lastMajorTotal), 8, TextField.DECIMAL);
		minorTotal = new TextField("Minor total",
				String.valueOf(lastMinorTotal), 8, TextField.DECIMAL);

		majorA = new TextField("Major A", "0", 8, TextField.DECIMAL);
		minorA = new TextField("Minor A", "0", 8, TextField.DECIMAL);

		majorB = new TextField("Major B", "0", 8, TextField.DECIMAL);
		minorB = new TextField("Minor B", "0", 8, TextField.DECIMAL);

		scoreA = new StringItem("Score A", "0");
		scoreB = new StringItem("Score B", "0");

		percent = new StringItem("Win ratio", "0%");

		players = new StringPair("A", "B");

		engine = new Engine();

		form.append(majorA);
		form.append(minorA);
		form.append(new Spacer(10, 10));

		form.append(majorB);
		form.append(minorB);
		form.append(new Spacer(10, 10));

		form.append(majorTotal);
		form.append(minorTotal);
		form.append(new Spacer(10, 10));

		form.append(percent);
		form.append(scoreA);
		form.append(scoreB);

		return form;
	}

	private Displayable getPercentages() {
		List list = new List("Lookup table", List.IMPLICIT);

		for (Enumeration i = Engine.SCORING_TABLE.keys(); i.hasMoreElements();) {
			IntPair range = (IntPair) i.nextElement();
			IntPair score = (IntPair) Engine.SCORING_TABLE.get(range);

			System.err.println(range + " " + score);

			String rangeString = range.a + "%" + "-" + range.b + "%";
			String scoreString = score.a + ":" + score.b;

			list.append(rangeString + " -> " + scoreString, null);
		}

		return list;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see javax.microedition.midlet.MIDlet#startApp()
	 */
	protected void startApp() throws MIDletStateChangeException {
		//this.display.setCurrent(this.scoreForm);
		Display.init(this);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * javax.microedition.lcdui.CommandListener#commandAction(javax.microedition
	 * .lcdui.Command, javax.microedition.lcdui.Displayable)
	 */
	public void commandAction(Command command, Displayable displayable) {
		if (command == this.flip || command == this.back) {
			if (displayable == this.scoreForm) {
				this.display.setCurrent(this.percentageTable);
			} else {
				this.display.setCurrent(this.scoreForm);
			}
		}

		if (command == this.count) {
			int minorTotal = getIntOfField(this.minorTotal);
			int minorA = getIntOfField(this.minorA);
			int minorB = getIntOfField(this.minorB);

			int majorTotal = getIntOfField(this.majorTotal);
			int majorA = getIntOfField(this.majorA);
			int majorB = getIntOfField(this.majorB);

			// Determine which of the players have more points.
			String winner = engine.determineWinner(majorA, minorA, majorB,
					minorB, players);

			// Determine how successful the victorious force was.
			double percentage = engine.determinePercentage(majorA, minorA,
					majorB, minorB, majorTotal, minorTotal, players);
			
			System.err.println("PERC " + percentage);

			// Determine what score each of the players get for the victory
			IntPair score = engine.determineScore(percentage);

			// Write out each player's scores.
			this.scoreA.setText((winner == players.a ? score.a : score.b) + "");
			this.scoreB.setText((winner == players.b ? score.a : score.b) + "");
			
			// Write out the percentage.
			this.percent.setText(percentage + "%");
		}
	}

	private final int getIntOfField(TextField field) {
		String string = field.getString();
		return Integer.parseInt(string);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see javax.microedition.midlet.MIDlet#destroyApp(boolean)
	 */
	protected void destroyApp(boolean unconditional)
			throws MIDletStateChangeException {
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see javax.microedition.midlet.MIDlet#pauseApp()
	 */
	protected void pauseApp() {
	}
}
