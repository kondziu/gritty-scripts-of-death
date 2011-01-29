package pl.poznan.pointd;

import java.io.IOException;
import java.util.Enumeration;

import javax.microedition.midlet.MIDlet;

import pl.poznan.pointd.engine.Engine;
import pl.poznan.pointd.engine.IntPair;
import pl.poznan.pointd.engine.StringPair;
import pl.poznan.pointd.exceptions.EngineException;

import com.sun.lwuit.Command;
import com.sun.lwuit.Display;
import com.sun.lwuit.Form;
import com.sun.lwuit.Label;
import com.sun.lwuit.TextArea;
import com.sun.lwuit.animations.CommonTransitions;
import com.sun.lwuit.events.ActionEvent;
import com.sun.lwuit.events.ActionListener;
import com.sun.lwuit.layouts.BoxLayout;
import com.sun.lwuit.layouts.Layout;
import com.sun.lwuit.plaf.UIManager;
import com.sun.lwuit.table.TableLayout;
import com.sun.lwuit.table.TableLayout.Constraint;
import com.sun.lwuit.util.Resources;

public class Lwuit extends MIDlet implements ActionListener {
	private Command exitCommand;
	private Command flipCommand;
	private Command backCommand;
	private Command countCommand;

	private Form scoreForm;
	private Form tableForm;
	private TextArea majorA;
	private TextArea majorB;
	private TextArea minorA;
	private TextArea minorB;
	private TextArea majorTotal;
	private TextArea minorTotal;
	private Label scoreA;
	private Label scoreB;
	private Label percentage;
	private Engine engine;
	private Label status;
	private StringPair players;

	public void startApp() {
		Display.init(this);

		try {
			Resources res = Resources.open("/custom_theme.res");
			String resource = res.getThemeResourceNames()[0];
			UIManager.getInstance().setThemeProps(res.getTheme(resource));
		} catch (IOException e) {
			e.printStackTrace();
		}

		initCommands();
		initScoreForm();
		initTableForm();

		engine = new Engine();

		players = new StringPair("A", "B");
	}

	private void initCommands() {
		exitCommand = new Command("Exit");
		flipCommand = new Command("Lookup");
		backCommand = new Command("Back");
		countCommand = new Command("Count");
	}

	private void initTableForm() {
		tableForm = new Form("Lookup table");
		Layout layout = new BoxLayout(BoxLayout.Y_AXIS);
		tableForm.setLayout(layout);

		TextArea title = new TextArea("Percentages are translated "
				+ "into scores by the following table:", 4);
		title.setEditable(false);
		title.setFocusable(false);
		tableForm.addComponent(title);

		// List list = new List();
		for (Enumeration i = Engine.SCORING_TABLE.keys(); i.hasMoreElements();) {
			IntPair key = (IntPair) i.nextElement();
			IntPair value = Engine.SCORING_TABLE.get(key);
			String text = key.a + "-" + key.b + " = " + value.a + ":"
					+ value.b;
			Label label = new Label(text);
			tableForm.addComponent(label);
			// list.addItem();
		}

		Label end = new Label();
		end.setFocusable(true);
		tableForm.addComponent(end);

		tableForm.setTransitionOutAnimator(CommonTransitions.createSlide(
				CommonTransitions.SLIDE_HORIZONTAL, false, 200));

		tableForm.addCommand(backCommand);
		tableForm.addCommand(exitCommand);
		tableForm.addCommandListener(this);
	}

