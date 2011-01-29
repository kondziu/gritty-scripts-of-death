package pl.poznan.pointd.engine;

public class StringPair {
	public String a, b;

	public StringPair(String a, String b) {
		this.a = a;
		this.b = b;
	}

	public int hashCode() {
		return a.hashCode() + b.hashCode();
	}

	public boolean equals(Object o) {
		if (!(o instanceof StringPair)) {
			return false;
		}
		StringPair p = (StringPair) o;
		return a.equals(p.a) && b.equals(p.b);
	}

	public String toString() {
		return "(" + a + ", " + b + ")";
	}
}
