#include <iostream>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <random>
#include <fstream>
#include <ctime>
#include <string>
#include <cmath>

using namespace std;

// set up random generator and define seed for each
random_device rd;
mt19937 generator(rd());

class Lattice {
public:
	// variables
	int dimensions;
	int numberSteps;
	vector<int> coordinates;

	// constructor
	Lattice(int d){
		dimensions = d;
		numberSteps = 0;

		// fills coordinate array with zeros
		// can probably be done with coordinates.assign(...)
		for(int i=0; i<d; i++){
			coordinates.push_back(0);
		}
	}

	// resets lattice to start position
	void reset(int d){
		vector<int> coordinates_new;
		dimensions = d;
		numberSteps = 0;
		for(int i=0; i<d; i++){
			coordinates_new.push_back(0);
		}
		coordinates = coordinates_new;
		// cout << "resetting" << endl;
	}

	// move function
	void move(){
		// int direction = rand()%dimensions;
		// int distance = rand()%2;

		uniform_int_distribution<> distribution1(0,dimensions-1);
		int direction = distribution1(generator);

		uniform_int_distribution<> distribution2(0,1);
		int distance = distribution2(generator);

		// so that distance is always -1 or 1
		if(distance == 0){
			distance = -1;
		}
		coordinates[direction] = coordinates[direction] + distance;
		numberSteps++;
		// cout << numberSteps << endl;
	}

	// randomise position, only works in 2d Circular well
	void randomisePosition(int boundary){

		int x = boundary;
		int y = boundary;

		while(sqrt((x * x) + (y * y)) > boundary){
			uniform_int_distribution<> distribution(-boundary, boundary);
			x = distribution(generator);
			y = distribution(generator);
		}

		coordinates[0] = x;
		coordinates[1] = y;
	}


	// caught function
	bool caught(double probability=0.1, string potential="", int boundary=0, int maxSteps=0){

		if((maxSteps == 0) || (numberSteps < maxSteps)){
			if(potential == ""){
				uniform_real_distribution<double> distribution(0.0,1.0);
				double number = distribution(generator);
			
				if(number <= probability){
					return true;
				}
				return false;
			}

			if(potential == "square"){
				for(int i=0; i<coordinates.size(); i++){
					if(!((coordinates[i] < boundary) && (coordinates[i] > (-1*boundary)))){
						return true;
					}
				}
				return false;
			}

			if(potential == "circle"){
				double tmp = 0;
				for(int i=0; i<coordinates.size(); i++){
					tmp = tmp + (coordinates[i] * coordinates[i]);
				}
				tmp = sqrt(tmp);
				if(!(tmp < boundary)){
					return true;
				}
				return false;
			}
			
			else{
				return false;
			}
		}

		else{
			// cout << "hello3" << endl;
			return true;
		}
	}

};


// prints a vector for debugging
void printVector(vector<int> item){
	for(int i=0; i<item.size(); i++){
		cout << item[i] << endl;
	}
}

int main(int argc, char* argv[]){
	// to do, take command line arguments to decide number of iterations and probability
	// make python function feed these arguments

	// probably unnecessary
	srand(time(NULL));   

	int dimen = atoi(argv[1]);
	int iterations = atoi(argv[2]);
	int maxSteps = atoi(argv[3]);
	double probability = atof(argv[4]);
	string potential = argv[5];
	int boundary = atoi(argv[6]);
	int randomise = atoi(argv[7]);

	// cout << dimen << endl;
	// cout << probability << endl;
	// cout << iterations << endl;
	// cout << maxSteps << endl;

	Lattice lattice(dimen);

	
	vector<int> data;
	vector<int> positions;

	// run the random walk
	for(int i=0; i<iterations; i++){

		if(randomise == 1){lattice.randomisePosition(boundary);}

		else{lattice.reset(dimen);}


		bool caught = false;
		int time = 0;
		while(caught != true){
			time++;
			lattice.move();
			caught = lattice.caught(probability, potential, boundary, maxSteps);
		}
		// append to data

		if(potential == "circle"){
			for(int i=0; i<lattice.coordinates.size(); i++){
				positions.push_back(lattice.coordinates[i]);
			}
		}
		data.push_back(time);
	}

	ofstream myfile;
	myfile.open("data.dat");
	for(int i=0; i<data.size(); i++){
		myfile << data[i] << "\n";
	}
	myfile.close();

	ofstream myfile1;
	myfile1.open("positions.dat");
	for(int i=0; i<positions.size(); i++){
		myfile1 << positions[i] << "\n";
	}
	myfile1.close();
	
	return 0;
}
