package pl.poznan.pointd.engine;

import java.util.Enumeration;
import java.util.Stack;
import java.util.Vector;

import pl.poznan.pointd.exceptions.ArityException;
import pl.poznan.pointd.exceptions.OperatorException;
import pl.poznan.pointd.exceptions.TokenException;

public class Engine {
	/**
	 * The array by which the percentage differences are translated into scores
	 * for the winning player and the loosing player.
	 */
	public static final AssocTable SCORING_TABLE = new AssocTable(16);
	static {
		SCORING_TABLE.put(new IntPair(0, 19), new IntPair(10, 10));
		SCORING_TABLE.put(new IntPair(20, 39), new IntPair(11, 9));
		SCORING_TABLE.put(new IntPair(40, 59), new IntPair(12, 8));
		SCORING_TABLE.put(new IntPair(60, 79), new IntPair(13, 7));
		SCORING_TABLE.put(new IntPair(80, 99), new IntPair(14, 6));
		SCORING_TABLE.put(new IntPair(100, 119), new IntPair(15, 5));
		SCORING_TABLE.put(new IntPair(120, 139), new IntPair(16, 4));
		SCORING_TABLE.put(new IntPair(140, 159), new IntPair(17, 3));
		SCORING_TABLE.put(new IntPair(160, 179), new IntPair(18, 2));
		SCORING_TABLE.put(new IntPair(180, 189), new IntPair(19, 1));
		SCORING_TABLE.put(new IntPair(190, 200), new IntPair(20, 0));
	}

	/**
	 * Debug mode: on or off.
	 */
	public static final boolean DEBUG = true;

	/**
	 * Default maximum number of total achievable major victory points.
	 */
	public static final int INITIAL_MAJOR_TOTAL = 1;

	/**
	 * Default maximum number of total achievable minor victory points.
	 */
	public static final int INITIAL_MINOR_TOTAL = 600;

	/**
	 * Variable is set to the text of a warning, if one occurs.
	 */
	private String warning;

	/**
	 * Checks if a warning has occurred while the engine was running.
	 * 
	 * @return <code>true</code> if a warning is set, <code>false</code> if it
	 *         isn't.
	 */
	public final boolean hasWarning() {
		return warning != null;
	}

	/**
	 * Get the text of a warning.
	 * 
	 * @return Text of a warning if one is set, or <code>null</code> if it
	 *         isn't.
	 */
	public final String getWarning() {
		return warning;
	}

	/**
	 * Set the text of the warning.
	 * <p>
	 * Only the <b>first</b> warning is kept, all other ones are ignored.
	 * 
	 * @param warning
	 *            the text of a warning.
	 */
	private final void setWarning(String warning) {
		if (hasWarning()) {
			return;
		}
		this.warning = warning;
	}

	/**
	 * Clear warnings.
	 */
	public final void clearWarning() {
		warning = null;
	}

	/**
	 * Determines who of the two players is the winner.
	 * 
	 * The player with more victory points is the winner, or if the number of
	 * players' victory points is the same, the player with the most kill points
	 * wins.
	 * 
	 * @param majorA
	 *            victory points of the first player
	 * @param minorA
	 *            kill points of the first player
	 * @param majorB
	 *            victory points of the second player
	 * @param minorB
	 *            kill points of the second player
	 * @param players
	 *            the symbols for the first and second player (a list of two
	 *            elements)
	 * @return the first or second element of the list given as players, or
	 *         <code>null</code> if no winner can be determined (it's a draw).
	 */
	public String determineWinner(int majorA, int minorA, int majorB,
			int minorB, StringPair players) {

		if (majorA > majorB) {
			return players.a;
		}

		if (majorB > majorA) {
			return players.b;
		}

		if (minorA > minorB) {
			return players.a;
		}

		if (minorB > minorA) {
			return players.b;
		}

		return null;
	}

	/**
	 * Convenience function to convert a ratio (a value to the maximum possible
	 * value) to a percentage representation.
	 * 
	 * @param value
	 *            a number between zero and <code>total</code>.
	 * @param total
	 *            a maximum possible value for the number.
	 * @return the ratio between the two numbers in percentage terms.
	 */
	private final double percentage(double value, double total) {
		return 100.0d * value / total;
	}

