package queensProblem;

import java.util.ArrayList;
import java.util.Arrays;

/**
 * 
 * @author sturlaf
 *
 */
public class Board {

	private int dim, queensFacing;
	private ArrayList<Integer> queens;
	private ArrayList<ArrayList<Integer>> moveValues;

	
	/**
	 * Initializes the board
	 * @param queens A list with the positions of all queens; each queen has one column, and the integer specifies where in the column the queen is. 
	 */
	public Board(ArrayList<Integer> queens) {
		this.dim = queens.size();
		this.moveValues = new ArrayList<ArrayList<Integer>>();
		this.setQueens(queens);
	}
	

	public ArrayList<Integer> getQueens() {
		return queens;
	}

	public void setQueens(ArrayList<Integer> queens) {
		checkConfig(queens);
		this.queens = queens;
		this.queensFacing();
		this.calcMoveValues();
	}

	public int getDim() {
		return dim;
	}
	
	public int getQueensFacing() {
		return this.queensFacing;
	}
	
	/**
	 * Checks if the given configuration is valid. Throws IllegalArgumentException if not valid.
	 * @param queens a list with the configurations of the queens
	 */
	private void checkConfig(ArrayList<Integer> queens) {
		//Checks every queen in the list, if it is on the board
		for(int queen : queens) {
			if ((queen < 0) || (queen > this.getDim())) {
				throw new IllegalArgumentException("This configuration is not valid: " + queens.toString());
			}
		}	
	}
	
	/**
	 * Counts the number of queens facing each other. A solution of the n-queens problem should have no queens facing.
	 * @return the number of queens facing each others
	 */
	private void queensFacing() {
		int nrQueensFacing = 0;
		for ( int col = 0; col < this.getDim(); col++) {
			int queenPos = this.queens.get(col);
			//Check all rows and diagonals right of this column, and counts the number of queens facing this queen from the right
			for( int i = col + 1; i < this.getDim(); i++) {
				//Get the position of the queen in column i
				int pos = this.queens.get(i);
				//Check if the queen on this column is on the same row as this queen
				if (pos == queenPos) {
					nrQueensFacing++;
				}
				//Checks if the queen is on the diagonal from, and therefore facing the queen in row col
				else if (queenPos + (i - col) == pos) {
					nrQueensFacing++;
				}
				else if (queenPos - (i - col) == pos) {
					nrQueensFacing++;
				}
			}
		}
		
		this.queensFacing = nrQueensFacing;
	}
	
	private int updateQueensFacing(int col, int newRow) {
		int oldNrQueensFacing = -1;
		int newNrQueensFacing = 0;
		int queenPos = this.queens.get(col);
		for(int index = 0; index < this.getDim(); index++) {
			//Get the position of the queen in column i
			int pos = this.queens.get(index);
			//Check if the queen on this column is on the same row as this queen
			if (pos == queenPos) {
				oldNrQueensFacing++;
			}
			//Checks if the queen is on the diagonal from, and therefore facing the queen in row col
			else if (queenPos + (index - col) == pos) {
				oldNrQueensFacing++;
			}
			else if (queenPos - (index - col) == pos) {
				oldNrQueensFacing++;
			}
			//Check if the queen on this column is on the same row as this queen
			if (pos == newRow) {
				newNrQueensFacing++;
			}
			//Checks if the queen is on the diagonal from, and therefore facing the queen in row col
			else if (newRow + (index - col) == pos) {
				newNrQueensFacing++;
			}
			else if (newRow - (index - col) == pos) {
				newNrQueensFacing++;
			}
		}
		return this.queensFacing - oldNrQueensFacing + newNrQueensFacing;
	}
	
	private void calcMoveValues() {
		this.moveValues.clear();
		for (int col = 0; col < this.getDim(); col++) {
			ArrayList<Integer> column = new ArrayList<Integer>();
			for (int row = 0; row < this.getDim(); row++) {
				int posQueen = this.queens.get(col);
				if (row == posQueen) {
					column.add(this.queensFacing);
				}
				else { 
					column.add(this.updateQueensFacing(col, row));
				}
			}
			this.moveValues.add(column);
		}
	}
	
	public void makeMove(int col, int row) {
		if( row > this.dim || row < 0) {
			throw new IllegalArgumentException("This is not a legal move");
		}
		try {
			this.queens.set(col	, row);
		}
		catch (Exception e) { throw new IllegalArgumentException("This is not a legal move"); }
		this.queensFacing();
		this.moveValues.clear();
		this.calcMoveValues();
	}
	
	public ArrayList<int[]> getBestMoves() {
		int bestMoveValue = this.queensFacing;
		ArrayList<int[]> moves = new ArrayList<int[]>();
		for(int col = 0; col < this.getDim(); col++) {
			for(int row = 0; row < this.getDim(); row++) {
				int value = this.moveValues.get(col).get(row);
				if(value <= bestMoveValue) {
					if ( value < bestMoveValue) {
						moves.clear();
					}
					bestMoveValue = value;
					int[] pos = new int[2];
					pos[0] = col;
					pos[1] = row;
					moves.add(pos);
				}
			}
		}
		ArrayList<int[]> newMoves = new ArrayList<int[]>();
		for (int[] move : moves) {
			if( this.queens.get(move[0]) != move[1]) {
				newMoves.add(move);
			}
		}
		return newMoves;
	}
	
	public int[] getBetterMove() {
		int bestMoveValue = this.queensFacing;
		int[] move = new int[2];
		//If no better moves exist, then the first index will be -1;
		move[0] = -1;
		for(int col = 0; col < this.getDim(); col++) {
			for(int row = 0; row < this.getDim(); row++) {
				int value = this.moveValues.get(col).get(row);
				if(value < bestMoveValue) {
					bestMoveValue = value;
					move[0] = col;
					move[1] = row;
				}
			}
		}
		return move;
	}
	
	public String toString() {
		String str = "Position of Queens: " + this.getQueens().toString();
		str += "\r\n" +"Number of Queens facing: " + this.queensFacing;
		for (ArrayList<Integer> col : this.moveValues) {
			str += "\r\n" + col.toString();
		}
		return str;
	}
	
	public static void main(String[] args) {
		
		ArrayList<Integer> config = new ArrayList<Integer>(Arrays.asList(0,5,1,4,6,3,7,2));
		ArrayList<Integer> config2 = new ArrayList<Integer>(Arrays.asList(3,2,1,4,3,2,1,2));
		
		Board board = new Board(config);
		Board board2 = new Board(config2);
		
		System.out.println(board);
		System.out.println(board2);
	}
}