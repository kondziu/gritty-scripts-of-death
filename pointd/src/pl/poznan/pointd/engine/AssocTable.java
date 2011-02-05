package pl.poznan.pointd.engine;

import java.util.Enumeration;

public class AssocTable {

	Entry[] table;
	int size = 0;

	public AssocTable(int capacity) {
		table = new Entry[capacity];
	}

	public boolean put(IntPair key, IntPair value) {
		for (int i = 0; i < size; i++) {
			if (table[i].key.equals(key)) {
				table[i].value = value;
				return true;
			}
		}

		if (size >= table.length) {
			return false;
		}

		table[size++] = new Entry(key, value);

		return true;
	}

	public Enumeration keys() {
		return new Enumeration() {
			int cursor;

			public Object nextElement() {
				return table[cursor++].key;
			}

			public boolean hasMoreElements() {
				return cursor < size;
			}
		};
	}

	public IntPair get(IntPair key) {
		for (int i = 0; i < size; i++) {
			if (table[i].key.equals(key)) {
				return table[i].value;
			}
		}
		return null;
	}
}