	/**
	 * Determines the percentage point difference between the players.
	 * 
	 * For each player the percentage of the achieved victory points to the
	 * total total victory points is established. Then the percentage of
	 * achieved kill points to the total available kill points are added to the
	 * percentage of victory points for each player.
	 * 
	 * The winner gets the difference between his own percentage and that of the
	 * looser's. The loser automatically gets 0%. If it is a draw, both players
	 * get 0%.
	 * 
	 * @param majorA
	 *            victory points of the first player
	 * @param minorA
	 *            kill points of the first player
	 * @param majorB
	 *            victory points of the second player
	 * @param minorB
	 *            kill points of the second player
	 * @param majorTotal
	 *            the maximum total achievable victory points
	 * @param minorTotal
	 *            the maximum total achievable kill points
	 * @param players
	 *            the symbols for the first and second player (a list of two
	 *            elements)
	 * @return a score of between 0 and 200.
	 */
	public double determinePercentage(int majorA, int minorA, int majorB,
			int minorB, int majorTotal, int minorTotal, StringPair players) {

		if (pointsExceedTotal(majorA, majorB, majorTotal)) {
			setWarning("More major points than total allows.");
		}

		if (pointsExceedTotal(minorA, minorB, minorTotal)) {
			setWarning("More minor points than total allows.");
		}

		String winner = determineWinner(majorA, minorA, majorB, minorB, players);

		if (winner == null) {
			return 0.0d;
		}

		boolean aWon = (winner == players.a);

		int majorWinner = aWon ? majorA : majorB;
		int majorLooser = aWon ? majorB : majorA;
		int minorWinner = aWon ? minorA : minorB;
		int minorLooser = aWon ? minorB : minorA;

		int majorDifference = majorWinner - majorLooser;
		int minorDifference = minorWinner - minorLooser;

		double percent = percentage(majorDifference, majorTotal);

		return percent + percentage(minorDifference, minorTotal);
	}

	/**
	 * Check if points were exceeded by either player.
	 * <p>
	 * A convenience method.
	 * 
	 * @param pointsA
	 *            points achieved by one player
	 * @param pointsB
	 *            points achieved by the other player
	 * @param pointsTotal
	 *            the total number of achievable points per player
	 * 
	 * @return <code>true</code> if either player got more points than the
	 *         total, otherwise <code>false</code>.
	 */
	private boolean pointsExceedTotal(int pointsA, int pointsB, int pointsTotal) {
		return pointsA > pointsTotal || pointsB > pointsTotal;
	}

	/**
	 * Determines the score gotten by each player.
	 * 
	 * The scores are determined by the SCORING_TABLE associative array. The
	 * array consists of string keys pointing to two-element lists of point
	 * values. The key is composed of two integers separated by a dash sign, the
	 * numbers indicate a range of percentages, where both numbers are included
	 * in the range. (So '1-9' means the numbers 1,2,3,4,5,6,7,8 and 9.)
	 * 
	 * @param percentage
	 *            the difference between the percentages gained by each player.
	 * @return a list of two elements - point values for each player, the value
	 *         for the winning player is indexed first. <code>null</code>, if no
	 *         range is fitted.
	 */
	public IntPair determineScore(double percentage) {
		IntPair lastRange = null;

		for (Enumeration i = SCORING_TABLE.keys(); i.hasMoreElements();) {
			IntPair range = (IntPair) i.nextElement();
			int a = range.a, b = range.b;
            

			if (percentage >= a && percentage <= b) { // Removed '+ 1'.
				return SCORING_TABLE.get(range);
			}

			lastRange = range;
		}

		if (lastRange == null) {
			return null;
		}

		return (IntPair) SCORING_TABLE.get(lastRange);
	}

