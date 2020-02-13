#include <iostream>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <random>
#include <fstream>
#include <ctime>

using namespace std;


/*
I use this method instead of rand because rand is seeded to time
And each use of rand seeds to time (not previous value like in python)
But the time is in seconds, so over many iterations, many random
values are repeated
*/

// set up random generators and define seeds for each
random_device rd1;
random_device rd2;
random_device rd3;
mt19937 generator1(rd1());
mt19937 generator2(rd2());
mt19937 generator3(rd3());

class Lattice {
public:
    // variables
    int dimensions;
    vector<int> coordinates;

    // constructor
    Lattice(int d){
	dimensions = d;

	// fills coordinate array with zeros
	// can probably be done with coordinates.assign(...)
	for(int i=0; i<d; i++){
	    coordinates.push_back(0);
	}
    }

  // move function
    void move(){
	// int direction = rand()%dimensions;
	// int distance = rand()%2;

	uniform_int_distribution<> distribution1(0,dimensions-1);
	int direction = distribution1(generator1);

	uniform_int_distribution<> distribution2(0,1);
	int distance = distribution2(generator2);

	// so that distance is always -1 or 1
	if(distance == 0){
	    distance = -1;
	}
	coordinates[direction] = coordinates[direction] + distance;
    }

  // caught function
    bool caught(double probability){
      uniform_real_distribution<double> distribution3(0.0,1.0);
      double number = distribution3(generator3);

      if(number < probability){
	  return true;
      }
      return false;
  }

};

int main(){

    srand(time(NULL));   

    int dimen = 4;
    Lattice lattice(dimen);
    
    vector<int> data;

    // run the random walk
    for(int i=0; i<1000; i++){
	bool caught = false;
	int time = 0;
	while(caught != true){
	    time++;
	    lattice.move();

	    caught = lattice.caught(0.1);
	}
	// append to data
	data.push_back(time);
    }

    // for debugging 
    // for(int i=0; i<data.size(); i++){
    // 	cout << data[i] << "\n";
    // }

    ofstream myfile;
    myfile.open("data.dat");
    for(int i=0; i<data.size(); i++){
    	myfile << data[i] << "\n";
    }
    myfile.close();
    return 0;
}
