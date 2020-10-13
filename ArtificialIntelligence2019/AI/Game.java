
import java.io.File;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

public class Game {

	int NDice, NSides, LTarget, UTarget, NGames, paramM;
	ArrayList<Dice> dice = new ArrayList<Dice>();
	ArrayList<Player> players = new ArrayList<Player>();
	ArrayList<Integer> currState = new ArrayList<Integer>();
	int firstGame = 0;

	Scanner scan;
	int GameCount = 0;

	int[][][] WinCount;
	int[][][] LoseCount;

	public class Dice {
		int id;
		int sides;

	}

	public class Player {
		int total, id;
		int[][][] Count;
	}
	
	public void prog3() {
		//hopefully wincount and losecount initialized to 0
		
		WinCount = new int[LTarget][LTarget][NDice + 1];
		//Arrays.fill(WinCount,1);
		LoseCount = new int[LTarget][LTarget][NDice + 1];
		
		//Loop over amount of games to play
		for(int i = 0; i < NGames; i++) {
			
			
			
			for (int j = 0; j < 2; j++) {
				Player player = new Player();
				player.id = i;
				player.Count = new int[LTarget][LTarget][NDice + 1];
				player.total = 0;
				players.add(player);
			}

		
			
			
			
			System.out.println("Game " + (i+1));
			playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, paramM);
		}
		
	}
	
	public int chooseDice(ArrayList<Integer> currState, int[][][] LoseCount, int [][][] WinCount, int NDice, int paramM) {
		
		
		int diceNum = 0;
		
			ArrayList<Integer> fj = new ArrayList<Integer>();
			int bMax = 0;
			int sum = 0;
			int stateTotal = 0;
			int b = 0;
			
			
			
			//Finding fj for j=0...k and b, which is the value of j with highest fj
			for (int j = 0; j < NDice; j++) {
				int x = (WinCount[currState.get(0)][currState.get(1)][j])
						/ (WinCount[currState.get(0)][currState.get(1)][j]
								+ LoseCount[currState.get(0)][currState.get(1)][j]);
				fj.add(x);
				if (x >= bMax) { // Might want to figure out how to break ties arbitrarily
					bMax = x;
					b = j;

				}
			}

			// Summing over all j not equal to b
			for (int j = 0; j < fj.size(); j++) {
				if (fj.get(j) != b) {
					sum += fj.get(j);
				}
			}

			//Sum of wincounts and losecounts from 0 to k - total number of games that have gone through current state ( wins and losses)
			for (int j = 0; j < NDice; j++) {
				stateTotal += WinCount[currState.get(0)][currState.get(1)][j]
						+ LoseCount[currState.get(0)][currState.get(1)][j];
			}

			//Choosing the dice
			
			//Finding the probability of rolling b dice - b determined earlier (how many dice would be best)
			double probB = (stateTotal * fj.get(b) + paramM)/(stateTotal * fj.get(b) + paramM*NDice);
			
			ArrayList<Double> probJ = new ArrayList<Double>();
			for(int j = 0; j<NDice; j++) {
				if(j != b) {
					probJ.add((1-probB) * ((stateTotal*fj.get(j)+paramM)/(sum*stateTotal + (NDice-1)*paramM)));
				}
			}
			
			ArrayList<Double> probMaster = new ArrayList<Double>(probJ);
			probMaster.add(probB);
			
			 diceNum = chooseFromDist(probMaster);

			
			
			//At this point you should have probB and arrayList of probabilities for probJ

			
		
		return diceNum;
		
	}
	
	

	public void playGame(int NDice, int NSides, int LTarget, int UTarget, int[][][] LoseCount, int[][][] WinCount, int paramM) {

		// Resetting current state and adding in the current total for player 1 and 2
		int gameover = 0; // check to determine if game is over
		
		
		// Play the game starting with player 1
		// Once loser is found, loop over all the states of that player and match them
		// to the master wincount and losecount
		
		while (gameover == 0) {
			
			currState.clear();
			currState.add(players.get(0).total);
			currState.add(players.get(1).total);

			
			for(int i = 0; i <players.size(); i++) {
				int numDice = 0;
				if(firstGame>0) {
			 numDice = chooseDice(currState, LoseCount, WinCount, NDice,paramM); //Choosing dice for current player
				}
				
				else {
					numDice=2;
					
				}
			
			players.get(i).Count[players.get(i).total][players.get(Math.abs(i-1)).total][numDice]++;

			
			
			
			
			int total = rollDice(numDice, NSides); //Rolling this player's dice
			players.get(i).total += total;
			
			
			//If your total is above UTarget, you lose
			
			if(players.get(i).total > UTarget) {
				
				///Setting LoseCount for current loser player
				for(int a = 0; a < LoseCount.length; a++) {
					for(int b = 0; b <LoseCount[a].length; b++) {
						for(int c = 0; c < LoseCount[a][b].length; c++) {
							LoseCount[a][b][c] = players.get(i).Count[a][b][c] + LoseCount[a][b][c];
						}
						
					}
				}
				
				//Setting the WinCount for the opponent who won
				for(int a = 0; a < WinCount.length; a++) {
					for(int b = 0; b <WinCount[a].length; b++) {
						for(int c = 0; c < WinCount[a][b].length; c++) {
							WinCount[a][b][c] = players.get(Math.abs(i-1)).Count[a][b][c] + WinCount[a][b][c];
						}
						
					}
				}
				
				
				firstGame++;
				gameover = 1;
				break;
			}
			//If your total falls in this range, you win	
			
			else if(players.get(i).total <= UTarget && players.get(i).total >= LTarget) {
				
				
				
				
				//Setting WinCount for current winner player
				for(int a = 0; a < WinCount.length; a++) {
					for(int b = 0; b <WinCount[a].length; b++) {
						for(int c = 0; c < WinCount[a][b].length; c++) {
							WinCount[a][b][c] = players.get(i).Count[a][b][c] + WinCount[a][b][c];
						}
						
					}
				}
				
				
				
				
				//Setting LoseCount for current loser player
				for(int a = 0; a < LoseCount.length; a++) {
					for(int b = 0; b <LoseCount[a].length; b++) {
						for(int c = 0; c < LoseCount[a][b].length; c++) {
							LoseCount[a][b][c] = players.get(Math.abs(i-1)).Count[a][b][c] + LoseCount[a][b][c];
						}
						
					}
				}
				gameover = 1;
				firstGame++;
				break;
			}
		
		
			}

		}
	}
	
	
	public int rollDice(int NDice, int NSides) {
		
		int total= 0;
		
		for(int i = 0; i <NDice; i++) {
			total+= (int)(Math.random()*NSides)+1;
			
		}
		
		
		
		System.out.println("Total is " + total);
		return total;
	}
	
	
	public int chooseFromDist(ArrayList<Double> p ) {
		ArrayList<Double> u = new ArrayList<Double>();
		double u0 = p.get(0);
		u.add(u0);
		
		
		for(int i = 1; i < p.size(); i++) {
			double u1 = u.get(i-1)+p.get(i);
			u.add(u1);	
		}
		
		double x = Math.random();
		
		for(int i = 0; i<p.size(); i++) {
			if(x < u.get(i)) {
				return i;
			}
		}
		
		return p.size();
		
		
	}
	
	
	


//Reading in input
	public void init(File f) throws FileNotFoundException {

		scan = new Scanner(f);

		NDice = scan.nextInt();
		System.out.println(NDice);
		NSides = scan.nextInt();
		System.out.println(NSides);

		LTarget = scan.nextInt();
		System.out.println(LTarget);

		UTarget = scan.nextInt();
		System.out.println(UTarget);

		NGames = scan.nextInt();
		paramM = scan.nextInt();

		for (int i = 0; i < NDice; i++) {
			Dice die = new Dice();
			die.id = i;
			die.sides = NSides;

		}

		

	}

	public static void main(String[] args) throws FileNotFoundException {

		File f = new File(args[0]);

		Game main = new Game();
		main.init(f);
		main.prog3();
		
		//for (int i = 0; i < main.NGames; i++) {
			//main.playGame();
		//}

	}

}
