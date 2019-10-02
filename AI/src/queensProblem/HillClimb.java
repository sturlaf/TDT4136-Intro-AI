package queensProblem;

import java.util.ArrayList;
import java.util.Random;

public class HillClimb {
	
	private int dim;
	private Board board;
	private boolean succses = false;
	private int maxDepth;
	private int iterations = 1;
	
	public HillClimb(int dim, int maxDepth) {
		this.dim = dim;
		this.maxDepth = maxDepth;
		Random rand = new Random();
		this.reshufle(rand);
	}

	public void reshufle(Random rand) {
		ArrayList<Integer> queenPositions = new ArrayList<Integer>();
		for(int col = 0; col < this.dim; col++) {
			queenPositions.add(rand.nextInt(this.dim));
		}
		this.board = new Board(queenPositions);
	}
	
	public void reshufleBoard(Random rand) {
		ArrayList<Integer> queenPositions = new ArrayList<Integer>();
		for(int col = 0; col < this.dim; col++) {
			queenPositions.add(rand.nextInt(this.dim));
		}
		this.board.setQueens(queenPositions);

	}
	
	public boolean getSuccses() {
		return this.succses;
	}
	
	public HillClimb(int dim) {
		this(dim, 100);
	}
	
	public int getCount() {
		return this.iterations;
	}
	
	private void count() {
		this.iterations++;
	}

	private void nextMove() {
		ArrayList<int[]> bestMoves = this.board.getBestMoves();
		if( !bestMoves.isEmpty()) {
			this.pickMove(bestMoves);
			bestMoves = this.board.getBestMoves();
		}
	}

	private void pickMove(ArrayList<int[]> bestMoves) {
		Random rand = new Random();
		int[] bestMove = bestMoves.get(rand.nextInt(bestMoves.size()));
		this.board.makeMove(bestMove[0], bestMove[1]);
		
	}
	
	public void hillClimbing() {
		int[] move = this.board.getBetterMove();
		while (move[0] != -1) {
			this.board.makeMove(move[0], move[1]);
			move = this.board.getBetterMove();
			this.count();
		}
		if ( this.board.getQueensFacing() == 0 ) {
			this.succses = true;
		}
	}
	
	private void sidewaysHillClimbing(int count) {
		if (count > this.maxDepth) {
			System.out.println("failed");
		}
		else if( this.board.getQueensFacing() == 0) {
			this.succses = true;
		}
		else {
			int lastValue = this.board.getQueensFacing();
			this.nextMove();
			int newValue = this.board.getQueensFacing();
			if(lastValue == newValue) {
				count++;
			}
			else { count = 0; }
			this.count();
			this.sidewaysHillClimbing(count);
		}
	}
	
	public void sidewaysHillClimbing() {
		this.sidewaysHillClimbing(0);
	}
	
	public Board getConfig() {
		return this.board;
	}
	
	public String toString() {
		return this.board.toString() + "\r\n" + this.getCount();
	}
	
	public static void main(String[] args) {

		HillClimb solution = new HillClimb(100);
		
		solution.sidewaysHillClimbing();
		
		System.out.println(solution);
		

	}

}
