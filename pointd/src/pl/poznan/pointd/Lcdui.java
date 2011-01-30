/* 
 *  Copyright 2011 Konrad Siek <konrad.siek@gmail.com>
 *
 *  This file is part of Point'd.
 *
 *  Point'd is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Point'd is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Point'd.  If not, see <http://www.gnu.org/licenses/>.  
 */
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

import pl.poznan.pointd.engine.Engine;
import pl.poznan.pointd.engine.IntPair;
import pl.poznan.pointd.engine.StringPair;
import pl.poznan.pointd.exceptions.EngineException;

public class Lcdui extends MIDlet implements CommandListener {

	private static final int SPACER_WIDTH = 50;
	private static final int SPACER_HEIGHT = 10;
	private static final int TEXTFIELD_SIZE = 40;

	private Displayable scoreForm;
	private Displayable percentageTable;

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

	private StringPair players;

	private Engine engine;
	private Command back;
	private Display display;
	private Command exit;
	private StringItem status;

	/**
	 * Creates several screens and navigates between them.
	 */
	public Lcdui() {
		this.display = Display.getDisplay(this);

		this.count = new Command("Count", Command.OK, 1);
		this.flip = new Command("Lookup", Command.BACK, 1);
		this.exit = new Command("Exit", Command.EXIT, 1);
		this.back = new Command("Back", Command.BACK, 1);

		this.scoreForm = getScoreForm();
		this.scoreForm.setCommandListener(this);
		this.scoreForm.addCommand(this.count);
		this.scoreForm.addCommand(this.flip);
		this.scoreForm.addCommand(this.exit);

		this.percentageTable = getPercentages();
		this.percentageTable.setCommandListener(this);
		this.percentageTable.addCommand(this.back);
		this.scoreForm.addCommand(this.exit);
	}

	private Displayable getScoreForm() {
		Form form = new Form("Point'd");
		StringItem subtitle = new StringItem("A point counting utility", null);

		majorTotal = new TextField("Major total",
				String.valueOf(Engine.INITIAL_MAJOR_TOTAL), TEXTFIELD_SIZE,
				TextField.ANY);
		minorTotal = new TextField("Minor total",
				String.valueOf(Engine.INITIAL_MINOR_TOTAL), TEXTFIELD_SIZE,
				TextField.ANY);

		majorA = new TextField("Major A", "", TEXTFIELD_SIZE, TextField.ANY);
		minorA = new TextField("Minor A", "", TEXTFIELD_SIZE, TextField.ANY);

		majorB = new TextField("Major B", "", TEXTFIELD_SIZE, TextField.ANY);
		minorB = new TextField("Minor B", "", TEXTFIELD_SIZE, TextField.ANY);

		scoreA = new StringItem("Score A", "0");
		scoreB = new StringItem("Score B", "0");

		percent = new StringItem("Win ratio", "0%");

		players = new StringPair("A", "B");
		
		status = new StringItem("","");

		engine = new Engine();

		form.append(subtitle);
		form.append(new Spacer(SPACER_WIDTH, SPACER_HEIGHT));

		form.append(majorA);
		form.append(majorB);
		form.append(majorTotal);
		form.append(new Spacer(SPACER_WIDTH, SPACER_HEIGHT));

		form.append(minorA);
		form.append(minorB);
		form.append(minorTotal);
		form.append(new Spacer(SPACER_WIDTH, SPACER_HEIGHT));

		form.append(percent);
		form.append(new Spacer(SPACER_WIDTH, SPACER_HEIGHT));
		form.append(scoreA);
		form.append(scoreB);
		
		form.append(new Spacer(SPACER_WIDTH, SPACER_HEIGHT));
		
		form.append(status);

		return form;
	}

	private Displayable getPercentages() {
		List list = new List("Lookup table", List.IMPLICIT);

		list.append(
				"Percentages are translated into scores by the following table:",
				null);

		for (Enumeration i = Engine.SCORING_TABLE.keys(); i.hasMoreElements();) {
			IntPair range = (IntPair) i.nextElement();
			IntPair score = (IntPair) Engine.SCORING_TABLE.get(range);

			//System.err.println(range + " " + score);

			String rangeString = range.a + "%" + "-" + range.b + "%";
			String scoreString = score.a + ":" + score.b;

			list.append(rangeString + " = " + scoreString, null);
		}

		return list;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see javax.microedition.midlet.MIDlet#startApp()
	 */
	protected void startApp() throws MIDletStateChangeException {
		this.display.setCurrent(this.scoreForm);
		// Display.init(this);
	}
	
	private void clearStatus() {
		status.setText("");
		status.setLabel("");
	}
	
	private void setStatus(String type, String message) {
		if (status.getText() != null && status.getText().length() > 0) {
			// A warning is already displayed.
			return;
		}
		
		status.setText(message);
		status.setLabel(type);
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
			return;
		}

		if (command == this.count) {
			clearStatus();
			engine.clearWarning();
			
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

			// Determine what score each of the players get for the victory
			IntPair score = engine.determineScore(percentage);

			// Write out each player's scores.
			this.scoreA.setText((winner == players.a ? score.a : score.b) + "");
			this.scoreB.setText((winner == players.b ? score.a : score.b) + "");

			// Write out the percentage.
			String percentString = Double.toString(percentage);
			if (percentString.length() > 6) {
				percentString = percentString.substring(0, 6);
			}
			this.percent.setText(percentString + "%");

			return;
		}

		if (command == exit) {
			notifyDestroyed();
		}
	}

	private final int getIntOfField(TextField field) {
		String text = field.getString();
		if (text.length() == 0) {
			return 0;
		}
		try {
			double value = engine.parseString(text);

			if (engine.hasWarning()) {
				setStatus("Warning", engine.getWarning());
			}

			return (new Double(value)).intValue();
		} catch (EngineException e) {
			setStatus("Error", e.getMessage());
			e.printStackTrace();
			return 0;
		}
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