	/**
	 * Parse a string representation of an arithmetic formula and evaluate it
	 * into a single result, if possible.
	 * 
	 * @param string
	 *            A representation of a mathematical expression.
	 * @return The result of the string-represented expression.
	 * @throws ArityException
	 *             in case when an operator is used with the wrong number of
	 *             arguments.
	 * @throws TokenException
	 *             in case tokens cannot be deduced from the string nor ignored.
	 * @throws OperatorException
	 *             in case an unknown operator is used during evaluation.
	 */
	public double parseString(String string) throws ArityException,
			TokenException, OperatorException {
		// Slice the string up into tokens representing numbers and operators.
		Token[] tokens = tokenizeString(string);

		// Reorganize the tokens into Reverse Polish Notation for easier
		// processing.
		Token[] rvp = shuntToRvp(tokens);

		// Evaluate the RVP expression.
		double result = evaluatePostfix(rvp);

		if (DEBUG) {
			System.err.println(string + " = " + result);
		}

		return result;
	}

	/**
	 * Evaluates a list of tokens representing a mathematical expression in
	 * Reverse Polish Notation into a single result.
	 * 
	 * @param tokens
	 *            a list of tokens in prefix representation.
	 * @return The result of the prefix-represented expression.
	 * @throws ArityException
	 *             in case when an operator is used with the wrong number of
	 *             arguments.
	 * @throws OperatorException
	 *             in case an unknown operator is used during evaluation.
	 */
	private double evaluatePostfix(Token[] tokens) throws ArityException,
			OperatorException {
		Stack stack = new Stack();

		// While there are input tokens left.
		for (int i = 0; i < tokens.length; i++) {
			// Read the next token from input.
			Token token = tokens[i];

			// If the token is a value push it onto the stack.
			if (token.isType(Token.NUMBER)) {
				stack.push(token);
				continue;
			}

			// If there are fewer than n values on the stack, it is known a
			// priori that the operator takes n arguments.
			// XXX All operators are binary.
			if (stack.size() < 2) {
				throw new ArityException("Operator " + token.getImage()
						+ " needs more arguments!");
			}

			// Else, Pop the top n values from the stack.
			Token token2 = (Token) stack.pop();
			Token token1 = (Token) stack.pop();

			// Evaluate the operator, with the values as arguments.
			double operand2 = Double.parseDouble(token2.getImage());
			double operand1 = Double.parseDouble(token1.getImage());
			double result = evaluate(token.getImage(), operand1, operand2);
			Token resultToken = Token.newNumber(String.valueOf(result));

			// Push the returned results, if any, back onto the stack.
			stack.push(resultToken);
		}

		// If there is only one value in the stack, that value is the result of
		// the calculation.
		if (stack.size() == 1) {
			Token token = (Token) stack.pop();
			if (token.isType(Token.NUMBER)) {
				return Double.parseDouble(token.getImage());
			}
		}

		// If there are more values in the stack, the user input has too many
		// values.
		throw new ArityException("Too many arguments.");
	}

	/**
	 * Perform the specified mathematical operation.
	 * 
	 * @param operator
	 * @param operand1
	 * @param operand2
	 * @return the result of the operation
	 * @throws ArityException
	 * @throws OperatorException
	 *             in case an unknown operator is used.
	 */
	private double evaluate(String operator, double operand1, double operand2)
			throws ArityException, OperatorException {
		// XXX All operators are single characters.
		char op = operator.charAt(0);
		switch (op) {
		case '+':
			return operand1 + operand2;
		case '-':
			return operand1 - operand2;
		case '*':
			return operand1 * operand2;
		case '/':
			return operand1 / operand2;
		default:
			throw new OperatorException("Unknown operator " + operator);
		}
	}

	/**
	 * Convert an expression in string form into a list of tokens.
	 * <p>
	 * The conversion will ignore any tokens that immediately cannot be
	 * processed as numbers or operators.
	 * 
	 * @param string
	 *            a string representation of an arithmetic expression.
	 * @return a list of tokens representing the expression.
	 * @throws TokenException
	 *             in case tokens cannot be deduced from the string nor ignored.
	 */
	public Token[] tokenizeString(String string) throws TokenException {
		Vector tokens = new Vector();

		Token last = Token.newStart();

		for (int i = 0; i < string.length(); i++) {
			char c = string.charAt(i);
			Token current = null;

			if (Token.isNumber(c)) {
				current = Token.newNumber(c);
			} else if (Token.isOperator(c)) {
				current = Token.newOperator(c);
			} else if (Token.isOpenBracket(c)) {
				current = Token.newOpenBracket();
			} else if (Token.isClosedBracket(c)) {
				current = Token.newClosedBracket();
			} else if (Token.isIgnored(c)) {
				current = Token.newIgnored(c);
			} else {
				System.err.println("Unknown character type: " + c
						+ ". Ignored.");
				setWarning("Unknown character type: " + c);
				current = Token.newIgnored(c);
			}

			if (Token.canJoin(last, current)) {
				current = Token.join(last, current);
			} else {
				tokens.addElement(last);
			}

			last = current;
		}
		tokens.addElement(last);

		Token[] result = new Token[tokens.size()];
		for (int i = 0; i < result.length; i++) {
			result[i] = (Token) tokens.elementAt(i);
		}

		return result;
	}

