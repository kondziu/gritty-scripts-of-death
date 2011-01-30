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
