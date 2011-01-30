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