	private void initScoreForm() {
		scoreForm = new Form("Point'd");
		TableLayout layout = new TableLayout(7, 4);
		scoreForm.setLayout(layout);
		scoreForm.show();

		Label title = new Label("A point counting utility");
		Constraint titleSpan = layout.createConstraint();
		titleSpan.setHorizontalSpan(4);
		titleSpan.setWidthPercentage(100);
		// constraint.setWidthPercentage(50);

		// TextArea end = new TextArea();
		status = new Label();
		status.setFocusable(true);
		// end.setEditable(false);
		Constraint endSpan = layout.createConstraint();
		endSpan.setHorizontalSpan(4);
		endSpan.setWidthPercentage(100);

		Label placeholderLabel = new Label("");
		Label playerALabel = new Label("A");
		Label playerBLabel = new Label("B");
		Label totalLabel = new Label("Max");

		Label majorLabel = new Label("Major Points"); // Victory Points
		Label minorLabel = new Label("Minor Points"); // Kill Points

		Label percentageLabel = new Label("Percentage");
		Label scoreLabel = new Label("Score");

		majorA = new TextArea("");
		majorB = new TextArea("");
		minorA = new TextArea("");
		minorB = new TextArea("");

		// majorA.setConstraint(TextArea.NUMERIC);
		// majorB.setConstraint(TextArea.NUMERIC);
		// minorA.setConstraint(TextArea.NUMERIC);
		// minorB.setConstraint(TextArea.NUMERIC);

		majorTotal = new TextArea(String.valueOf(Engine.INITIAL_MAJOR_TOTAL));
		minorTotal = new TextArea(String.valueOf(Engine.INITIAL_MINOR_TOTAL));

		scoreA = new Label("0");
		scoreB = new Label("0");
		percentage = new Label("0%");

		Constraint percentageSpan = layout.createConstraint();
		percentageSpan.setHorizontalSpan(2);

		scoreForm.addComponent(titleSpan, title);

		scoreForm.addComponent(placeholderLabel);
		scoreForm.addComponent(playerALabel);
		scoreForm.addComponent(playerBLabel);
		scoreForm.addComponent(totalLabel);

		scoreForm.addComponent(majorLabel);
		scoreForm.addComponent(majorA);
		scoreForm.addComponent(majorB);
		scoreForm.addComponent(majorTotal);

		scoreForm.addComponent(minorLabel);
		scoreForm.addComponent(minorA);
		scoreForm.addComponent(minorB);
		scoreForm.addComponent(minorTotal);

		scoreForm.addComponent(percentageLabel);
		scoreForm.addComponent(percentageSpan, percentage);
		scoreForm.addComponent(new Label(""));

		scoreForm.addComponent(scoreLabel);
		scoreForm.addComponent(scoreA);
		scoreForm.addComponent(scoreB);
		scoreForm.addComponent(new Label(""));

		scoreForm.addComponent(endSpan, status);

		scoreForm.setTransitionOutAnimator(CommonTransitions.createSlide(
				CommonTransitions.SLIDE_HORIZONTAL, false, 200));

		scoreForm.addCommand(countCommand);
		scoreForm.addCommand(flipCommand);
		scoreForm.addCommand(exitCommand);
		scoreForm.addCommandListener(this);
	}

	public void pauseApp() {
	}

	public void destroyApp(boolean unconditional) {
	}

	public void actionPerformed(ActionEvent ae) {
		Command command = ae.getCommand();
		if (command == flipCommand) {
			tableForm.show();
			return;
		}

		if (command == backCommand) {
			scoreForm.show();
			return;
		}

		if (command == countCommand) {
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
			this.percentage.setText(percentString + "%");

			return;
		}

		if (command == exitCommand) {
			notifyDestroyed();
		}
	}

	private int getIntOfField(TextArea area) {
		String text = area.getText();
		if (text.length() == 0) {
			return 0;
		}

		// Attempt to parse the quite-possibly-arithmetic expression.
		try {
			double value = engine.parseString(text);

			if (engine.hasWarning()) {
				setStatus(engine.getWarning());
			}

			return (new Double(value)).intValue();
		} catch (EngineException e) {
			setStatus(e.getMessage());
			e.printStackTrace();
			return 0;
		}
	}

	private void clearStatus() {
		status.setText("");
	}
	
	private void setStatus(final String message) {		
		if (status.getText().length() > 0) {
			// A warning is already displayed.
			return;
		}
				
		Runnable runnable = new Runnable() {
			public void run() {
				status.setText(message);
				scoreForm.repaint();
			}
		};
		
		Display.getInstance().callSerially(runnable);
	}
}