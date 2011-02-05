package pl.poznan.pointd.engine;

public class IntPair {
	public int a, b;

	public IntPair(int a, int b) {
		this.a = a;
		this.b = b;
	}

	public int hashCode() {
		return a + b;
	}

	public boolean equals(Object o) {
		if (!(o instanceof IntPair)) {
			return false;
		}
		IntPair p = (IntPair) o;
		return a == p.a && b == p.b;
	}

	public String toString() {
		return "(" + a + ", " + b + ")";
	}
}
