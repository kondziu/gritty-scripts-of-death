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
