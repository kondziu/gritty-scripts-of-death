package pl.poznan.pointd.engine;

import pl.poznan.pointd.exceptions.TokenException;

class Token {
	public static final int START = 0;
	public static final int NUMBER = 1;
	public static final int OPERATOR = 2;
	public static final int BRACKET_OPEN = 4;
	public static final int BRACKET_CLOSE = 8;
	public static final int IGNORED = 16;

	public Token(int type, String image) {
		this.type = type;
		this.image = image;
	}

	public Token(int type) {
		this.type = type;
		this.image = "";
	}

	private String image;
	private int type;

	public boolean sameType(Token token) {
		return type == token.type;
	}

	public static final boolean canJoin(Token a, Token b) {
		if (a == null || b == null) {
			return false;
		}

		if (!a.sameType(b)) {
			return false;
		}

		if (a.type == BRACKET_CLOSE || a.type == BRACKET_OPEN) {
			return false;
		}

		return true;
	}

	public static final Token join(Token a, Token b) throws TokenException {
		if (a == null) {
			return b;
		}

		if (b == null) {
			return a;
		}

		if (!a.sameType(b)) {
			throw new TokenException("Cannot join tokens of "
					+ "different types. Tokens: " + a + " and " + b + ".");
		}

		Token result = new Token(a.type, a.image);
		result.image = result.image.concat(b.image);

		return result;
	}

	public String getImage() {
		return image;
	}

	public int getType() {
		return type;
	}

	public String toString() {
		return "(" + type + ", " + image + ")";
	}

	public static final Token newStart() {
		return new Token(START, "=");
	}

	public static Token newIgnored(char c) {
		return newIgnored((new Character(c)).toString());
	}

	public static Token newIgnored(String string) {
		return new Token(IGNORED, string);
	}

	public static final Token newOpenBracket() {
		return new Token(BRACKET_OPEN, "(");
	}

	public static final Token newClosedBracket() {
		return new Token(BRACKET_CLOSE, ")");
	}

	public static final Token newNumber(char number) {
		return newNumber((new Character(number)).toString());
	}

	public static final Token newNumber(String number) {
		return new Token(NUMBER, number);
	}

	public static final Token newOperator(char operator) {
		return newOperator((new Character(operator)).toString());
	}

	public static final Token newOperator(String operator) {
		return new Token(OPERATOR, operator);
	}

	public static boolean isNumber(char c) {
		return c == ',' || c == '.' || Character.isDigit(c);
	}

	public static boolean isOperator(char c) {
		return c == '*' || c == '/' || c == '+' || c == '-';
	}

	public static boolean isOpenBracket(char c) {
		return c == '(';
	}

	public static boolean isClosedBracket(char c) {
		return c == ')';
	}

	public static boolean isIgnored(char c) {
		return c == ' ' || c == '\t';
	}

	public boolean isType(int type) {
		return type == this.type;
	}

	public int getPrecedence() {
		if (type != OPERATOR) {
			return -1;
		}

		char c = image.charAt(0);

		switch (c) {
		case '*':
		case '/':
			return 3;
		case '+':
		case '-':
			return 2;
		default:
			return 1;
		}
	}
}