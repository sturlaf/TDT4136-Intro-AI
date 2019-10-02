package queensProblem;

import java.util.Random;

public class RandomRestartHillClimb {
	
	private int count = 0;
	private int maxDepth, dim;
	private HillClimb hillClimb;
	private Random random;
	
	public RandomRestartHillClimb(int dim, int maxDepth) {
		this.maxDepth = maxDepth;
		this.dim = dim;
		this.hillClimb = new HillClimb(this.dim, this.maxDepth);
		this.random = new Random();
	}
	
	public RandomRestartHillClimb(int dim) {
		this(dim, 30);
	}
	
	public void randomRestartHillClimbing() {
		while (!this.hillClimb.getSuccses()) {
			this.hillClimb.reshufleBoard(this.random);
			this.hillClimb.hillClimbing();
		}
		this.count = hillClimb.getCount();
	}
	
	public void randomSidewaysRestart() {
		while (!this.hillClimb.getSuccses()) {
			this.hillClimb.reshufleBoard(this.random);
			this.hillClimb.sidewaysHillClimbing();	
		}
		this.count = hillClimb.getCount();
	}
	
	public String toString() {
		return this.hillClimb.toString();
	}

	public int getCount() {
		return count;
	}
	
	public static void main(String[] args) {
		
		RandomRestartHillClimb solution = new RandomRestartHillClimb(200);
		
		//solution.randomRestartHillClimbing();
		
		System.out.print(solution);
	}
}
