package pl.poznan.pointd.engine;

public class Entry {
	public IntPair key, value;

	public Entry(IntPair key, IntPair value) {
		this.key = key;
		this.value = value;
	}

	public int hashCode() {
		return key.hashCode() + value.hashCode();
	}

	public boolean equals(Object o) {
		if (!(o instanceof Entry)) {
			return false;
		}
		Entry p = (Entry) o;
		return key.equals(p.key) && value.equals(p.value);
	}

	public int[] toArray() {
		return new int[]{key.a, key.b, value.a, value.b};
	}
}