	public Token[] shuntToRvp(Token[] tokens) throws ArityException {
		Stack stack = new Stack();
		Vector output = new Vector(tokens.length);

		for (int i = 0; i < tokens.length; i++) {
			// Read a token.
			Token token = tokens[i];

			// If the token is a number, then add it to the output queue.
			if (token.isType(Token.NUMBER)) {
				output.addElement(token);
				// printIt(output, stack);
				continue;
			}

			// If the token is an operator, o1, then:
			if (token.isType(Token.OPERATOR)) {
				while (!stack.isEmpty()) {
					Token otherToken = (Token) stack.peek();

					// While there is an operator token, o2, at the top of the
					// stack.
					if (!otherToken.isType(Token.OPERATOR)) {
						break;
					}

					// And o1 is left-associative and its precedence is less
					// than or equal to that of o2.
					if (!(token.getPrecedence() <= otherToken.getPrecedence())) {
						break;
					}

					// XXX Ignoring right-associative operators.

					// Pop o2 off the stack, onto the output queue;
					output.addElement(stack.pop());
				}

				stack.push(token);
				continue;
			}

			// If the token is a left parenthesis, then push it onto the stack.
			if (token.isType(Token.BRACKET_OPEN)) {
				stack.push(token);
				continue;
			}

			// If the token is a right parenthesis.
			if (token.isType(Token.BRACKET_CLOSE)) {
				boolean foundParentheses = false;

				// Until the token at the top of the stack is a left
				// parenthesis, pop operators off the stack onto the output
				// queue.
				while (!stack.isEmpty()) {
					Token otherToken = (Token) stack.peek();
					if (otherToken.isType(Token.BRACKET_OPEN)) {
						// Pop the left parenthesis from the stack, but not onto
						// the output queue.
						// Token forget = (Token)
						stack.pop();
						// System.out.println("[RVP] pop and forget: " +
						// forget);
						// printIt(output, stack);

						foundParentheses = true;
						break;
					}
					output.addElement(stack.pop());
					// printIt(output, stack);
				}

				// XXX Functions are ignored.

				// If the stack runs out without finding a left parenthesis,
				// then there are mismatched parentheses.
				if (!foundParentheses) {
					throw new ArityException("Mismatched parentheses!");
				}
			}

			// Ignore starting token.
			if (token.isType(Token.START) || token.isType(Token.IGNORED)) {
				continue;
			}
		}

		// When there are no more tokens to read but while there are still
		// operator tokens in the stack:
		while (!stack.isEmpty()) {
			Token token = (Token) stack.pop();

			// If the operator token on the top of the stack is a parenthesis,
			// then there are mismatched parentheses.
			if (token.isType(Token.BRACKET_CLOSE)
					|| token.isType(Token.BRACKET_OPEN)) {
				throw new ArityException("Mismatched parentheses!");
			}

			// Pop the operator onto the output queue.
			output.addElement(token);
		}

		Token[] result = new Token[output.size()];
		for (int i = 0; i < result.length; i++) {
			result[i] = (Token) output.elementAt(i);
		}

		return result;
	}

	// private void printDebug(Vector output, Stack stack) {
	// System.out.print("Stack: ");
	// for (int i = 0; i < stack.size(); i++) {
	// System.err.print(stack.elementAt(i) + " ");
	// }
	// System.out.println();
	// System.out.print("Output: ");
	// for (int k = 0; k < output.size(); k++) {
	// if (output.elementAt(k) == null) {
	// continue;
	// }
	// System.err.print(output.elementAt(k) + " ");
	// }
	// System.out.println();
	// }
}
